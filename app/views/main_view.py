from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD as TkinterDnD2
from PyPDF2 import PdfReader, PdfWriter

from app.views.components.preview_frame import PDFPreviewFrame
from .components.merger_frame import MergerFrame
from .components.remover_frame import RemoverFrame
from .components.converter_frame import ConverterFrame


class MainWindow(TkinterDnD2.Tk):
    def __init__(self, default_output_path):
        super().__init__()
        self.title("PDF Toolbox Pro")
        self.geometry("800x600")
        self.default_output_path = default_output_path
        self._create_widgets()
        self._configure_styles()

    def _create_widgets(self):
        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Onglet Fusion PDF
        merger_tab = MergerFrame(self.notebook, self.default_output_path)
        self.notebook.add(merger_tab, text="Fusion PDF")

        # Onglet Suppression Pages
        remover_tab = RemoverFrame(self.notebook, self.default_output_path)
        self.notebook.add(remover_tab, text="Suppression Pages")

        # Onglet Conversion
        converter_tab = ConverterFrame(self.notebook, self.default_output_path)
        self.notebook.add(converter_tab, text="Conversion Fichiers")

        # Onglet de prévisualisation
        preview_tab = ttk.Frame(self.notebook)
        self.notebook.add(preview_tab, text="Prévisualisation")

        # Barre de contrôle
        control_frame = ttk.Frame(preview_tab)
        control_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(control_frame, text="Ouvrir PDF", command=self._load_pdf).pack(
            side="left"
        )

        ttk.Button(control_frame, text="Télécharger PDF", command=self._save_pdf).pack(
            side="left", padx=10
        )

        # Prévisualisation
        self.preview_frame = PDFPreviewFrame(preview_tab, self.default_output_path)
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _configure_styles(self):
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TFrame", background="#f0f0f0")

    def _load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.preview_frame.load_pdf(file_path)

    def _save_pdf(self):
        if not self.preview_frame.current_pdf_path:
            messagebox.showerror("Erreur", "Aucun PDF sélectionné")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
        )
        if not output_path:
            return

        try:
            # Appliquer les rotations et supprimer les pages sélectionnées
            reader = PdfReader(self.preview_frame.current_pdf_path)
            writer = PdfWriter()

            # Ne plus utiliser selected_indices ici

            # Itérer sur les pages conservées dans self.page_frames
            for page_data in self.preview_frame.page_frames:
                original_page_index = page_data["original_index"]
                original_page = reader.pages[
                    original_page_index
                ]  # Récupérer la page originale avec l'index original

                rotation = page_data["rotation"]
                original_page.rotate(rotation % 360)
                writer.add_page(
                    original_page
                )  # Ajouter la page originale (rotatée) au writer

            # Sauvegarde
            with open(output_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Succès", "PDF sauvegardé avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de sauvegarde : {str(e)}")
