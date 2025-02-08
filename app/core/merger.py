from PyPDF2 import PdfMerger
import os

class PdfMergerHandler:
    def merge_files(self, input_paths, output_dir):
        """
        Fusionne plusieurs fichiers PDF en un seul fichier de sortie
        """
        if not input_paths:
            raise ValueError("Aucun fichier sélectionné")
        
        output_path = self._generate_output_path(input_paths, output_dir)
        
        try:
            with PdfMerger() as merger:
                for path in input_paths:
                    if not os.path.exists(path):
                        raise FileNotFoundError(f"Fichier introuvable : {path}")
                    merger.append(path)
                
                merger.write(output_path)
            
            return output_path
        except Exception as e:
            raise RuntimeError(f"Échec de la fusion : {str(e)}")

    def _generate_output_path(self, input_paths, output_dir):
        base_names = [os.path.splitext(os.path.basename(p))[0] for p in input_paths]
        truncated_names = '_'.join([n[:15] for n in base_names[:3]])
        return os.path.join(output_dir, f"fusion_{truncated_names}.pdf")