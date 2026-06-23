//! CSV/Parquet read/write utilities for episode data.
//!
//! Supports both CSV (via the `csv` crate) and Arrow/Parquet interchange
//! (via the `arrow` and `parquet` crates, gated behind `arrow-parquet` feature).

use crate::diagnostics::NwauError;
use crate::types::{EpisodeFlags, EpisodeOutput, EpisodeRow, ReferenceRow};
use std::path::Path;

#[cfg(feature = "arrow-parquet")]
use arrow::array::{Float64Array, Int64Array};
#[cfg(feature = "arrow-parquet")]
use arrow::datatypes::{DataType, Field, Schema};
#[cfg(feature = "arrow-parquet")]
use arrow::record_batch::RecordBatch;
#[cfg(feature = "arrow-parquet")]
use parquet::basic::Compression;
#[cfg(feature = "arrow-parquet")]
use parquet::file::properties::WriterProperties;
#[cfg(feature = "arrow-parquet")]
use std::fs::File;
#[cfg(feature = "arrow-parquet")]
use std::sync::Arc;

// ---------------------------------------------------------------------------
// CSV I/O
// ---------------------------------------------------------------------------

/// Write episode outputs as CSV.
pub fn write_output_csv(path: &Path, outputs: &[EpisodeOutput]) -> Result<(), NwauError> {
    let mut wtr = csv::Writer::from_path(path).map_err(|e| NwauError::IoError(e.to_string()))?;
    wtr.write_record([
        "error_code",
        "separation_category",
        "eligible_icu_hours",
        "los_icu_removed",
        "w01",
        "w02",
        "w03",
        "w04",
        "gwau",
        "private_service_deduction",
        "private_accommodation_deduction",
        "nwau",
    ])
    .map_err(|e| NwauError::IoError(e.to_string()))?;

    for out in outputs {
        wtr.write_record(&[
            out.error_code.to_string(),
            out.separation_category
                .map(|c| c.to_string())
                .unwrap_or_default(),
            out.eligible_icu_hours.to_string(),
            out.los_icu_removed.to_string(),
            out.w01.to_string(),
            out.w02.to_string(),
            out.w03.to_string(),
            out.w04.to_string(),
            out.gwau.to_string(),
            out.private_service_deduction.to_string(),
            out.private_accommodation_deduction.to_string(),
            out.nwau.to_string(),
        ])
        .map_err(|e| NwauError::IoError(e.to_string()))?;
    }

    wtr.flush().map_err(|e| NwauError::IoError(e.to_string()))?;
    Ok(())
}

/// Read episode rows from a CSV file.
pub fn read_episode_csv(path: &Path) -> Result<Vec<EpisodeRow>, NwauError> {
    let mut rdr = csv::ReaderBuilder::new()
        .trim(csv::Trim::All)
        .from_path(path)
        .map_err(|e| NwauError::IoError(e.to_string()))?;

    let mut rows = Vec::new();
    for result in rdr.deserialize() {
        let record: EpisodeRowCsv = result.map_err(|e| NwauError::FormatError(e.to_string()))?;
        rows.push(EpisodeRow {
            drg: record.drg,
            los: record.los,
            icu_hours: record.icu_hours,
            icu_other: record.icu_other,
            flags: EpisodeFlags {
                same_day: record.same_day,
                private_patient: record.private_patient,
                covid: record.covid,
                eligible_paediatric: record.eligible_paediatric,
                indigenous: record.indigenous,
                remoteness_code: record.remoteness_code,
            },
            episode_id: record.episode_id,
        });
    }
    Ok(rows)
}

/// Read reference rows from a CSV file.
pub fn read_reference_csv(path: &Path) -> Result<Vec<ReferenceRow>, NwauError> {
    let mut rdr = csv::ReaderBuilder::new()
        .trim(csv::Trim::All)
        .from_path(path)
        .map_err(|e| NwauError::IoError(e.to_string()))?;

    let mut rows = Vec::new();
    for result in rdr.deserialize() {
        let record: ReferenceRowCsv = result.map_err(|e| NwauError::FormatError(e.to_string()))?;
        rows.push(ReferenceRow {
            drg: record.drg,
            inlier_lower_bound: record.inlier_lower_bound,
            inlier_upper_bound: record.inlier_upper_bound,
            paediatric_multiplier: record.paediatric_multiplier,
            same_day_list_flag: record.same_day_list_flag,
            bundled_icu_flag: record.bundled_icu_flag,
            same_day_base_weight: record.same_day_base_weight,
            same_day_per_diem: record.same_day_per_diem,
            inlier_weight: record.inlier_weight,
            long_stay_per_diem: record.long_stay_per_diem,
            private_service_adjustment: record.private_service_adjustment,
        });
    }
    Ok(rows)
}

