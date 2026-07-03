//! Diagnostic and error types for the NWAU calculation pipeline.

use thiserror::Error;

/// Top-level error type for the nwau-core crate.
#[derive(Error, Debug, Clone)]
pub enum NwauError {
    /// A reference row was not found for the given DRG.
    #[error("reference row not found for DRG: {0}")]
    ReferenceRowNotFound(String),

    /// An episode input failed validation.
    #[error("validation error: {0}")]
    ValidationError(String),

    /// An I/O error occurred.
    #[error("I/O error: {0}")]
    IoError(String),

    /// A format or parsing error occurred.
    #[error("format error: {0}")]
    FormatError(String),

    /// An unknown or unclassified error occurred.
    #[error("unknown error: {0}")]
    Unknown(String),
}

/// A diagnostic message emitted during calculation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Diagnostic {
    /// The severity level.
    pub level: DiagnosticLevel,
    /// A human-readable message.
    pub message: String,
    /// Optional DRG code associated with this diagnostic.
    pub drg: Option<String>,
    /// Optional episode identifier.
    pub episode_id: Option<String>,
}

/// Severity level for diagnostics.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum DiagnosticLevel {
    /// Informational message.
    Info,
    /// Warning — calculation proceeded but with caveats.
    Warning,
    /// Error — calculation could not be completed for this episode.
    Error,
}

impl Diagnostic {
    /// Create an info-level diagnostic.
    pub fn info(message: impl Into<String>) -> Self {
        Self {
            level: DiagnosticLevel::Info,
            message: message.into(),
            drg: None,
            episode_id: None,
        }
    }

    /// Create a warning-level diagnostic.
    pub fn warning(message: impl Into<String>) -> Self {
        Self {
            level: DiagnosticLevel::Warning,
            message: message.into(),
            drg: None,
            episode_id: None,
        }
    }

    /// Create an error-level diagnostic.
    pub fn error(message: impl Into<String>) -> Self {
        Self {
            level: DiagnosticLevel::Error,
            message: message.into(),
            drg: None,
            episode_id: None,
        }
    }

    /// Attach a DRG code to this diagnostic.
    pub fn with_drg(mut self, drg: impl Into<String>) -> Self {
        self.drg = Some(drg.into());
        self
    }

    /// Attach an episode identifier to this diagnostic.
    pub fn with_episode_id(mut self, id: impl Into<String>) -> Self {
        self.episode_id = Some(id.into());
        self
    }
}

/// Accumulates diagnostics during a batch calculation.
#[derive(Debug, Clone, Default)]
pub struct DiagnosticCollector {
    diagnostics: Vec<Diagnostic>,
}

impl DiagnosticCollector {
    /// Create a new empty collector.
    pub fn new() -> Self {
        Self {
            diagnostics: Vec::new(),
        }
    }

    /// Record a diagnostic.
    pub fn record(&mut self, diagnostic: Diagnostic) {
        self.diagnostics.push(diagnostic);
    }

    /// Return all recorded diagnostics.
    pub fn diagnostics(&self) -> &[Diagnostic] {
        &self.diagnostics
    }

    /// Return all error-level diagnostics.
    pub fn errors(&self) -> Vec<&Diagnostic> {
        self.diagnostics
            .iter()
            .filter(|d| d.level == DiagnosticLevel::Error)
            .collect()
    }

    /// Return all warning-level diagnostics.
    pub fn warnings(&self) -> Vec<&Diagnostic> {
        self.diagnostics
            .iter()
            .filter(|d| d.level == DiagnosticLevel::Warning)
            .collect()
    }

    /// Return true if any error-level diagnostics have been recorded.
    pub fn has_errors(&self) -> bool {
        !self.errors().is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn diagnostic_levels() {
        let diag = Diagnostic::error("test error");
        assert_eq!(diag.level, DiagnosticLevel::Error);
    }

    #[test]
    fn diagnostic_collector() {
        let mut collector = DiagnosticCollector::new();
        collector.record(Diagnostic::info("started"));
        collector.record(Diagnostic::error("failed").with_drg("801A"));
        assert_eq!(collector.diagnostics().len(), 2);
        assert!(collector.has_errors());
        assert_eq!(collector.errors().len(), 1);
        assert_eq!(collector.warnings().len(), 0);
    }

    #[test]
    fn nwau_error_display() {
        let err = NwauError::ReferenceRowNotFound("801A".into());
        assert_eq!(err.to_string(), "reference row not found for DRG: 801A");
    }
}
