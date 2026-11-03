"""Import pinned official acute pricing ALOS sources into the MCHS benchmark CSV."""

import argparse
import csv
import hashlib
import json
import math
import re
import tempfile
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from local_tool_output import read_output
from openpyxl import load_workbook
from pyxlsb import open_workbook

MANIFEST = Path(__file__).with_name("ihacpa_pricing_alos_sources.json")
DRG = re.compile(r"[A-Z0-9][0-9]{2}[A-Z]")


def workbook_rows(path):
    if path.suffix == ".zip":
        with ZipFile(path) as archive:
            members = [
                n for n in archive.namelist() if "/" not in n and n.endswith(".xlsb")
            ]
            if len(members) != 1:
                raise ValueError("Expected one root XLSB")
            with (
                open_workbook(BytesIO(archive.read(members[0]))) as book,
                book.get_sheet("Admitted Acute") as sheet,
            ):
                return [[cell.v for cell in row] for row in sheet.rows()]
    book = load_workbook(path, read_only=True, data_only=True)
    try:
        return list(book["Admitted Acute"].values)
    finally:
        book.close()


def extract_workbook(path, edition):
    rows = workbook_rows(path)
    for i, row in enumerate(rows):
        headers = [str(value).strip() for value in row]
        if f"AR-DRG V{edition}" in headers:
            code = headers.index(f"AR-DRG V{edition}")
            (alos,) = [j for j, h in enumerate(headers) if h.startswith("ALOS")]
            return [
                (str(r[code]).strip(), r[alos])
                for r in rows[i + 1 :]
                if DRG.fullmatch(str(r[code]).strip())
            ]
    raise ValueError(f"No acute ALOS header for edition {edition}")


def extract_legacy_pdf(path, edition):
    """Pinned 2014/2015 acute pages repeat a column-aligned ALOS heading."""
    text = read_output(["pdftotext", "-layout", str(path.resolve()), "-"]).decode()
    if not re.search(r"AR-DRG\s+V\s*" + re.escape(edition), text, re.I):
        raise ValueError("Unexpected historical edition")
    rows = []
    for page in text.split("\f"):
        lines = page.splitlines()
        headers = [line.index("ALOS") for line in lines if line.strip() == "ALOS"]
        if not headers:
            continue
        for line in lines:
            match = re.match(r"^ *([A-Z0-9][0-9]{2}[A-Z])\b", line)
            if match:
                (value,) = [
                    m.group()
                    for m in re.finditer(r"\b\d+\.\d\b", line)
                    if abs(m.start() - headers[0]) <= 8
                ]
                rows.append((match[1], float(value)))
    return rows


def import_series(source_dir, output):
    records = []
    for year, spec in json.loads(MANIFEST.read_text()).items():
        if spec["check_801B"] is None:
            continue  # The acute price tables for these years have no ALOS field.
        path = source_dir / spec["filename"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != spec["sha256"]:
            raise ValueError(f"{year}: source checksum differs")
        extract = extract_legacy_pdf if path.suffix == ".pdf" else extract_workbook
        rows = extract(path, spec["edition"])
        values = dict(rows)
        if len(rows) != len(values) or values.get("801B") != spec["check_801B"]:
            raise ValueError(f"{year}: duplicate DRG or determination control mismatch")
        blank = 0
        for code, days in sorted(rows):
            if days is None:
                blank += 1
                continue
            if (
                not isinstance(days, (int, float))
                or not math.isfinite(days)
                or days <= 0
            ):
                raise ValueError(f"{year}: invalid ALOS for {code}: {days!r}")
            records.append(
                ("pricing_alos", year, spec["edition"], code, days, spec["url"])
            )
        print(
            year,
            spec["edition"],
            len(rows) - blank,
            "published values;",
            blank,
            "unavailable",
        )
    with tempfile.NamedTemporaryFile(
        mode="w", dir=output.parent, delete=False, newline=""
    ) as stream:
        path = Path(stream.name)
        writer = csv.writer(stream)
        writer.writerow(
            ("kind", "start_year", "edition", "stratum", "expected_days", "source")
        )
        writer.writerows(records)
    path.replace(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    import_series(args.source_dir, args.output)
