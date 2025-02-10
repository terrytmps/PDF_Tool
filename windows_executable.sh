#!/bin/bash
# Créer et activer un environnement virtuel
echo "Création de l'environnement virtuel..."
python -m venv venv

echo "Activation de l'environnement virtuel..."
venv\Scripts\activate

# Installer les dépendances nécessaires
echo "Installation des dépendances nécessaires..."
pip install -r requirements.txt

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

# Vérifier si le dossier 'dist' existe
if [ -f "dist/main.exe" ]; then
    echo "Suppression de l'ancien exécutable..."
    rm dist/main.exe
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

# Désactiver l'environnement virtuel
echo "Désactivation de l'environnement virtuel..."
deactivate

# Fin
echo "Terminé !"
