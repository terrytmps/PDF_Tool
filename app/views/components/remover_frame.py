import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.core.remover import PdfPageRemover

class RemoverFrame(ttk.Frame):
    def __init__(self, parent, output_path):
        super().__init__(parent)
        self.output_path = output_path
        self.remover = PdfPageRemover()
        self.current_file = None
        self._create_widgets()
        self._setup_placeholder()

    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Sélection de fichier
        self.select_btn = ttk.Button(
            self, 
            text="Sélectionner un PDF", 
            command=self._select_file
        )
        self.select_btn.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Entrée pour les pages
        self.pages_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.pages_var)
        self.entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Bouton de validation
        self.remove_btn = ttk.Button(
            self, 
            text="Supprimer les pages", 
            style="Accent.TButton", 
            command=self._remove_pages
        )
        self.remove_btn.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

    def _setup_placeholder(self):
        self.placeholder_text = "Ex: 1-3,5,7-9"
        self.entry.insert(0, self.placeholder_text)
        self.entry.config(foreground="grey")
        
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._restore_placeholder)

    def _clear_placeholder(self, event):
        if self.entry.get() == self.placeholder_text:
            self.entry.delete(0, tk.END)
            self.entry.config(foreground="black")

    def _restore_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder_text)
            self.entry.config(foreground="grey")

    def _select_file(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionnez un fichier PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.current_file = file_path
            self.select_btn.config(text=f"Fichier sélectionné : {os.path.basename(file_path)}")

    def _remove_pages(self):
        if not hasattr(self, 'current_file') or not self.current_file:
            messagebox.showwarning("Aucun fichier", "Veuillez sélectionner un fichier PDF")
            return

        pages = self.pages_var.get().strip()
        if not pages or pages == self.placeholder_text:
            messagebox.showwarning("Aucune page", "Veuillez spécifier les pages à supprimer")
            return

        try:
            output_path = self.remover.remove_pages(
                self.current_file, 
                pages, 
                self.output_path
            )
            messagebox.showinfo(
                "Suppression réussie", 
                f"Pages supprimées avec succès!\nNouveau fichier : {output_path}",
                parent=self
            )
            self._reset_form()
        except Exception as e:
            messagebox.showerror(
                "Erreur de suppression", 
                f"Une erreur est survenue :\n{str(e)}",
                parent=self
            )

    def _reset_form(self):
        self.pages_var.set("")
        self.current_file = None
        self.select_btn.config(text="Sélectionner un PDF")
        self._restore_placeholder(None)