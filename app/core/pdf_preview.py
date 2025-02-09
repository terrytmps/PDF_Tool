from pdf2image import convert_from_path
from PIL import Image, ImageTk
import tempfile
import os


class PDFPreviewGenerator:
    def __init__(self, dpi=100, thumbnail_size=(200, 200)):
        self.dpi = dpi
        self.thumbnail_size = thumbnail_size
        self.temp_dir = tempfile.TemporaryDirectory()

    def generate_previews(self, pdf_path):
        """Convertit un PDF en vignettes d'images"""
        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                output_folder=self.temp_dir.name,
                fmt="png",
                thread_count=4,
            )

            previews = []
            for i, img in enumerate(images):
                img.thumbnail(self.thumbnail_size)
                previews.append(ImageTk.PhotoImage(img))
            return previews
        except Exception as e:
            raise RuntimeError(f"Erreur de conversion PDF : {str(e)}")
        finally:
            self.temp_dir.cleanup()
