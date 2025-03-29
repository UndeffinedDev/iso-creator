#!/bin/bash

# Copyleft (ↄ) 2025 - Free use under the terms of the GNU GPL or similar licenses

set -e

log_file="iso_creator.log"
> "$log_file"

echo "Starting script..." | tee -a "$log_file"

# Verificar si mkisofs o genisoimage están disponibles
if command -v mkisofs &> /dev/null; then
    iso_cmd="mkisofs"
elif command -v genisoimage &> /dev/null; then
    iso_cmd="genisoimage"
else
    echo "Error: Neither mkisofs nor genisoimage is installed. Please install one before running the script." | tee -a "$log_file"
    exit 1
fi

# Verificar la existencia de otros comandos necesarios
for cmd in unzip zip; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: $cmd is not installed. Please install it before running the script." | tee -a "$log_file"
        exit 1
    fi
done

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 [-l label] <file1/directory1> [<file2/directory2> ...] [output.iso]" | tee -a "$log_file"
    exit 1
fi

label="ISO_CREATION"
while getopts "l:" opt; do
    case "$opt" in
        l) label="$OPTARG" ;;
        *) echo "Invalid option" | tee -a "$log_file"; exit 1 ;;
    esac
done
shift $((OPTIND -1))

if [[ "${!#}" == *.iso ]]; then
    output_iso="${!#}"
    set -- "${@:1:$(($#-1))}"
else
    output_iso="output.iso"
fi

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

disk_space=$(df --output=avail "$tmp_dir" | tail -n 1)
if (( disk_space < 500000 )); then
    echo "Error: Insufficient disk space." | tee -a "$log_file"
    exit 1
fi

echo "Processing files/directories..." | tee -a "$log_file"
for file in "$@"; do
    if [ -d "$file" ]; then
        echo "Processing directory: $file" | tee -a "$log_file"
        cp -r "$file" "$tmp_dir" || { echo "Error copying directory $file" | tee -a "$log_file"; exit 1; }
        find "$file" -type f | while read -r subfile; do
            echo "  -> $subfile" | tee -a "$log_file"
        done
    elif [[ "$file" == *.zip ]]; then
        echo "Processing ZIP archive: $file" | tee -a "$log_file"
        unzip -q "$file" -d "$tmp_dir" || { echo "Error extracting $file" | tee -a "$log_file"; exit 1; }
        find "$tmp_dir" -type f | while read -r subfile; do
            echo "  -> Extracted: $subfile" | tee -a "$log_file"
        done
    elif [ -f "$file" ]; then
        echo "Processing file: $file" | tee -a "$log_file"
        zip_name="${file}.zip"
        zip -r "$zip_name" "$file" || { echo "Error compressing $file" | tee -a "$log_file"; exit 1; }
        unzip -q "$zip_name" -d "$tmp_dir" || { echo "Error extracting $zip_name" | tee -a "$log_file"; exit 1; }
        echo "  -> Compressed and extracted: $file" | tee -a "$log_file"
    else
        echo "Error: $file not found or invalid." | tee -a "$log_file"
        exit 1
    fi
done

echo "Creating ISO image using $iso_cmd..." | tee -a "$log_file"
$iso_cmd -J -r -iso-level 3 -V "$label" -o "$output_iso" "$tmp_dir" || { echo "Error creating ISO" | tee -a "$log_file"; exit 1; }

echo "ISO successfully created: $output_iso" | tee -a "$log_file"