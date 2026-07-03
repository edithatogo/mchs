//! Coding-set and classification registries.
//!
//! These are synthetic (no real IHACPA data) lookup tables used to validate
//! inputs and classify episodes.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// A registry of DRG codes with metadata.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DrgRegistry {
    /// Map from DRG code to its metadata.
    entries: HashMap<String, DrgEntry>,
}

/// Metadata associated with a single DRG code.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DrgEntry {
    /// DRG code.
    pub code: String,
    /// Whether this DRG is in scope for acute pricing.
    pub acute_in_scope: bool,
    /// Whether this DRG is on the same-day list.
    pub same_day_list: bool,
    /// Whether ICU hours are bundled for this DRG.
    pub bundled_icu: bool,
}

impl DrgRegistry {
    /// Create an empty registry.
    pub fn new() -> Self {
        Self {
            entries: HashMap::new(),
        }
    }

    /// Insert a DRG entry.
    pub fn insert(&mut self, entry: DrgEntry) {
        self.entries.insert(entry.code.clone(), entry);
    }

    /// Look up a DRG code.
    pub fn get(&self, code: &str) -> Option<&DrgEntry> {
        self.entries.get(code)
    }

    /// Return true if the DRG code is registered and in scope for acute pricing.
    pub fn is_acute_in_scope(&self, code: &str) -> bool {
        self.entries.get(code).is_some_and(|e| e.acute_in_scope)
    }

    /// Return all registered DRG codes.
    pub fn codes(&self) -> Vec<&str> {
        self.entries.keys().map(|s| s.as_str()).collect()
    }

    /// Populate with the synthetic acute 2025 fixture DRGs.
    pub fn with_acute_2025_fixtures(mut self) -> Self {
        for (code, same_day, bundled) in &[
            ("801A", false, false),
            ("T63A", false, false),
            ("T63B", false, false),
            ("AAA", false, false),
            ("BBB", true, true),
        ] {
            self.insert(DrgEntry {
                code: code.to_string(),
                acute_in_scope: true,
                same_day_list: *same_day,
                bundled_icu: *bundled,
            });
        }
        self
    }
}

impl Default for DrgRegistry {
    fn default() -> Self {
        Self::new()
    }
}

/// A registry of separation mode codes.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SeparationModeRegistry {
    entries: HashMap<String, SeparationModeEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SeparationModeEntry {
    pub code: String,
    pub label: String,
    pub is_acute: bool,
}

impl SeparationModeRegistry {
    /// Create an empty registry.
    pub fn new() -> Self {
        Self {
            entries: HashMap::new(),
        }
    }

    /// Insert a separation mode entry.
    pub fn insert(&mut self, entry: SeparationModeEntry) {
        self.entries.insert(entry.code.clone(), entry);
    }

    /// Look up a separation mode code.
    pub fn get(&self, code: &str) -> Option<&SeparationModeEntry> {
        self.entries.get(code)
    }

    /// Return true if the separation mode is acute.
    pub fn is_acute(&self, code: &str) -> bool {
        self.entries.get(code).is_some_and(|e| e.is_acute)
    }
}

impl Default for SeparationModeRegistry {
    fn default() -> Self {
        let mut reg = Self::new();
        for (code, label, acute) in &[
            ("1", "Admitted – acute", true),
            ("2", "Admitted – non-acute", false),
            ("3", "Admitted – newborn", true),
            ("4", "Admitted – other", false),
        ] {
            reg.insert(SeparationModeEntry {
                code: code.to_string(),
                label: label.to_string(),
                is_acute: *acute,
            });
        }
        reg
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn drg_registry_acute_fixtures() {
        let reg = DrgRegistry::new().with_acute_2025_fixtures();
        assert!(reg.is_acute_in_scope("801A"));
        assert!(reg.is_acute_in_scope("T63A"));
        assert!(!reg.is_acute_in_scope("ZZZZ"));
    }

    #[test]
    fn drg_registry_bbb_has_bundled_icu() {
        let reg = DrgRegistry::new().with_acute_2025_fixtures();
        let entry = reg.get("BBB").unwrap();
        assert!(entry.same_day_list);
        assert!(entry.bundled_icu);
    }

    #[test]
    fn separation_mode_registry_defaults() {
        let reg = SeparationModeRegistry::default();
        assert!(reg.is_acute("1"));
        assert!(!reg.is_acute("2"));
        assert!(!reg.is_acute("99"));
    }
}