// ---------------------------------------------------------------------------
// Arrow / Parquet I/O  (feature = "arrow-parquet")
// ---------------------------------------------------------------------------

/// Convert episode outputs to an Arrow record batch.
#[cfg(feature = "arrow-parquet")]
pub fn outputs_to_record_batch(outputs: &[EpisodeOutput]) -> RecordBatch {
    let error_code: Int64Array = outputs.iter().map(|o| Some(o.error_code as i64)).collect();
    let separation_category: Int64Array = outputs
        .iter()
        .map(|o| o.separation_category.map(|c| c as i64))
        .collect();
    let eligible_icu_hours: Float64Array =
        outputs.iter().map(|o| Some(o.eligible_icu_hours)).collect();
    let los_icu_removed: Float64Array = outputs.iter().map(|o| Some(o.los_icu_removed)).collect();
    let w01: Float64Array = outputs.iter().map(|o| Some(o.w01)).collect();
    let w02: Float64Array = outputs.iter().map(|o| Some(o.w02)).collect();
    let w03: Float64Array = outputs.iter().map(|o| Some(o.w03)).collect();
    let w04: Float64Array = outputs.iter().map(|o| Some(o.w04)).collect();
    let gwau: Float64Array = outputs.iter().map(|o| Some(o.gwau)).collect();
    let private_service_deduction: Float64Array = outputs
        .iter()
        .map(|o| Some(o.private_service_deduction))
        .collect();
    let private_accommodation_deduction: Float64Array = outputs
        .iter()
        .map(|o| Some(o.private_accommodation_deduction))
        .collect();
    let nwau: Float64Array = outputs.iter().map(|o| Some(o.nwau)).collect();

    let schema = Schema::new(vec![
        Field::new("error_code", DataType::Int64, false),
        Field::new("separation_category", DataType::Int64, true),
        Field::new("eligible_icu_hours", DataType::Float64, false),
        Field::new("los_icu_removed", DataType::Float64, false),
        Field::new("w01", DataType::Float64, false),
        Field::new("w02", DataType::Float64, false),
        Field::new("w03", DataType::Float64, false),
        Field::new("w04", DataType::Float64, false),
        Field::new("gwau", DataType::Float64, false),
        Field::new("private_service_deduction", DataType::Float64, false),
        Field::new("private_accommodation_deduction", DataType::Float64, false),
        Field::new("nwau", DataType::Float64, false),
    ]);

    RecordBatch::try_new(
        Arc::new(schema),
        vec![
            Arc::new(error_code),
            Arc::new(separation_category),
            Arc::new(eligible_icu_hours),
            Arc::new(los_icu_removed),
            Arc::new(w01),
            Arc::new(w02),
            Arc::new(w03),
            Arc::new(w04),
            Arc::new(gwau),
            Arc::new(private_service_deduction),
            Arc::new(private_accommodation_deduction),
            Arc::new(nwau),
        ],
    )
    .expect("record batch construction must succeed")
}

/// Write episode outputs as Parquet.
#[cfg(feature = "arrow-parquet")]
pub fn write_output_parquet(path: &Path, outputs: &[EpisodeOutput]) -> Result<(), NwauError> {
    let batch = outputs_to_record_batch(outputs);
    let file = File::create(path).map_err(|e| NwauError::IoError(e.to_string()))?;

    let props = WriterProperties::builder()
        .set_compression(Compression::SNAPPY)
        .build();

    let mut writer = parquet::arrow::ArrowWriter::try_new(file, batch.schema(), Some(props))
        .map_err(|e| NwauError::IoError(e.to_string()))?;

    writer
        .write(&batch)
        .map_err(|e| NwauError::IoError(e.to_string()))?;
    writer
        .close()
        .map_err(|e| NwauError::IoError(e.to_string()))?;

    Ok(())
}

