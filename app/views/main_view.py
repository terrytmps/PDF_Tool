import tkinter as tk
from tkinter import ttk
from .components.merger_frame import MergerFrame
from .components.remover_frame import RemoverFrame
from .components.converter_frame import ConverterFrame


class MainWindow(tk.Tk):
    def __init__(self, default_output_path):
        super().__init__()
        self.title("PDF Toolbox Pro")
        self.geometry("800x600")
        self.default_output_path = default_output_path

        self._create_widgets()
        self._configure_styles()

    def _create_widgets(self):
        notebook = ttk.Notebook(self)

        # Onglet Fusion PDF
        merger_tab = MergerFrame(notebook, self.default_output_path)
        notebook.add(merger_tab, text="Fusion PDF")

        # Onglet Suppression Pages
        remover_tab = RemoverFrame(notebook, self.default_output_path)
        notebook.add(remover_tab, text="Suppression Pages")

        # Onglet Conversion
        converter_tab = ConverterFrame(notebook, self.default_output_path)
        notebook.add(converter_tab, text="Conversion Fichiers")

        notebook.pack(expand=True, fill="both", padx=10, pady=10)

    def _configure_styles(self):
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TFrame", background="#f0f0f0")
