//! Manifest schema types for describing calculator configurations and
//! data file sets.

use serde::{Deserialize, Serialize};

/// A top-level manifest describing a calculator run configuration.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Manifest {
    /// Manifest format version.
    pub manifest_version: String,
    /// Calculator identifier.
    pub calculator: String,
    /// Pricing year.
    pub pricing_year: u16,
    /// Human-readable description.
    pub description: Option<String>,
    /// Input data sources.
    pub sources: ManifestSources,
    /// Adjustment factor overrides (optional).
    pub adjustments: Option<ManifestAdjustments>,
}

/// Data sources referenced in a manifest.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ManifestSources {
    /// Path or reference to the episode input file.
    pub episodes: String,
    /// Path or reference to the reference rows file.
    pub reference: String,
    /// Path for the output file.
    pub output: Option<String>,
    /// Optional format hint ("csv" or "parquet").
    pub format: Option<String>,
}

/// Adjustment factor overrides in a manifest.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ManifestAdjustments {
    /// ICU hourly rate.
    pub icu_rate: Option<f64>,
    /// COVID adjustment.
    pub covid_adjustment: Option<f64>,
    /// Indigenous adjustment.
    pub indigenous_adjustment: Option<f64>,
    /// Remoteness adjustment.
    pub remoteness_adjustment: Option<f64>,
    /// Treatment remoteness adjustment.
    pub treatment_remoteness_adjustment: Option<f64>,
    /// Radiotherapy adjustment.
    pub radiotherapy_adjustment: Option<f64>,
    /// Dialysis adjustment.
    pub dialysis_adjustment: Option<f64>,
    /// Private accommodation same-day deduction.
    pub private_accommodation_same_day: Option<f64>,
    /// Private accommodation overnight deduction.
    pub private_accommodation_overnight: Option<f64>,
}

impl Manifest {
    /// Create a minimal manifest.
    pub fn new(
        calculator: impl Into<String>,
        pricing_year: u16,
        episodes: impl Into<String>,
        reference: impl Into<String>,
    ) -> Self {
        Self {
            manifest_version: "0.1.0".into(),
            calculator: calculator.into(),
            pricing_year,
            description: None,
            sources: ManifestSources {
                episodes: episodes.into(),
                reference: reference.into(),
                output: None,
                format: None,
            },
            adjustments: None,
        }
    }

    /// Parse a manifest from a JSON string.
    pub fn from_json(json: &str) -> Result<Self, serde_json::Error> {
        serde_json::from_str(json)
    }

    /// Serialize to a JSON string.
    pub fn to_json(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string_pretty(self)
    }

    /// Set the description and return self.
    pub fn with_description(mut self, desc: impl Into<String>) -> Self {
        self.description = Some(desc.into());
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn manifest_json_roundtrip() {
        let manifest = Manifest::new("acute-2025", 2025, "episodes.csv", "reference.csv")
            .with_description("synthetic test");
        let json = manifest.to_json().unwrap();
        let parsed = Manifest::from_json(&json).unwrap();
        assert_eq!(parsed.calculator, "acute-2025");
        assert_eq!(parsed.pricing_year, 2025);
        assert_eq!(parsed.sources.episodes, "episodes.csv");
    }

    #[test]
    fn manifest_with_adjustments() {
        let mut manifest = Manifest::new("acute-2025", 2025, "episodes.csv", "reference.csv");
        manifest.adjustments = Some(ManifestAdjustments {
            icu_rate: Some(0.05),
            covid_adjustment: None,
            indigenous_adjustment: None,
            remoteness_adjustment: None,
            treatment_remoteness_adjustment: None,
            radiotherapy_adjustment: None,
            dialysis_adjustment: None,
            private_accommodation_same_day: None,
            private_accommodation_overnight: None,
        });
        let json = manifest.to_json().unwrap();
        let parsed = Manifest::from_json(&json).unwrap();
        assert!((parsed.adjustments.unwrap().icu_rate.unwrap() - 0.05).abs() < 1e-6);
    }
}
