from PIL import Image
import pillow_heif
import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path


class FileConverter:
    SUPPORTED_INPUT = {
        "image": [".png", ".jpg", ".jpeg", ".heic", ".HEIC"],
        "pdf": [".pdf"],
    }

    def convert_files(self, input_paths, output_format, output_dir):
        """
        Convertit des fichiers entre différents formats
        """
        results = []

        for path in input_paths:
            try:
                ext = os.path.splitext(path)[1].lower()

                if ext in self.SUPPORTED_INPUT["image"]:
                    results.append(self._convert_image(path, output_format, output_dir))
                elif ext == ".pdf":
                    results.extend(self._convert_pdf(path, output_format, output_dir))
                else:
                    raise ValueError(f"Format non supporté : {ext}")
            except Exception as e:
                raise RuntimeError(f"Erreur avec {os.path.basename(path)} : {str(e)}")

        return results

    def _convert_image(self, input_path, output_format, output_dir):
        # Gestion spéciale pour HEIC
        if input_path.lower().endswith((".heic", ".HEIC")):
            pillow_heif.register_heif_opener()

        with Image.open(input_path) as img:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}.{output_format}")
            img.save(output_path)
            return output_path

    def _convert_pdf(self, input_path, output_format, output_dir):
        if output_format not in ["png", "jpeg"]:
            raise ValueError("Conversion PDF uniquement vers PNG/JPEG")

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        pages = convert_from_path(input_path)
        outputs = []

        for i, page in enumerate(pages, 1):
            output_path = os.path.join(
                output_dir, f"{base_name}_page{i}.{output_format}"
            )
            page.save(output_path, output_format.upper())
            outputs.append(output_path)

        return outputs
