from pdf2image import convert_from_path
from PIL import Image, ImageTk
import tempfile
import gc
import os


class PDFPreviewGenerator:
    def __init__(self, dpi=72, thumbnail_size=(200, 200), poppler_path=None):
        self.dpi = dpi
        self.thumbnail_size = thumbnail_size
        self.max_pages = int(os.environ.get("MAX_PREVIEW_PAGES", 5))

    def generate_previews(self, pdf_path, output_format="JPEG", quality=70, thread_count=2):
        """Convertit un PDF en images PIL avec gestion mémoire avancée"""
        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                thread_count=thread_count,
                use_pdftocairo=True,
                strict=False,
            )

            previews = []
            for i, img in enumerate(images):
                if i >= self.max_pages:
                    break
                previews.append(img)
            return previews
        except Exception as e:
            raise RuntimeError(f"Erreur de conversion : {str(e)}")