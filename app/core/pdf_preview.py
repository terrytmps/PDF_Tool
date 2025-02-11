from pdf2image import convert_from_path
import os


class PDFPreviewGenerator:
    def __init__(self, dpi=72, thumbnail_size=(200, 200), poppler_path=None):
        self.dpi = dpi
        self.thumbnail_size = thumbnail_size
        self.max_pages = int(os.environ.get("MAX_PREVIEW_PAGES", 5))

    def generate_previews(self, pdf_path):
        """Convertit un PDF en images PIL"""
        try:
            return convert_from_path(
                pdf_path,
                dpi=self.dpi,
                thread_count=2,
                use_pdftocairo=True,
                strict=False,
            )[: self.max_pages]
        except Exception as e:
            raise RuntimeError(f"Erreur de conversion : {str(e)}")
