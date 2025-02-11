from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
from PyPDF2 import PdfReader
from app.core.pdf_preview import PDFPreviewGenerator


class PDFPreviewFrame(ttk.Frame):
    def __init__(self, parent, output_path=None):
        super().__init__(parent)
        self.preview_generator = PDFPreviewGenerator()
        self.original_images = []
        self.page_frames = []
        self.current_pdf_path = None
        self.original_rotations = []
        self._create_widgets()

    def _create_widgets(self):
        # Barre d'outils
        toolbar = ttk.Frame(self)
        toolbar.pack(side="top", fill="x")

        # Boutons de rotation
        ttk.Button(
            toolbar, text="↺ Rotation gauche", command=lambda: self.rotate_selected(90)
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar, text="↻ Rotation droite", command=lambda: self.rotate_selected(-90)
        ).pack(side="left", padx=5)

        # Bouton de suppression
        ttk.Button(
            toolbar, text="Supprimer la page", command=self.remove_selected
        ).pack(side="left", padx=5)

        # Zone de prévisualisation
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.preview_container = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.preview_container, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Événements
        self.preview_container.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def load_pdf(self, pdf_path):
        self._clear_previews()
        try:
            # Lire les rotations originales
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                self.original_rotations = [
                    page.get("/Rotate", 0) for page in reader.pages
                ]

            # Générer les prévisualisations
            self.original_images = self.preview_generator.generate_previews(pdf_path)
            self.current_pdf_path = pdf_path
            self._display_previews()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _display_previews(self):
        self.page_frames = []
        for i, img in enumerate(self.original_images):
            # Création de la miniature
            thumbnail = img.copy()
            thumbnail.thumbnail(
                self.preview_generator.thumbnail_size, Image.Resampling.LANCZOS
            )
            photo = ImageTk.PhotoImage(thumbnail)

            # Création du cadre
            frame = ttk.Frame(self.preview_container)
            var = tk.BooleanVar()

            # Checkbox
            ttk.Checkbutton(frame, variable=var).pack(side="top")

            # Image
            label = ttk.Label(frame, image=photo)
            label.image = photo
            label.pack(padx=5, pady=5)

            # Numéro de page
            ttk.Label(frame, text=f"Page {i+1}").pack()

            # Positionnement
            frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)

            self.page_frames.append(
                {
                    "frame": frame,
                    "var": var,
                    "label": label,
                    "index": i,
                    "original_index": i,
                    "rotation": 0,
                    "rotated_image": img.copy(),
                }
            )

    def rotate_selected(self, angle):
        for page in self.page_frames:
            if page["var"].get():
                # Stocker la rotation en degrés horaires
                page["rotation"] = (page["rotation"] - angle) % 360

                # Rotation de l'image: Pivoter page['rotated_image']
                rotated_img = page["rotated_image"].rotate(angle, expand=True)
                page["rotated_image"] = (
                    rotated_img  # Mettre à jour rotated_image avec l'image pivotée
                )

                thumbnail = rotated_img.copy()
                thumbnail.thumbnail(
                    self.preview_generator.thumbnail_size, Image.Resampling.LANCZOS
                )

                # Mise à jour de l'affichage
                new_photo = ImageTk.PhotoImage(thumbnail)
                page["label"].configure(image=new_photo)
                page["label"].image = new_photo

    def remove_selected(self):
        selected_pages = [page for page in self.page_frames if page["var"].get()]
        for page in selected_pages:
            page["frame"].destroy()
            self.page_frames.remove(page)
        self._reindex_pages()

    def _reindex_pages(self):
        for i, page in enumerate(self.page_frames):
            page["index"] = i
            page["frame"].grid(row=i // 4, column=i % 4, padx=10, pady=10)
            page["frame"].winfo_children()[-1].configure(text=f"Page {i+1}")

    def get_rotations(self):
        return [
            p["rotation"] for p in sorted(self.page_frames, key=lambda x: x["index"])
        ]

    def _clear_previews(self):
        for widget in self.preview_container.winfo_children():
            widget.destroy()
        self.page_frames = []
        self.original_images = []
        self.original_rotations = []

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
