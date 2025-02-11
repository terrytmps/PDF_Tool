from tkinter import ttk
from tkinterdnd2 import TkinterDnD as TkinterDnD2

from .components.preview_frame import PDFPreviewFrame
from .components.merger_frame import MergerFrame
from .components.remover_frame import RemoverFrame
from .components.converter_frame import ConverterFrame
from .components.compression_frame import CompressionFrame


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
        preview_tab = PDFPreviewFrame(self.notebook)
        self.notebook.add(preview_tab, text="Prévisualisation")

        # Onglet de compression
        compression_tab = CompressionFrame(self.notebook, self.default_output_path)
        self.notebook.add(compression_tab, text="Compression PDF")

        # Barre de contrôle
        control_frame = ttk.Frame(preview_tab)
        control_frame.pack(fill="x", padx=10, pady=10)

    def _configure_styles(self):
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TFrame", background="#f0f0f0")
