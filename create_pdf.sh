#!/bin/bash

# Créer le dossier pdf s'il n'existe pas
mkdir -p pdf

# Liste des fichiers texte à convertir
texte_files=("fichier1.txt" "fichier2.txt" "fichier3.txt")

# Créer des fichiers texte avec du contenu fictif
for file in "${texte_files[@]}"; do
    echo "Ceci est le contenu du $file" > "$file"
done

# Convertir chaque fichier texte en PDF et le déplacer dans le dossier pdf
for file in "${texte_files[@]}"; do
    # Nom du fichier PDF de sortie
    pdf_file="pdf/${file%.txt}.pdf"

    # Convertir le fichier texte en HTML, puis en PDF
    cat "$file" | wkhtmltopdf - "$pdf_file"

    echo "Fichier $file converti en $pdf_file"
done

echo "Conversion terminée. Les fichiers PDF sont dans le dossier pdf."
