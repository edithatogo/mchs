use nwau_core::{
    kernels::{SubAcuteBoundary, SUBACUTE_CANARY_DRG, SUBACUTE_UNSUPPORTED_ERROR_CODE},
    Acute2025Kernel, AdjustmentFactors, DiagnosticLevel, EpisodeFlags, EpisodeRow, Kernel,
    KernelRegistry, ReferenceRow, SubAcuteKernel,
};

fn neutral_episode() -> EpisodeRow {
    EpisodeRow {
        drg: "801A".into(),
        los: 10.0,
        icu_hours: 0.0,
        icu_other: 0.0,
        flags: EpisodeFlags::default(),
        episode_id: Some("phase2-gate".into()),
    }
}

fn neutral_reference() -> ReferenceRow {
    ReferenceRow {
        drg: "801A".into(),
        inlier_lower_bound: 7.0,
        inlier_upper_bound: 72.0,
        paediatric_multiplier: 1.35,
        same_day_list_flag: false,
        bundled_icu_flag: false,
        same_day_base_weight: 0.9527,
        same_day_per_diem: 1.1849,
        inlier_weight: 9.2472,
        long_stay_per_diem: 0.26,
        private_service_adjustment: 0.0,
    }
}

fn subacute_canary_episode() -> EpisodeRow {
    EpisodeRow {
        drg: SUBACUTE_CANARY_DRG.into(),
        los: 12.0,
        icu_hours: 0.0,
        icu_other: 0.0,
        flags: EpisodeFlags::default(),
        episode_id: Some("subacute-canary".into()),
    }
}

fn subacute_canary_reference() -> ReferenceRow {
    ReferenceRow {
        drg: SUBACUTE_CANARY_DRG.into(),
        inlier_lower_bound: 1.0,
        inlier_upper_bound: 30.0,
        paediatric_multiplier: 1.0,
        same_day_list_flag: false,
        bundled_icu_flag: true,
        same_day_base_weight: 0.0,
        same_day_per_diem: 0.0,
        inlier_weight: 2.5,
        long_stay_per_diem: 0.0,
        private_service_adjustment: 0.0,
    }
}

#[test]
fn phase2_defaults_expose_only_acute_as_a_promotable_kernel() {
    let registry = KernelRegistry::new().with_defaults();
    let labels = registry.labels();

    assert!(labels.contains(&"acute-2025"));
    assert!(labels.contains(&"sub-acute"));
    assert!(registry.get("emergency").is_none());
    assert!(registry.get("community-mental-health").is_none());
    assert!(registry.get("non-admitted").is_none());
}

#[test]
fn phase3_acute_kernel_remains_promotable() {
    let kernel = Acute2025Kernel::new();
    let output = kernel.calculate(
        &neutral_episode(),
        &neutral_reference(),
        &AdjustmentFactors::default(),
    );

    assert_eq!(kernel.label(), "acute-2025");
    assert_eq!(output.error_code, 0);
    assert!((output.nwau - 9.2472).abs() < 1e-4);
}

#[test]
fn phase3_subacute_canary_calculates_inside_bounded_slice() {
    let kernel = SubAcuteKernel::new();
    let episode = subacute_canary_episode();
    let reference = subacute_canary_reference();
    let adjustments = AdjustmentFactors::default();

    let output = kernel.calculate(&episode, &reference, &adjustments);
    let diagnostic = kernel.diagnostic(&episode, &reference, &adjustments);

    assert_eq!(kernel.label(), "sub-acute");
    assert_eq!(
        kernel.boundary(&episode, &reference, &adjustments),
        SubAcuteBoundary::Canary
    );
    assert_eq!(output.error_code, 0);
    assert_eq!(output.nwau, 2.5);
    assert_eq!(output.gwau, 2.5);
    assert_eq!(diagnostic.level, DiagnosticLevel::Warning);
    assert_eq!(diagnostic.drg.as_deref(), Some(SUBACUTE_CANARY_DRG));
}

#[test]
fn phase3_subacute_non_canary_remains_unsupported_for_promotion() {
    let kernel = SubAcuteKernel::new();
    let episode = neutral_episode();
    let reference = neutral_reference();
    let adjustments = AdjustmentFactors::default();
    let output = kernel.calculate(&episode, &reference, &adjustments);
    let diagnostic = kernel.diagnostic(&episode, &reference, &adjustments);

    assert_eq!(kernel.label(), "sub-acute");
    assert_eq!(
        kernel.boundary(&episode, &reference, &adjustments),
        SubAcuteBoundary::Unsupported
    );
    assert_eq!(output.error_code, SUBACUTE_UNSUPPORTED_ERROR_CODE);
    assert_eq!(output.nwau, 0.0);
    assert_eq!(diagnostic.level, DiagnosticLevel::Error);
    assert!(diagnostic.message.contains("not promoted"));
}
