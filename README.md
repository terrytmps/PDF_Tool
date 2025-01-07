# Dossier pour l'outil de gestion PDF et conversion de fichiers

## Mettre à jour vers une nouvelle version de l'outil

1. Modifier le fichier `pdf_tool.py`.
2. Double-cliquer sur `update.sh`.

### Ou

1. Installer PyInstaller :
    ```sh
    pip install pyinstaller
    ```
2. Créer un exécutable :
    ```sh
    pyinstaller --onefile --windowed --icon=icone.ico pdf_tool.py
    ```

Le fichier exécutable se trouve dans `dist/pdf_tool.exe`.