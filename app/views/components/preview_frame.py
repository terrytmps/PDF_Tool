import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from app.core.pdf_preview import PDFPreviewGenerator


class PDFPreviewFrame(ttk.Frame):
    def __init__(self, parent, default_output_path):
        super().__init__(parent)
        self.preview_generator = PDFPreviewGenerator()
        self.current_previews = []
        self._create_widgets()

    def _create_widgets(self):
        # Canvas avec ascenseur
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.preview_container = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.preview_container, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Événements de défilement
        self.preview_container.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_pdf(self, pdf_path):
        """Charge un PDF et affiche les prévisualisations"""
        self._clear_previews()
        try:
            previews = self.preview_generator.generate_previews(pdf_path)
            self._display_previews(previews)
        except Exception as e:
            tk.messagebox.showerror("Erreur", str(e))

    def _display_previews(self, previews):
        """Affiche les vignettes dans le conteneur"""
        for i, preview in enumerate(previews):
            frame = ttk.Frame(self.preview_container)
            label = ttk.Label(frame, image=preview)
            label.image = preview  # Garde une référence
            label.pack(padx=5, pady=5)
            ttk.Label(frame, text=f"Page {i+1}").pack()
            frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)
        self.current_previews = previews

    def _clear_previews(self):
        """Efface les prévisualisations actuelles"""
        for widget in self.preview_container.winfo_children():
            widget.destroy()
        self.current_previews = []
