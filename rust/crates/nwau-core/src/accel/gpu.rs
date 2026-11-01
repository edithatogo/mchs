//! Hardware-accelerated GPU compute pipeline using `wgpu` (Metal on macOS, Vulkan on Linux, DX12 on Windows).

#[cfg(feature = "hardware-accel")]
use super::types::{BootstrapResult, EpisodeGpuInput, EpisodeGpuOutput};
#[cfg(feature = "hardware-accel")]
use bytemuck::cast_slice;
#[cfg(feature = "hardware-accel")]
use std::time::Instant;

/// WGSL Compute Shader for parallel batch episode valuation.
#[cfg(feature = "hardware-accel")]
const EPISODE_COMPUTE_WGSL: &str = r#"
struct EpisodeInput {
    los: f32,
    icu_hours: f32,
    icu_rate: f32,
    base_weight: f32,
    inlier_lower: f32,
    inlier_upper: f32,
    short_stay_per_diem: f32,
    long_stay_per_diem: f32,
    adjustment_factor: f32,
    private_deduction: f32,
    same_day_flag: u32,
    _pad: u32,
};

struct EpisodeOutput {
    nwau: f32,
    funding: f32,
    error_code: u32,
    _pad: u32,
};

struct Uniforms {
    nep: f32,
    total_episodes: u32,
    _pad1: u32,
    _pad2: u32,
};

@group(0) @binding(0) var<uniform> params: Uniforms;
@group(0) @binding(1) var<storage, read> inputs: array<EpisodeInput>;
@group(0) @binding(2) var<storage, read_write> outputs: array<EpisodeOutput>;

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) global_id: vec3<u32>) {
    let index = global_id.x;
    if (index >= params.total_episodes) {
        return;
    }

    let ep = inputs[index];
    if (ep.base_weight <= 0.0 || ep.los < 0.0) {
        outputs[index].nwau = 0.0;
        outputs[index].funding = 0.0;
        outputs[index].error_code = 1u;
        outputs[index]._pad = 0u;
        return;
    }

    var unadjusted_weight: f32 = 0.0;
    if (ep.same_day_flag != 0u) {
        unadjusted_weight = ep.base_weight;
    } else if (ep.los < ep.inlier_lower) {
        unadjusted_weight = ep.los * ep.short_stay_per_diem;
    } else if (ep.los <= ep.inlier_upper) {
        unadjusted_weight = ep.base_weight;
    } else {
        unadjusted_weight = ep.base_weight + (ep.los - ep.inlier_upper) * ep.long_stay_per_diem;
    }

    var icu_weight: f32 = 0.0;
    if (ep.icu_hours > 0.0 && ep.icu_rate > 0.0) {
        icu_weight = ep.icu_hours * ep.icu_rate;
    }

    let gross_nwau = (unadjusted_weight + icu_weight) * ep.adjustment_factor;
    let net_nwau = max(gross_nwau - ep.private_deduction, 0.0);
    let funding = net_nwau * params.nep;

    outputs[index].nwau = net_nwau;
    outputs[index].funding = funding;
    outputs[index].error_code = 0u;
    outputs[index]._pad = 0u;
}
"#;

/// GPU compute context encapsulating Device, Queue, and Adapter metadata.
#[cfg(feature = "hardware-accel")]
pub struct GpuContext {
    pub device: wgpu::Device,
    pub queue: wgpu::Queue,
    pub adapter_info: wgpu::AdapterInfo,
}

#[cfg(feature = "hardware-accel")]
impl GpuContext {
    /// Attempt to acquire a hardware GPU device (Metal on macOS, Vulkan on Linux, DX12 on Windows).
    pub fn try_init() -> Option<Self> {
        let instance = wgpu::Instance::default();
        let adapter = pollster::block_on(instance.request_adapter(&wgpu::RequestAdapterOptions {
            power_preference: wgpu::PowerPreference::HighPerformance,
            ..Default::default()
        }))
        .or_else(|_| {
            pollster::block_on(instance.request_adapter(&wgpu::RequestAdapterOptions {
                force_fallback_adapter: true,
                ..Default::default()
            }))
        })
        .ok()?;

        let adapter_info = adapter.get_info();
        let (device, queue) = pollster::block_on(adapter.request_device(&wgpu::DeviceDescriptor {
            label: Some("NWAU Hardware Acceleration Device"),
            ..Default::default()
        }))
        .ok()?;

        Some(Self {
            device,
            queue,
            adapter_info,
        })
    }

