import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
import pillow_heif  # Nécessaire pour la gestion des fichiers HEIC
import os

# Fonction pour obtenir le chemin vers le dossier Downloads
def get_downloads_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

# Liste des formats supportés
AVAILABLE_FORMATS = ["png", "jpeg", "pdf"]

# Fonction pour sélectionner des fichiers PDF à fusionner
def select_files():
    files = filedialog.askopenfilenames(
        title="Sélectionnez des fichiers PDF",
        filetypes=[("PDF Files", "*.pdf")],
    )
    for file in files:
        file_listbox.insert(tk.END, file)

def remove_selected():
    for index in reversed(file_listbox.curselection()):
        file_listbox.delete(index)

def move_up():
    for index in file_listbox.curselection():
        if index == 0:
            continue
        item = file_listbox.get(index)
        file_listbox.delete(index)
        file_listbox.insert(index - 1, item)
        file_listbox.selection_set(index - 1)

def move_down():
    for index in reversed(file_listbox.curselection()):
        if index == file_listbox.size() - 1:
            continue
        item = file_listbox.get(index)
        file_listbox.delete(index)
        file_listbox.insert(index + 1, item)
        file_listbox.selection_set(index + 1)

def merge_pdfs():
    files = file_listbox.get(0, tk.END)
    if not files:
        messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
        return

    # Générer un nom pour le fichier fusionné
    base_names = [os.path.basename(file).replace(".pdf", "") for file in files]
    output_file_name = f"merged_{'_'.join(base_names)}.pdf"
    output_file = os.path.join(get_downloads_folder(), output_file_name)

    try:
        merger = PdfMerger()
        for file in files:
            merger.append(file)
        merger.write(output_file)
        merger.close()
        messagebox.showinfo("Succès", f"Fichiers fusionnés en {output_file}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

def remove_pages():
    input_file = filedialog.askopenfilename(
        title="Sélectionnez un fichier PDF",
        filetypes=[("PDF Files", "*.pdf")],
    )
    if not input_file:
        return

    pages_to_remove = page_input_var.get()
    if not pages_to_remove:
        messagebox.showerror("Erreur", "Aucune page spécifiée.")
        return

    # Générer un nom pour le fichier modifié
    base_name = os.path.basename(input_file).replace(".pdf", "")
    output_file_name = f"removed_{base_name}.pdf"
    output_file = os.path.join(get_downloads_folder(), output_file_name)

    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        pages_to_remove_set = set()
        for part in pages_to_remove.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                pages_to_remove_set.update(range(start, end + 1))
            else:
                pages_to_remove_set.add(int(part))

        for page_number in range(len(reader.pages)):
            if page_number + 1 not in pages_to_remove_set:
                writer.add_page(reader.pages[page_number])

        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)

        messagebox.showinfo("Succès", f"Pages supprimées. Nouveau fichier : {output_file}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

# --- Nouvelle section : Conversion de fichiers ---
def convert_files():
    input_files = filedialog.askopenfilenames(
        title="Sélectionnez des fichiers à convertir",
        filetypes=[
            ("Tous les fichiers supportés", "*.heic;*.HEIC;*.png;*.jpg;*.jpeg;*.pdf"),
            ("Images", "*.png;*.jpg;*.jpeg;*.heic;*.HEIC"),
            ("PDF", "*.pdf"),
        ],
    )
    if not input_files:
        return

    output_format = output_format_var.get().lower()
    if output_format not in AVAILABLE_FORMATS:
        messagebox.showerror("Erreur", f"Format non supporté : {output_format}.")
        return

    output_folder = get_downloads_folder()

    try:
        for input_file in input_files:
            base_name, ext = os.path.splitext(os.path.basename(input_file))
            ext = ext.lower()

            if ext in [".png", ".jpg", ".jpeg", ".heic", ".HEIC"]:
                # Charger les fichiers HEIC avec pillow-heif
                if ext in [".heic", ".HEIC"]:
                    pillow_heif.register_heif_opener()
                img = Image.open(input_file)
                output_file = os.path.join(output_folder, f"{base_name}.{output_format}")
                img.save(output_file)
            elif ext == ".pdf" and output_format in ["png", "jpeg"]:
                reader = PdfReader(input_file)
                for page_num, page in enumerate(reader.pages, start=1):
                    output_file = os.path.join(output_folder, f"{base_name}_page{page_num}.{output_format}")
                    # Simulation d'extraction d'image (PyPDF2 ne supporte pas directement les images)
                    with open(output_file, "wb") as output_img:
                        output_img.write(page.extract_images()[0].data)

            else:
                messagebox.showwarning("Non supporté", f"Fichier non supporté : {input_file}")
                continue

        messagebox.showinfo("Succès", f"Fichiers convertis et enregistrés dans {output_folder}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion de fichiers PDF et conversions")
root.minsize(500, 500)  # Taille minimale de la fenêtre

# Variables
page_input_var = tk.StringVar()
output_format_var = tk.StringVar(value=AVAILABLE_FORMATS[0])  # Format par défaut

# Widgets pour fusionner les PDF
frame_files = ttk.Frame(root)
frame_files.pack(fill="x", padx=10, pady=5)

tk.Label(frame_files, text="Fichiers PDF à fusionner :").pack(anchor="w")
file_listbox = tk.Listbox(frame_files, selectmode=tk.EXTENDED, height=10)
file_listbox.pack(fill="both", expand=True, padx=5, pady=5)

frame_buttons = ttk.Frame(root)
frame_buttons.pack(fill="x", padx=10, pady=5)

ttk.Button(frame_buttons, text="Ajouter des fichiers", command=select_files).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame_buttons, text="Supprimer la sélection", command=remove_selected).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame_buttons, text="Monter", command=move_up).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(frame_buttons, text="Descendre", command=move_down).grid(row=0, column=3, padx=5, pady=5)

ttk.Button(root, text="Fusionner les fichiers", command=merge_pdfs).pack(pady=10)

# Widgets pour supprimer des pages
tk.Label(root, text="Supprimer des pages d'un PDF :").pack(anchor="w", padx=10, pady=5)
tk.Entry(root, textvariable=page_input_var, width=30).pack(pady=5)
ttk.Button(root, text="Supprimer les pages", command=remove_pages).pack(pady=10)

# Widgets pour la conversion
tk.Label(root, text="Conversion de fichiers :").pack(anchor="w", padx=10, pady=5)
conversion_frame = ttk.Frame(root)
conversion_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(conversion_frame, text="Format cible :").grid(row=0, column=0, padx=5, pady=5)
format_combobox = ttk.Combobox(conversion_frame, textvariable=output_format_var, values=AVAILABLE_FORMATS, state="readonly")
format_combobox.grid(row=0, column=1, padx=5, pady=5)

ttk.Button(conversion_frame, text="Convertir (sauf PDF)", command=convert_files).grid(row=0, column=2, padx=5, pady=5)

# Boucle principale
root.mainloop()
