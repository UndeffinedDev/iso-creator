# iso-creator

A Bash script to create ISO images from files and directories, with support for ZIP extraction, logging, and custom labels.

## 🚀 Features
- ✅ Free! I made this idea so as not to be limited to the ~870MB that AnyToISO allows to convert for free. (This is not a replacement, just a small alternative).
- ✅ Create ISO images from files and directories
- ✅ Support for custom labels in the ISO
- ✅ ZIP file compatibility (extract and include contents)
- ✅ Dependency validation (`mkisofs`, `unzip`, `zip`)
- ✅ Disk space check to prevent errors
- ✅ Activity logging via `iso_creator.log`
- ✅ Robust error handling with clear messages
- ✅ Automatic cleanup of temporary files
- ✅ User-friendly command-line options (`-l` for label, etc.)

## 🔧 Ideas
- 💡 Change to another language to be able to port this to Windows.
- 💡 Support more file types

## 📥 Installation
Make sure you have the required dependencies installed:

```bash
sudo apt update && sudo apt install genisoimage zip unzip
```

Clone the repository:
```bash
git clone https://github.com/yourusername/iso-creator.git
cd iso-creator
chmod +x iso-creator.sh
```

## 📌 Usage

### Basic Usage
```bash
./iso-creator.sh file1 file2 directory1 output.iso
```
This will create an ISO named `output.iso` containing the specified files and directories.

### Using a Custom Label
```bash
./iso-creator.sh -l "MyCustomLabel" file1 directory1 output.iso
```
The `-l` option sets a custom label for the ISO image.

### Example Output
```
$ ./convert_to_iso.sh -l PYTHON_EXECUTABLES Pythons.zip

Starting script...
Processing files/directories...
Processing ZIP archive: Pythons.zip
  -> Extracted: /tmp/tmp.KZiX6JNLCy/python-2.7.18.amd64.msi
  -> Extracted: /tmp/tmp.KZiX6JNLCy/python-3.4.4.amd64.msi
Creating ISO image...
I: -input-charset not specified, using utf-8 (detected in locale settings)
 21.81% done, estimate finish Fri Mar 28 22:11:33 2025
 43.62% done, estimate finish Fri Mar 28 22:11:33 2025
 65.33% done, estimate finish Fri Mar 28 22:11:33 2025
 87.14% done, estimate finish Fri Mar 28 22:11:33 2025
Total translation table size: 0
Total rockridge attributes bytes: 358
Total directory bytes: 0
Path table size(bytes): 10
Max brk space used 0
22961 extents written (44 MB)
ISO successfully created: output.iso
```

## ⚠️ Requirements
> [!NOTE]
> In some linux distributions, mkisofs is a genisoimage symbolic link, but the script still checks for either of these two commands
- Linux-based OS (Tested on Linux Mint 22.1 | Xia)
- `mkisofs` (or `genisoimage`)
- `unzip`, `zip`

## 🛠️ Contributing
Feel free to submit issues or pull requests to improve the script!

## 📜 License
Copyleft (ↄ) 2025 - Free use under the terms of the GNU GPL or similar licenses.
