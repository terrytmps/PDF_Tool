from tkinter import ttk, filedialog, messagebox, StringVar
import tkinter
from app.core.compression import FileCompressor


class CompressionFrame(ttk.Frame):

    def __init__(self, parent, output_path):
        super().__init__(parent)
        self.output_path = output_path
        self.converter = FileCompressor()
        self.compression_level = tkinter.StringVar(value="good")
        self._create_widgets()

    def _create_widgets(self):
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(
            2, weight=1
        )  # Row 2 now has weight for radiobuttons to stay at top

        # Compression level selection
        level_frame = ttk.Frame(self)
        level_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ttk.Label(level_frame).grid(row=0, column=0, sticky="w")

        radio_less = ttk.Radiobutton(
            level_frame,
            text="Moins de qualité, forte compression",
            variable=self.compression_level,
            value="less",
        )
        radio_good = ttk.Radiobutton(
            level_frame,
            text="Bonne qualité, bonne compression",
            variable=self.compression_level,
            value="good",
        )
        radio_high = ttk.Radiobutton(
            level_frame,
            text="Haute qualité, moins de compression",
            variable=self.compression_level,
            value="high",
        )
        radio_less.grid(row=0, column=1, padx=5, sticky="w")
        radio_good.grid(row=0, column=2, padx=5, sticky="w")
        radio_high.grid(row=0, column=3, padx=5, sticky="w")

        # Bouton de conversion
        ttk.Button(
            self,
            text="Choisir des fichiers à compresser",
            style="Accent.TButton",
            command=self._compress_files,
        ).grid(row=1, column=0, pady=10, padx=10, sticky="ew")

    def _compress_files(self):
        input_files = filedialog.askopenfilenames(
            title="Sélectionnez des fichiers à compresser",
            filetypes=[
                ("PDF Files", "*.pdf"),
                ("Tous les fichiers", "*.*"),
            ],
        )
        if not input_files:
            return

        try:
            results = self.converter.compress_files(
                input_files,
                self.output_path,
                self.compression_level.get(),  # Pass the selected level
            )

            messagebox.showinfo(
                "Compression terminée",
                f"{len(results)} fichiers compressés avec succès!\n"
                + f"Emplacement : {self.output_path}",
                parent=self,
            )
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Une erreur s'est produite lors de la compression des fichiers : {str(e)}",
                parent=self,
            )
