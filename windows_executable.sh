#!/bin/bash
# Installer les dépendances nécessaires
echo "Installation des dépendances nécessaires..."
pip install tkinterdnd2 pillow pillow-heif PyPDF2 pyinstaller

# Vérifier si le fichier python existe
if [ ! -f "pdf_tool.py" ]; then
    echo "Le fichier 'pdf_tool.py' est introuvable dans le répertoire actuel."
    exit 1
fi

# Vérifier si l'icône existe
if [ ! -f "assets/icone.ico" ]; then
    echo "Le fichier 'icone.ico' est introuvable dans le répertoire actuel."
    exit 1
fi

# Générer l'exécutable
echo "Création de l'exécutable avec PyInstaller..."
pyinstaller --onefile --windowed --icon=assets/icone.ico app/main.py

# Vérifier si la création a réussi
if [ $? -eq 0 ]; then
    echo "L'exécutable a été généré avec succès dans le dossier 'dist/'."
else
    echo "Une erreur est survenue lors de la génération de l'exécutable."
    exit 1
fi

# Fin
echo "Terminé !"
