import os
import subprocess
import shutil


class FileCompressor:
    def __init__(self):
        if not shutil.which("gs"):
            raise SystemExit(
                "Erreur: Ghostscript (gs) n'est pas installé ou n'est pas dans le PATH.\n"
                "Voir https://www.ghostscript.com/ pour l'installation."
            )

    def compress_files(self, input_files, output_path, compression_level="good"):
        compressed_files = []
        # Associe les niveaux de compression aux paramètres Ghostscript
        gs_presets = {
            "less": "/screen",  # Compression élevée (qualité réduite)
            "good": "/ebook",  # Compression équilibrée
            "high": "/prepress",  # Qualité maximale (compression minimale)
        }
        preset = gs_presets.get(compression_level, "/ebook")

        for input_file in input_files:
            try:
                # Crée le dossier de sortie si nécessaire
                os.makedirs(output_path, exist_ok=True)

                # Génère le nom du fichier de sortie
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_filename = f"{base_name}_compressed.pdf"
                output_filepath = os.path.join(output_path, output_filename)

                # Construction de la commande Ghostscript
                gs_command = [
                    "gs",
                    "-q",  # Mode silencieux
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.4",
                    f"-dPDFSETTINGS={preset}",
                    "-dNOPAUSE",
                    "-dBATCH",
                    f"-sOutputFile={output_filepath}",
                    input_file,
                ]

                # Exécute la commande
                subprocess.run(gs_command, check=True)
                compressed_files.append(output_filepath)

            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de la compression de {input_file} : {e}")
            except Exception as e:
                print(f"Erreur inattendue avec {input_file} : {e}")

        return compressed_files
