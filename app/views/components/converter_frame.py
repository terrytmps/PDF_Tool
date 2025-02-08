import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.core.converter import FileConverter

class ConverterFrame(ttk.Frame):
    FORMATS = [("PNG", "png"), ("JPEG", "jpeg"), ("PDF", "pdf")]

    def __init__(self, parent, output_path):
        super().__init__(parent)
        self.output_path = output_path
        self.converter = FileConverter()
        self._create_widgets()

    def _create_widgets(self):
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Sélection du format
        self.format_var = tk.StringVar(value="png")
        format_frame = ttk.Frame(self)
        format_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        for text, value in self.FORMATS:
            ttk.Radiobutton(
                format_frame,
                text=text,
                value=value,
                variable=self.format_var
            ).pack(side="left", padx=10)

        # Bouton de conversion
        ttk.Button(
            self, 
            text="Choisir des fichiers à convertir", 
            style="Accent.TButton", 
            command=self._convert_files
        ).grid(row=1, column=0, pady=10, padx=10, sticky="ew")

    def _convert_files(self):
        input_files = filedialog.askopenfilenames(
            title="Sélectionnez des fichiers à convertir",
            filetypes=[
                ("Tous les formats", "*.heic;*.HEIC;*.png;*.jpg;*.jpeg;*.pdf"),
                ("Images", "*.heic;*.HEIC;*.png;*.jpg;*.jpeg"),
                ("PDF", "*.pdf")
            ]
        )
        if not input_files:
            return

        try:
            output_format = self.format_var.get()
            results = self.converter.convert_files(
                input_files, 
                output_format, 
                self.output_path
            )
            
            messagebox.showinfo(
                "Conversion terminée",
                f"{len(results)} fichiers convertis avec succès!\n" +
                f"Emplacement : {self.output_path}",
                parent=self
            )
        except Exception as e:
            messagebox.showerror(
                "Erreur de conversion", 
                f"Une erreur est survenue :\n{str(e)}",
                parent=self
            )