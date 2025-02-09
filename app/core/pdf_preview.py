from pdf2image import convert_from_path
from PIL import Image, ImageTk
import tempfile
import gc
import os

class PDFPreviewGenerator:
    def __init__(self, dpi=72, thumbnail_size=(200, 200), poppler_path=None):
        self.dpi = dpi
        self.thumbnail_size = thumbnail_size
        self.max_pages = int(os.environ.get("MAX_PREVIEW_PAGES", 5))  # Default to 5 if not set

    def generate_previews(self, pdf_path, output_format="JPEG", quality=70, thread_count=2):
        """Convertit un PDF en vignettes avec gestion mémoire avancée"""
        temp_dir = tempfile.TemporaryDirectory()
        
        try:
            # Conversion PDF -> Images avec paramètres optimisés
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                output_folder=temp_dir.name,
                fmt=output_format.lower(),
                thread_count=thread_count,
                use_pdftocairo=True,
                strict=False,
                jpegopt={"quality": quality, "progressive": True},
            )

            previews = []
            for i, img in enumerate(images):
                if i >= self.max_pages:
                    break
                    
                # Réduction progressive de la taille
                img.thumbnail(
                    self.thumbnail_size,
                    resample=Image.Resampling.LANCZOS
                )
                
                # Conversion pour Tkinter
                photo_img = ImageTk.PhotoImage(img)
                previews.append(photo_img)
                
                # Nettoyage mémoire explicite
                del img
                gc.collect()

            return previews

        except Exception as e:
            raise RuntimeError(f"Erreur de conversion : {str(e)}")
        
        finally:
            temp_dir.cleanup()