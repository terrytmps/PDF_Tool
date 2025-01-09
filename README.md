# PDF Management and File Conversion Tool

This project provides a tool for managing PDF files and converting files into different formats.

## Updating to a New Version of the Tool

### Modify the Source File

To make changes, update the main tool file located in `pdf_tool.py`.

### Automatically Generate the Executable for Windows

After modifying the file, double-click or run the `update.sh` script to apply the update.

### Manually Generate the Executable for Windows

### Install PyInstaller

Ensure Python is installed, then install PyInstaller by running the following command:

```bash
pip install pyinstaller
```

### Generate the Executable

Create a Windows executable with the windowed option (`--windowed`) and a custom icon (`icone.ico`):

```bash
pyinstaller --onefile --windowed --icon=icone.ico pdf_tool.py
```

After creation, the executable file will be located in the `dist/` folder under the name `pdf_tool.exe`.

## Executables for Linux

### Open a Terminal and Run the Script

```bash
./execute.sh
```

Ensure you have execution permissions for this script. If necessary, modify the permissions with the following command:

```bash
chmod +x execute.sh
```