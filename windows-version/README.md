# iso-creator

A Python-based tool to create ISO images from files and directories, with support for ZIP extraction, logging, and custom labels.

## 🚀 Features
- ✅ **Free!** Created as an alternative to avoid the ~870MB limit in AnyToISO's free version (not a replacement, just another option).
- ✅ **Windows & Linux compatibility** (Check the [main](https://github.com/UndeffinedDev/iso-creator/tree/main/windows-version)` branch for Linux script).
- ✅ **Create ISO images** from files and directories.
- ✅ **Support for custom** for the ISO image.
- ✅ **ZIP extraction** (optional) before adding to the ISO.
- ✅ **Dependency validation** (`oscdimg.exe` included in the `.exe` build).
- ✅ **Disk space check** to prevent errors.
- ✅ **Logging** (`iso_creator.log`) for troubleshooting.
- ✅ **Error handling** with clear messages.
- ✅ **Automatic cleanup** of temporary files.
- ✅ **User-friendly CLI options** (`-l` for label, `-z` for ZIP extraction, etc.).

## 🔧 Future Improvements
- 💡 **Support more file types.**

## ⬇️ Download
You can download the latest version from the [Releases](https://github.com/UndeffinedDev/iso-creator/releases) section on GitHub or [Dist folder](https://github.com/UndeffinedDev/iso-creator/tree/main/windows-version/dist).


## 📥 Installation
### Running the Precompiled Executable (Windows)
Download `iso-creator.exe` and run it from the command line.

### Running from Source (Python 3.7+)
Make sure you have the required dependencies:

Clone the repository:
```bash
git clone https://github.com/UndeffinedDev/iso-creator.git
cd iso-creator
python main.py file1 file2 directory1 output.iso

```

## 📥 Compilation

To compile `iso-creator` from source, you need Python 3.7+ and PyInstaller to create the executables.

### Step-by-Step Compilation

1. **Clone the repository:**
```bash
git clone https://github.com/UndeffinedDev/iso-creator.git
cd iso-creator
```

2. **Install the dependencies:** Make sure you have `PyInstaller` installed. If not, you can install it using:

`pip install pyinstaller`

3. **Compile the executable:** For Windows, run the following command to generate the `iso-creator.exe`:

```bash
pyinstaller --icon=resources/gear.ico --onefile --name=iso-creator --add-data "resources/oscdimg.exe;." main.py
```

4. Compile the graphical interface (if desired): If you want to compile the GUI version (`iso-creator-ui.exe`), use:

```bash
pyinstaller --icon=resources/gear.ico --onefile --windowed --name=iso-creator-ui --add-data "dist/iso-creator.exe;." .\ui.py
```

5. Locate your executables: After compilation, the executables will be located in the `dist` folder inside the project directory.

### Additional Notes

- The `oscdimg.exe` utility is bundled with the executable to ensure functionality.

- On Linux, you can use the `main` branch for a script-based version (see the README for more details).

## 📌 Usage
### Command Line (iso-creator.exe)
#### Basic Usage
```bash
iso-creator.exe file1 file2 directory1 output.iso
```
This creates an ISO named `output.iso` containing the specified files and directories.

#### Using a Custom Label
```bash
iso-creator.exe -l "MyCustomLabel" file1 directory1 output.iso
```
The `-l` option sets a custom label for the ISO image.

#### Extracting ZIP Files Automatically
```bash
iso-creator.exe -z my_archive.zip output.iso
```
The `-z` option extracts ZIP contents before adding them to the ISO.

#### Example Output
```
iso-creator.exe -z "musica.zip" "music.iso"

Starting script...
Processing files/directories...
Processing ZIP archive: C:\Users\Sergio\Documents\VSCode Projects\iso-creator\musica.zip
  -> Extracted: C:\Users\Sergio\AppData\Local\Temp\tmpocfl9pwv\Bailando Junto a Ti.mp3
  -> Extracted: C:\Users\Sergio\AppData\Local\Temp\tmpocfl9pwv\Chino & Nacho - Niña Bonita (Original Version).flac
  -> Extracted: C:\Users\Sergio\AppData\Local\Temp\tmpocfl9pwv\COQUETA REMIX - HEREDERO - FABIAN DJ.mp3
  -> Extracted: C:\Users\Sergio\AppData\Local\Temp\tmpocfl9pwv\Todavia.flac
  -> Extracted: C:\Users\Sergio\AppData\Local\Temp\tmpocfl9pwv\videoplayback.m4a
Creating ISO image using C:\Users\Sergio\AppData\Local\Temp\_MEI75802\oscdimg.exe...
ISO successfully created: music.iso
```

## 🖥️ Graphical Interface (iso-creator-ui.exe)
For users who prefer a GUI, `iso-creator-ui.exe` provides a simple interface to select files, set labels, and create ISOs with a few clicks.

### Running the GUI
Simply execute:
```bash
iso-creator-ui.exe
```

## ⚠️ Requirements
- **Windows:** (Tested on Windows 11 22H2 x64)
- `oscdimg.exe` (Bundled inside `iso-creator.exe`).

## 🛠️ Contributing
Feel free to submit issues or pull requests to improve the project!

## 📜 License
Copyleft (ↄ) 2025 - Free use under the terms of the GNU GPL or similar licenses.

