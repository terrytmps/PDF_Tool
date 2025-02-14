import os
import shutil
import subprocess
from pathlib import Path

class FileCompressor:
    def __init__(self):
        # Détermine le nom de l'exécutable Ghostscript selon l'OS
        self.gs_executable = "gswin64c" if os.name == "nt" else "gs"
        
        if not shutil.which(self.gs_executable):
            raise SystemExit(
                f"Erreur: Ghostscript ({self.gs_executable}) n'est pas installé ou n'est pas dans le PATH.\n"
                "Voir https://www.ghostscript.com/ pour l'installation.\n"
                "Sur Windows, vérifiez que le nom de l'exécutable est bien gswin64c.exe"
            )

    def compress_files(self, input_files, output_path, compression_level="good"):
        compressed_files = []
        gs_presets = {
            "less": "/screen",
            "good": "/ebook",
            "high": "/prepress"
        }
        preset = gs_presets.get(compression_level, "/ebook")

        for input_file in input_files:
            try:
                os.makedirs(output_path, exist_ok=True)
                
                # Génération du chemin POSIX
                base_name = Path(input_file).stem
                output_filepath = Path(output_path) / f"{base_name}_compressed.pdf"
                
                # Conversion des chemins en format slash
                gs_command = [
                    self.gs_executable,
                    '-q',
                    '-sDEVICE=pdfwrite',
                    '-dCompatibilityLevel=1.4',
                    f'-dPDFSETTINGS={preset}',
                    '-dNOPAUSE',
                    '-dBATCH',
                    f'-sOutputFile={output_filepath.as_posix()}',
                    Path(input_file).as_posix()
                ]

                subprocess.run(gs_command, check=True, capture_output=True)
                compressed_files.append(output_filepath.as_posix())
            
            except subprocess.CalledProcessError as e:
                print(f"Erreur Ghostscript ({e.returncode}) : {e.stderr.decode()}")
            except Exception as e:
                print(f"Erreur avec {input_file} : {str(e)}")
        
        return compressed_files
