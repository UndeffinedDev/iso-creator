import subprocess
import shutil
import argparse
import tempfile
import sys
import zipfile
from pathlib import Path

LOG_FILE = "iso_creator.log"

def log(message):
    """Logs messages to both the terminal and a log file."""
    formatted_message = f"{message}"
    print(formatted_message)
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(formatted_message + "\n")

def check_disk_space(path, required_space=500000):
    """Checks if there is enough free disk space (in KB)."""
    total, used, free = shutil.disk_usage(path)
    if free // 1024 < required_space:
        log("Error: Insufficient disk space.")
        sys.exit(1)

def find_oscdimg():
    """Finds oscdimg.exe in the project folder."""
    exe_path = Path(__file__).parent / "oscdimg.exe"
    if exe_path.exists():
        return str(exe_path)
    log("Error: oscdimg.exe not found in project folder.")
    sys.exit(1)

def process_files(files, tmp_dir, extract_zip):
    """Processes files and directories, copying or extracting ZIPs if specified."""
    log("Processing files/directories...")
    
    for file in files:
        src = Path(file).resolve()
        dest = tmp_dir / src.stem if extract_zip and src.suffix == ".zip" else tmp_dir / src.name

        if src.is_dir():
            log(f"Processing directory: {src}")
            shutil.copytree(src, dest, dirs_exist_ok=True)
            for subfile in src.rglob("*"):
                log(f"  -> {subfile}")
        elif src.is_file():
            if extract_zip and src.suffix == ".zip":
                log(f"Processing ZIP archive: {src}")
                with zipfile.ZipFile(src, "r") as zip_ref:
                    zip_ref.extractall(tmp_dir)
                for subfile in tmp_dir.rglob("*"):  
                    log(f"  -> Extracted: {subfile}")
            else:
                log(f"Processing file: {src}")
                shutil.copy2(src, dest)
        else:
            log(f"Error: {file} not found or invalid.")
            sys.exit(1)

def create_iso(output_iso, tmp_dir, label):
    """Creates an ISO using oscdimg.exe."""
    oscdimg_path = find_oscdimg()
    log(f"Creating ISO image using {oscdimg_path}...")

    command = [
        oscdimg_path,
        f"-l{label}",   # Sin espacio entre -l y la etiqueta
        "-u2",         # O usa -u1 según tus necesidades
        str(tmp_dir),  # Carpeta de origen
        str(output_iso)  # Archivo ISO de destino
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        log(f"ISO successfully created: {output_iso}")
    else:
        log(f"Error: ISO creation failed.\nExit Code: {result.returncode}")
        sys.exit(1)

def main():
    """Main execution flow, handling arguments and execution."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--label", default="ISO_CREATION", help="Volume label.")
    parser.add_argument("-z", "--extract-zip", action="store_true", help="Extract ZIP files instead of copying them.")
    parser.add_argument("files", nargs="+", help="Files or directories to include.")
    args = parser.parse_args()

    open(LOG_FILE, "w").close()
    log("Starting script...")

    output_iso = "output.iso"
    if args.files[-1].endswith(".iso"):
        output_iso = args.files.pop()

    tmp_dir = Path(tempfile.mkdtemp())

    try:
        check_disk_space(tmp_dir)
        process_files(args.files, tmp_dir, args.extract_zip)
        create_iso(output_iso, tmp_dir, args.label)
    finally:
        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    main()