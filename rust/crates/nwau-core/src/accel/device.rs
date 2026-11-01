//! Unified device abstraction with automatic GPU detection and seamless CPU fallback.

use super::cpu::{bootstrap_cpu, evaluate_batch_cpu, DEFAULT_NEP};
use super::types::{AccelerationInfo, BootstrapResult, EpisodeGpuInput, EpisodeGpuOutput};

#[cfg(feature = "hardware-accel")]
use super::gpu::GpuContext;

/// Compute device selecting between native GPU shader execution and multi-core Rayon CPU execution.
pub enum ComputeDevice {
    /// Multi-threaded CPU execution with Rayon and SIMD chunking.
    Cpu,
    /// Hardware GPU execution (Metal on Apple Silicon, Vulkan on Linux, DX12 on Windows).
    #[cfg(feature = "hardware-accel")]
    Gpu(Box<GpuContext>),
}

impl ComputeDevice {
    /// Automatically select the highest performance available compute device.
    ///
    /// Tries GPU acceleration first (Metal on macOS, Vulkan on Linux, DX12 on Windows).
    /// If no compatible GPU adapter is detected, falls back seamlessly to CPU multi-threading.
    pub fn auto() -> Self {
        #[cfg(feature = "hardware-accel")]
        {
            if let Some(gpu) = GpuContext::try_init() {
                return ComputeDevice::Gpu(Box::new(gpu));
            }
        }
        ComputeDevice::Cpu
    }

    /// Force multi-core CPU execution.
    pub fn cpu() -> Self {
        ComputeDevice::Cpu
    }

    /// Force GPU execution (returns None if no GPU adapter is available).
    pub fn gpu() -> Option<Self> {
        #[cfg(feature = "hardware-accel")]
        {
            GpuContext::try_init().map(|g| ComputeDevice::Gpu(Box::new(g)))
        }
        #[cfg(not(feature = "hardware-accel"))]
        {
            None
        }
    }

    /// Evaluate a batch of episodes using the active compute device.
    pub fn evaluate_batch(
        &self,
        episodes: &[EpisodeGpuInput],
        nep: Option<f32>,
    ) -> Vec<EpisodeGpuOutput> {
        let nep = nep.unwrap_or(DEFAULT_NEP);

        #[cfg(feature = "hardware-accel")]
        if let ComputeDevice::Gpu(gpu) = self {
            match gpu.evaluate_episodes(episodes, nep) {
                Ok(outputs) => return outputs,
                Err(err) => {
                    eprintln!("GPU evaluation failed, falling back to CPU: {}", err);
                }
            }
        }

        evaluate_batch_cpu(episodes, nep)
    }

    /// Perform parallel Monte Carlo bootstrap resampling using the active compute device.
    pub fn bootstrap(
        &self,
        values: &[f64],
        iterations: usize,
        sample_size: Option<usize>,
    ) -> BootstrapResult {
        #[cfg(feature = "hardware-accel")]
        if let ComputeDevice::Gpu(gpu) = self {
            if let Ok(res) = gpu.bootstrap(values, iterations, sample_size) {
                return res;
            }
        }

        bootstrap_cpu(values, iterations, sample_size)
    }

    /// Return metadata describing the active compute device and SIMD architecture.
    pub fn acceleration_info(&self) -> AccelerationInfo {
        let simd_arch = if cfg!(target_arch = "aarch64") {
            "ARM NEON 128-bit SIMD".to_string()
        } else if cfg!(target_arch = "x86_64") {
            "x86_64 AVX2 / SSE4.2".to_string()
        } else {
            "Portable Scalar Fallback".to_string()
        };

        let threads = rayon::current_num_threads();

        #[cfg(feature = "hardware-accel")]
        if let ComputeDevice::Gpu(gpu) = self {
            let backend_name = match gpu.adapter_info.backend {
                wgpu::Backend::Metal => "Apple Silicon Metal GPU".to_string(),
                wgpu::Backend::Vulkan => "Vulkan Compute GPU".to_string(),
                wgpu::Backend::Dx12 => "DirectX 12 Compute GPU".to_string(),
                _ => format!("{:?} GPU", gpu.adapter_info.backend),
            };

            return AccelerationInfo {
                backend_name,
                is_gpu: true,
                simd_architecture: simd_arch,
                available_threads: threads,
                device_description: Some(gpu.adapter_info.name.clone()),
            };
        }

        AccelerationInfo {
            backend_name: "Rayon Multi-Core CPU".to_string(),
            is_gpu: false,
            simd_architecture: simd_arch,
            available_threads: threads,
            device_description: None,
        }
    }
}

impl Default for ComputeDevice {
    fn default() -> Self {
        Self::auto()
    }
}
