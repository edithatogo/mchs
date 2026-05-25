#!/usr/bin/env bash
set -euo pipefail

version="${1:-0.1.0}"
out_dir="${2:-dist}"
archive="nwau-c-abi-${version}-source.tar.gz"
staging="$(mktemp -d)"
trap 'rm -rf "$staging"' EXIT

root="nwau-c-abi-${version}"
mkdir -p "$staging/$root/rust/crates"

cp LICENSE "$staging/$root/LICENSE"
cp rust/Cargo.toml "$staging/$root/rust/Cargo.toml"
cp rust/Cargo.lock "$staging/$root/rust/Cargo.lock"
cp -R rust/crates/nwau-core "$staging/$root/rust/crates/nwau-core"
cp -R rust/crates/nwau-c-abi "$staging/$root/rust/crates/nwau-c-abi"
cp -R rust/crates/nwau-py "$staging/$root/rust/crates/nwau-py"

find "$staging/$root" -name target -prune -o -name .git -prune -o -type f -print0 |
  xargs -0 touch -t 202605260000.00

mkdir -p "$out_dir"
(
  cd "$staging"
  find "$root" -type f | LC_ALL=C sort > "$staging/file-list.txt"
  COPYFILE_DISABLE=1 tar -czf "$out_dir/$archive" -T "$staging/file-list.txt"
)

sha256="$(shasum -a 256 "$out_dir/$archive" | awk '{print $1}')"
sha512="$(shasum -a 512 "$out_dir/$archive" | awk '{print $1}')"
bytes="$(wc -c < "$out_dir/$archive" | tr -d ' ')"

cat <<EOF
archive=$out_dir/$archive
bytes=$bytes
sha256=$sha256
sha512=$sha512
EOF
