import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD as TkinterDnD2

from app.views.components.preview_frame import PDFPreviewFrame
from .components.merger_frame import MergerFrame
from .components.remover_frame import RemoverFrame
from .components.converter_frame import ConverterFrame


class MainWindow(TkinterDnD2.Tk):
    def __init__(self, default_output_path):
        self.default_output_path = default_output_path
        super().__init__()
        self.title("PDF Toolbox Pro")
        self.geometry("800x600")
        self.notebook = ttk.Notebook(self)

        self._create_widgets()
        self._create_preview_tab()
        self._configure_styles()

    def _create_widgets(self):
        # Déplacez la création du notebook dans __init__ et utilisez self.notebook
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

    def _configure_styles(self):
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TFrame", background="#f0f0f0")

    def _create_preview_tab(self):
        preview_tab = ttk.Frame(self.notebook)
        self.notebook.add(preview_tab, text="Prévisualisation PDF")

        # Contrôles de sélection
        control_frame = ttk.Frame(preview_tab)
        control_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(
            control_frame, text="Sélectionner PDF", command=self._load_preview
        ).pack(side="left")

        self.preview_frame = PDFPreviewFrame(preview_tab, self.default_output_path)
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _load_preview(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.preview_frame.load_pdf(file_path)
