import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.core.merger import PdfMergerHandler

class MergerFrame(ttk.Frame):
    def __init__(self, parent, output_path):
        super().__init__(parent)
        self.output_path = output_path
        self.merger = PdfMergerHandler()
        self._create_widgets()

    def _create_widgets(self):
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Liste de fichiers
        self.file_listbox = tk.Listbox(self, selectmode=tk.EXTENDED, height=8)
        self.file_listbox.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)

        # Boutons de contrôle
        control_frame = ttk.Frame(self)
        control_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=10, pady=5)

        ttk.Button(control_frame, text="Ajouter des PDF", command=self._add_files).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Supprimer", command=self._remove_files).pack(side="left", padx=2)
        ttk.Button(control_frame, text="▲", width=3, command=self._move_up).pack(side="left", padx=2)
        ttk.Button(control_frame, text="▼", width=3, command=self._move_down).pack(side="left", padx=2)
        
        # Bouton de fusion
        ttk.Button(self, text="Fusionner les PDF", style="Accent.TButton", command=self._merge).grid(
            row=3, column=0, columnspan=4, pady=10, padx=10, sticky="ew"
        )

    def _add_files(self):
        files = filedialog.askopenfilenames(
            title="Sélectionnez des fichiers PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        for file in files:
            if file not in self.file_listbox.get(0, tk.END):
                self.file_listbox.insert(tk.END, file)

    def _remove_files(self):
        for index in reversed(self.file_listbox.curselection()):
            self.file_listbox.delete(index)

    def _move_up(self):
        selected = self.file_listbox.curselection()
        if not selected:
            return
        for pos in selected:
            if pos == 0:
                continue
            text = self.file_listbox.get(pos)
            self.file_listbox.delete(pos)
            self.file_listbox.insert(pos-1, text)
            self.file_listbox.selection_set(pos-1)

    def _move_down(self):
        selected = reversed(self.file_listbox.curselection())
        if not selected:
            return
        for pos in selected:
            if pos == self.file_listbox.size()-1:
                continue
            text = self.file_listbox.get(pos)
            self.file_listbox.delete(pos)
            self.file_listbox.insert(pos+1, text)
            self.file_listbox.selection_set(pos+1)

    def _merge(self):
        files = self.file_listbox.get(0, tk.END)
        if not files:
            messagebox.showwarning("Aucun fichier", "Veuillez sélectionner des fichiers PDF à fusionner")
            return
        
        try:
            output_path = self.merger.merge_files(files, self.output_path)
            messagebox.showinfo(
                "Fusion réussie", 
                f"Fichiers fusionnés avec succès!\nEmplacement : {output_path}",
                parent=self
            )
            self.file_listbox.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror(
                "Erreur de fusion", 
                f"Une erreur est survenue :\n{str(e)}",
                parent=self
            )