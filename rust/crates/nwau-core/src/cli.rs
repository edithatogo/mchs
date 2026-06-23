//! CLI argument parsing and command dispatch for the NWAU Rust core.

use clap::{Parser, Subcommand};

/// Command-line interface for the NWAU Rust calculator.
#[derive(Parser, Debug)]
#[command(name = "nwau", version, about = "NWAU Rust Calculator")]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

/// Available subcommands.
#[derive(Subcommand, Debug)]
pub enum Command {
    /// Calculate NWAU for episodes from an input file.
    Calculate {
        /// Path to the episode input file (CSV).
        #[arg(short = 'i', long)]
        input: String,

        /// Path to the reference file (CSV).
        #[arg(short = 'r', long)]
        reference: String,

        /// Path for the output file (CSV).
        #[arg(short = 'o', long, default_value = "output.csv")]
        output: String,

        /// Calculator label (e.g. "acute-2025").
        #[arg(short = 'c', long, default_value = "acute-2025")]
        calculator: String,

        /// ICU hourly rate.
        #[arg(long, default_value = "0.0")]
        icu_rate: f64,

        /// Pricing year.
        #[arg(short = 'y', long, default_value_t = 2025)]
        year: u16,

        /// Number of rows to limit processing (optional, for testing).
        #[arg(short = 'n', long)]
        limit: Option<usize>,
    },

    /// List available calculators.
    ListCalculators,

    /// Print version and kernel information.
    Info,

    /// Validate an input file against the registry.
    Validate {
        /// Path to the input file (CSV).
        #[arg(short = 'i', long)]
        input: String,
    },
}

impl Cli {
    /// Parse CLI arguments from `std::env::args()`.
    pub fn parse_from_env() -> Self {
        <Self as Parser>::parse()
    }

    /// Return a short description of the CLI purpose.
    pub fn description() -> &'static str {
        "NWAU Rust Calculator — synthetic acute 2025 proof of concept"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_calculate_command() {
        let cli = Cli::try_parse_from([
            "nwau",
            "calculate",
            "-i",
            "episodes.csv",
            "-r",
            "reference.csv",
            "-o",
            "out.csv",
        ])
        .expect("should parse calculate");

        match cli.command {
            Command::Calculate {
                input,
                reference,
                output,
                ..
            } => {
                assert_eq!(input, "episodes.csv");
                assert_eq!(reference, "reference.csv");
                assert_eq!(output, "out.csv");
            }
            _ => panic!("expected Calculate command"),
        }
    }

    #[test]
    fn parse_list_calculators() {
        let cli = Cli::try_parse_from(["nwau", "list-calculators"])
            .expect("should parse list-calculators");
        assert!(matches!(cli.command, Command::ListCalculators));
    }

    #[test]
    fn parse_info() {
        let cli = Cli::try_parse_from(["nwau", "info"]).expect("should parse info");
        assert!(matches!(cli.command, Command::Info));
    }
}
