//! Provenance metadata types for tracking calculation context.
//!
//! Provenance records the source and configuration context for a batch of
//! calculations, enabling audit trails and reproducibility.

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// Top-level provenance metadata attached to a calculation batch.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Provenance {
    /// Unique batch identifier.
    pub batch_id: Uuid,
    /// Timestamp when the batch was created.
    pub created_at: DateTime<Utc>,
    /// Kernel label used for this batch.
    pub kernel_label: String,
    /// Pricing year.
    pub pricing_year: u16,
    /// Source description (e.g. "synthetic fixture data").
    pub source: String,
    /// Optional version tag.
    pub version: Option<String>,
    /// Optional user or process identifier.
    pub run_by: Option<String>,
    /// Optional free-form notes.
    pub notes: Option<String>,
}

impl Provenance {
    /// Create a new provenance record with the current timestamp.
    pub fn new(
        kernel_label: impl Into<String>,
        pricing_year: u16,
        source: impl Into<String>,
    ) -> Self {
        Self {
            batch_id: Uuid::new_v4(),
            created_at: Utc::now(),
            kernel_label: kernel_label.into(),
            pricing_year,
            source: source.into(),
            version: None,
            run_by: None,
            notes: None,
        }
    }

    /// Attach a version string.
    pub fn with_version(mut self, version: impl Into<String>) -> Self {
        self.version = Some(version.into());
        self
    }

    /// Attach a run-by identifier.
    pub fn with_run_by(mut self, run_by: impl Into<String>) -> Self {
        self.run_by = Some(run_by.into());
        self
    }
}

/// Provenance recorded for a single episode result.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EpisodeProvenance {
    /// Reference to the batch provenance batch_id.
    pub batch_id: Uuid,
    /// Episode identifier (if available).
    pub episode_id: Option<String>,
    /// DRG code.
    pub drg: String,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn provenance_creation() {
        let prov = Provenance::new("acute-2025", 2025, "synthetic fixture");
        assert_eq!(prov.kernel_label, "acute-2025");
        assert_eq!(prov.pricing_year, 2025);
        assert!(prov.batch_id != Uuid::nil());
    }

    #[test]
    fn provenance_with_optional_fields() {
        let prov = Provenance::new("acute-2025", 2025, "test")
            .with_version("0.1.0")
            .with_run_by("ci");
        assert_eq!(prov.version.unwrap(), "0.1.0");
        assert_eq!(prov.run_by.unwrap(), "ci");
    }
}
