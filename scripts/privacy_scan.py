"""Screen added Git lines with Microsoft Presidio without displaying matched text."""

import argparse
import sys
from pathlib import PurePosixPath

from local_tool_output import read_output
from presidio_analyzer import Pattern, PatternRecognizer

RULES = {
    "CLINICAL_IDENTIFIER": (
        r"\b(?:MRN|URN|patient[ _-]*(?:id|number))"
        r"\s*[:=#,]\s*[\"']?\d{4,12}\b"
    ),
    "PRIVATE_LOCATION": (
        r"(?:/User[s]/[^/\s]+/|ClinicalResearchEvidence"
        r"/|[a-z0-9-]+-my\.sharepoint\.com/)"
    ),
    "AU_MEDICARE_CONTEXT": (
        r"\bmedicare\s*(?:number|no\.?)?"
        r"\s*[:=#,]\s*[2-6]\d{3}\s*\d{5}\s*\d\b"
    ),
}


def scan(revision):
    if revision is not None and (not revision or revision.startswith("-")):
        raise ValueError("Expected a Git revision")
    options = ["--cached"] if revision is None else [revision]
    names = (
        read_output(
            ["git", "diff", "--name-only", "-z", "--diff-filter=ACMRT", *options]
        )
        .decode()
        .split("\0")
    )
    recognizers = [
        PatternRecognizer(
            supported_entity=entity, patterns=[Pattern(entity, regex, 1.0)]
        )
        for entity, regex in RULES.items()
    ]
    findings = set()
    for name in filter(None, names):
        path = PurePosixPath(name)
        if path.suffix.lower() in {
            ".parquet",
            ".feather",
            ".dta",
            ".key",
            ".pem",
        } or any(
            part in {".private", "incoming", "ClinicalResearchEvidence"}
            for part in path.parts
        ):
            findings.add("restricted file type or directory")
        diff = read_output(
            [
                "git",
                "diff",
                "--no-ext-diff",
                "--no-textconv",
                "-U0",
                *options,
                "--",
                name,
            ]
        ).decode(errors="replace")
        if any(line.startswith("Binary files ") for line in diff.splitlines()):
            findings.add("unreviewable binary change")
        added = "\n".join(
            line[1:]
            for line in diff.splitlines()
            if line.startswith("+") and not line.startswith("+++ ")
        )
        for recognizer in recognizers:
            if recognizer.analyze(added, recognizer.supported_entities):
                findings.update(recognizer.supported_entities)
    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--revision", help="Git comparison, e.g. BASE...HEAD; default: staged"
    )
    arguments = parser.parse_args()
    issues = scan(arguments.revision)
    if issues:
        print("Privacy review required:", ", ".join(sorted(issues)), file=sys.stderr)
    sys.exit(bool(issues))
