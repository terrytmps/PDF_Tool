import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from app.core.pdf_preview import PDFPreviewGenerator


class PDFPreviewFrame(ttk.Frame):
    def __init__(self, parent, default_output_path):
        super().__init__(parent)
        self.preview_generator = PDFPreviewGenerator()
        self.original_images = []
        self.page_frames = []
        self._create_widgets()

    def _create_widgets(self):
        # Barre d'outils avec boutons de rotation
        toolbar = ttk.Frame(self)
        toolbar.pack(side='top', fill='x')

        self.rotate_left_btn = ttk.Button(
            toolbar, text="↺ Rotation gauche", command=lambda: self.rotate_selected(90)
        )
        self.rotate_left_btn.pack(side='left', padx=5)

        self.rotate_right_btn = ttk.Button(
            toolbar, text="↻ Rotation droite", command=lambda: self.rotate_selected(-90)
        )
        self.rotate_right_btn.pack(side='left', padx=5)

        # Canvas et ascenseur
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.preview_container = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.preview_container, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.preview_container.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def rotate_selected(self, angle):
        for page in self.page_frames:
            if page['var'].get():
                # Mise à jour de l'angle de rotation
                page['rotation'] = (page['rotation'] + angle) % 360
                
                # Rotation de l'image originale
                original_img = self.original_images[page['index']]
                rotated_img = original_img.rotate(page['rotation'], expand=True)
                
                # Création de la miniature
                thumbnail = rotated_img.copy()
                thumbnail.thumbnail(self.preview_generator.thumbnail_size, Image.Resampling.LANCZOS)
                
                # Mise à jour de l'image affichée
                new_photo = ImageTk.PhotoImage(thumbnail)
                page['label'].configure(image=new_photo)
                page['label'].image = new_photo

    def load_pdf(self, pdf_path):
        self._clear_previews()
        try:
            self.original_images = self.preview_generator.generate_previews(pdf_path)
            previews = []
            for img in self.original_images:
                thumbnail = img.copy()
                thumbnail.thumbnail(self.preview_generator.thumbnail_size, Image.Resampling.LANCZOS)
                previews.append(ImageTk.PhotoImage(thumbnail))
            self._display_previews(previews)
        except Exception as e:
            tk.messagebox.showerror("Erreur", str(e))

    def _display_previews(self, previews):
        self.page_frames = []
        for i, preview in enumerate(previews):
            frame = ttk.Frame(self.preview_container)
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(frame, variable=var)
            chk.pack(side='top')

            label = ttk.Label(frame, image=preview)
            label.image = preview
            label.pack(padx=5, pady=5)

            ttk.Label(frame, text=f"Page {i+1}").pack()
            frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)

            self.page_frames.append({
                'frame': frame,
                'var': var,
                'label': label,
                'index': i,
                'rotation': 0
            })

    def _clear_previews(self):
        for widget in self.preview_container.winfo_children():
            widget.destroy()
        self.page_frames = []
        self.original_images = []

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")