// ---------------------------------------------------------------------------
// Internal CSV deserialization helpers
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Deserialize)]
struct EpisodeRowCsv {
    drg: String,
    los: f64,
    icu_hours: f64,
    icu_other: f64,
    #[serde(default)]
    same_day: bool,
    #[serde(default)]
    private_patient: bool,
    #[serde(default)]
    covid: bool,
    #[serde(default)]
    eligible_paediatric: bool,
    #[serde(default)]
    indigenous: bool,
    #[serde(default)]
    remoteness_code: u8,
    #[serde(default)]
    episode_id: Option<String>,
}

#[derive(Debug, Clone, serde::Deserialize)]
struct ReferenceRowCsv {
    drg: String,
    inlier_lower_bound: f64,
    inlier_upper_bound: f64,
    paediatric_multiplier: f64,
    same_day_list_flag: bool,
    bundled_icu_flag: bool,
    same_day_base_weight: f64,
    same_day_per_diem: f64,
    inlier_weight: f64,
    long_stay_per_diem: f64,
    private_service_adjustment: f64,
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn write_and_verify_output_csv() {
        let dir = std::env::temp_dir();
        let path = dir.join("nwau_test_output.csv");
        let outputs = vec![EpisodeOutput {
            error_code: 0,
            separation_category: Some(3),
            eligible_icu_hours: 0.0,
            los_icu_removed: 10.0,
            w01: 9.2472,
            w02: 9.2472,
            w03: 9.2472,
            w04: 9.2472,
            gwau: 9.2472,
            private_service_deduction: 0.0,
            private_accommodation_deduction: 0.0,
            nwau: 9.2472,
        }];
        write_output_csv(&path, &outputs).unwrap();
        let content = std::fs::read_to_string(&path).unwrap();
        assert!(content.contains("nwau"));
        assert!(content.contains("9.2472"));
        std::fs::remove_file(&path).ok();
    }

    #[test]
    fn read_episode_csv_roundtrip() {
        let dir = std::env::temp_dir();
        let path = dir.join("nwau_test_episodes.csv");
        let csv_data =
            b"drg,los,icu_hours,icu_other,same_day,private_patient,covid,eligible_paediatric\n\
                         801A,10,0,0,false,false,false,false\n\
                         T63A,5,12,0,false,true,false,true\n";
        let mut f = std::fs::File::create(&path).unwrap();
        f.write_all(csv_data).unwrap();
        f.flush().unwrap();

        let rows = read_episode_csv(&path).unwrap();
        assert_eq!(rows.len(), 2);
        assert_eq!(rows[0].drg, "801A");
        assert_eq!(rows[1].drg, "T63A");
        assert!(rows[1].flags.private_patient);
        assert!(rows[1].flags.eligible_paediatric);
        std::fs::remove_file(&path).ok();
    }

    #[test]
    fn read_reference_csv_roundtrip() {
        let dir = std::env::temp_dir();
        let path = dir.join("nwau_test_reference.csv");
        let csv_data = b"drg,inlier_lower_bound,inlier_upper_bound,paediatric_multiplier,\
                          same_day_list_flag,bundled_icu_flag,same_day_base_weight,\
                          same_day_per_diem,inlier_weight,long_stay_per_diem,\
                          private_service_adjustment\n\
                         801A,7,72,1.35,false,false,0.9527,1.1849,9.2472,0.26,0.0\n";
        let mut f = std::fs::File::create(&path).unwrap();
        f.write_all(csv_data).unwrap();
        f.flush().unwrap();

        let rows = read_reference_csv(&path).unwrap();
        assert_eq!(rows.len(), 1);
        assert_eq!(rows[0].drg, "801A");
        assert!((rows[0].inlier_weight - 9.2472).abs() < 1e-4);
        std::fs::remove_file(&path).ok();
    }

    #[cfg(feature = "arrow-parquet")]
    #[test]
    fn outputs_to_record_batch_roundtrip() {
        let outputs = vec![EpisodeOutput {
            error_code: 0,
            separation_category: Some(3),
            eligible_icu_hours: 0.0,
            los_icu_removed: 10.0,
            w01: 9.2472,
            w02: 9.2472,
            w03: 9.2472,
            w04: 9.2472,
            gwau: 9.2472,
            private_service_deduction: 0.0,
            private_accommodation_deduction: 0.0,
            nwau: 9.2472,
        }];
        let batch = outputs_to_record_batch(&outputs);
        assert_eq!(batch.num_rows(), 1);
        assert_eq!(batch.num_columns(), 12);
    }
}