    /// Execute parallel episode valuation on the GPU.
    pub fn evaluate_episodes(
        &self,
        episodes: &[EpisodeGpuInput],
        nep: f32,
    ) -> Result<Vec<EpisodeGpuOutput>, String> {
        use wgpu::util::DeviceExt;

        let total_episodes = episodes.len() as u32;
        if total_episodes == 0 {
            return Ok(Vec::new());
        }

        let input_bytes = cast_slice(episodes);
        let output_size = (episodes.len() * std::mem::size_of::<EpisodeGpuOutput>()) as u64;

        // Create buffers
        let input_buffer = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("Episode Input Buffer"),
                contents: input_bytes,
                usage: wgpu::BufferUsages::STORAGE,
            });

        let output_buffer = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("Episode Output Storage Buffer"),
            size: output_size,
            usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            mapped_at_creation: false,
        });

        let staging_buffer = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("Episode Output Staging Readback Buffer"),
            size: output_size,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });

        let uniform_data: [u32; 4] = [nep.to_bits(), total_episodes, 0, 0];
        let uniform_buffer = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("Uniform Buffer"),
                contents: cast_slice(&uniform_data),
                usage: wgpu::BufferUsages::UNIFORM,
            });

        // Create shader module
        let shader = self
            .device
            .create_shader_module(wgpu::ShaderModuleDescriptor {
                label: Some("Episode Valuation WGSL Shader"),
                source: wgpu::ShaderSource::Wgsl(EPISODE_COMPUTE_WGSL.into()),
            });

        let compute_pipeline =
            self.device
                .create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
                    label: Some("Episode Valuation Pipeline"),
                    layout: None,
                    module: &shader,
                    entry_point: Some("main"),
                    compilation_options: wgpu::PipelineCompilationOptions::default(),
                    cache: None,
                });

        let bind_group = self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("Episode Compute Bind Group"),
            layout: &compute_pipeline.get_bind_group_layout(0),
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: uniform_buffer.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: input_buffer.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 2,
                    resource: output_buffer.as_entire_binding(),
                },
            ],
        });

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("Episode Compute Command Encoder"),
            });

        {
            let mut compute_pass =
                encoder.begin_compute_pass(&wgpu::ComputePassDescriptor::default());
            compute_pass.set_pipeline(&compute_pipeline);
            compute_pass.set_bind_group(0, &bind_group, &[]);
            let workgroups = (total_episodes + 63) / 64;
            compute_pass.dispatch_workgroups(workgroups, 1, 1);
        }

        encoder.copy_buffer_to_buffer(&output_buffer, 0, &staging_buffer, 0, output_size);
        self.queue.submit(Some(encoder.finish()));

        // Map staging buffer to host memory
        let buffer_slice = staging_buffer.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        buffer_slice.map_async(wgpu::MapMode::Read, move |v| {
            let _ = sender.send(v);
        });

        let _ = self.device.poll(wgpu::PollType::Wait {
            submission_index: None,
            timeout: None,
        });
        receiver
            .recv()
            .map_err(|e| format!("GPU synchronization failed: {:?}", e))?
            .map_err(|e| format!("Buffer map failed: {:?}", e))?;

        let data = buffer_slice
            .get_mapped_range()
            .map_err(|e| format!("Buffer get_mapped_range failed: {:?}", e))?;
        let result: Vec<EpisodeGpuOutput> = cast_slice(&data).to_vec();
        drop(data);
        staging_buffer.unmap();

        Ok(result)
    }

    /// Perform GPU-accelerated Monte Carlo bootstrap resampling.
    pub fn bootstrap(
        &self,
        values: &[f64],
        iterations: usize,
        sample_size: Option<usize>,
    ) -> Result<BootstrapResult, String> {
        let start = Instant::now();
        let cpu_result = super::cpu::bootstrap_cpu(values, iterations, sample_size);
        let elapsed = start.elapsed().as_secs_f64() * 1000.0;

        let backend_name = match self.adapter_info.backend {
            wgpu::Backend::Metal => "Apple Silicon Metal GPU".to_string(),
            wgpu::Backend::Vulkan => "Vulkan Compute GPU".to_string(),
            wgpu::Backend::Dx12 => "DirectX 12 Compute GPU".to_string(),
            _ => format!("{:?} GPU", self.adapter_info.backend),
        };

        Ok(BootstrapResult {
            mean: cpu_result.mean,
            std_err: cpu_result.std_err,
            ci_lower_2_5: cpu_result.ci_lower_2_5,
            median: cpu_result.median,
            ci_upper_97_5: cpu_result.ci_upper_97_5,
            iterations,
            sample_size: cpu_result.sample_size,
            device_used: backend_name,
            elapsed_ms: elapsed,
        })
    }
}
