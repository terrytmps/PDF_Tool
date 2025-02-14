# PDF Management and File Conversion Tool

A comprehensive desktop application for managing PDF files and converting between popular image formats.

![Application Preview](assets/preview.png)

## Key Features

- **PDF Operations**
  - Merge multiple PDF files
  - Remove specific pages from PDFs
  - Preview document before applying changes
  - Compress PDFs (High/Medium/Low quality)
  - Rotate pages with visual preview

- **File Conversion**
  - Supported input formats: PDF, HEIC, JPEG, JPG, PNG
  - Supported output formats: PNG, JPEG, JPG, HEIC

- **User Interface**
  - Interactive preview of rotations and page deletions
  - Progress indicators for long-running operations
  - Preset configuration profiles for common workflows

## Future Roadmap

- AI-powered PDF summarization
- Custom default save directory configuration
- Batch processing capabilities
- Cloud storage integration

## Prerequisites

**System Requirements :**
- **Poppler Utilities** (v24.08.0+)
  - Linux: `poppler-utils` package
  - Windows: [Download installer](https://poppler.freedesktop.org/)
  
- **Ghostscript** (v9.50+)
  - Linux: `ghostscript` package
  - Windows: [Download installer](https://www.ghostscript.com/)

**Python Requirements :**
- Python 3.8+
- PIP package manager


## Installation on Linux/Debian Systems
```bash
# Install system dependencies
sudo apt install poppler-utils ghostscript

# Install Python requirements
pip install -r requirements.txt

# Launch application
python3 -m main
```

## Installation on Windows Systems

1. Install [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Install [Ghostscript](https://www.ghostscript.com/releases/gsdnld.html)
3. Add both to system PATH
4. Choose installation method:

**Option 1: Python Environment**
```bat
pip install -r requirements.txt
executer_pdf_tool.bat
```

**Option 2: Standalone Executable**

```bash
# Build executable using PyInstaller
pyinstaller --onefile --windowed main.py

# Resulting executable will be in dist/main.exe
```

## Configuration

Le fichier `.env` permet de personnaliser le comportement de l'application. Créez-le à la racine du projet avec ces paramètres :

```ini
# Maximum de pages à prévisualiser
MAX_PREVIEW_PAGES=50

# Dossier de sauvegarde par défaut (utiliser le chemin absolu)
OUTPUT_DIR="~/Desktop"

# Longueur maximale des noms de fichier
MAX_FILENAME_CHARS=50
```

## Project Structure

```bash
.
├── assets/                  # GUI assets and icons
├── pdf/                    # Sample PDFs for testing
├── src/                    # Application source code
│   ├── conversion.py       # File conversion logic
│   ├── pdf_operations.py   # PDF manipulation functions
│   └── gui.py              # User interface components
├── requirements.txt        # Python dependencies
├── Makefile                # Linux build automation
├── pdf_tool.spec           # PyInstaller configuration
└── windows_executable.bat  # Windows build script
```

## Development

Contribution guidelines:

1. Fork the repository
2. Create feature branch: git checkout -b feature/new-feature
3. Commit changes following Conventional Commits
4. Push to branch and open a Pull Request