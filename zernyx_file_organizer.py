"""
============================================================
ZERNYX File Organizer
============================================================

Creado por Matias Frutos · ZERNYX

Herramienta para organizar archivos de una carpeta por tipo.
- Vista previa antes de mover
- Organización por categorías
- Historial en TXT
- Deshacer último movimiento
- Interfaz gráfica con Tkinter

============================================================
"""

import os
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


APP_NAME = "ZERNYX File Organizer"
LOG_FILE = "organizer_historial.txt"
UNDO_FILE = "organizer_ultimo_movimiento.txt"


CATEGORIES = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
    "Planillas": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentaciones": [".ppt", ".pptx", ".odp"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Audio": [".mp3", ".wav", ".ogg", ".flac", ".m4a"],
    "Codigo": [".py", ".js", ".html", ".css", ".php", ".java", ".json", ".xml", ".sql", ".bat"],
    "Instaladores": [".exe", ".msi"],
    "Otros": []
}


class ZernyxFileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("980x660")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f4f4f5")

        self.folder_path = tk.StringVar()
        self.status_text = tk.StringVar(value="Seleccioná una carpeta para analizar.")
        self.total_text = tk.StringVar(value="Archivos detectados: 0")

        self.include_subfolders = tk.BooleanVar(value=False)
        self.create_date_folder = tk.BooleanVar(value=False)
        self.skip_existing = tk.BooleanVar(value=True)

        self.preview_items = []

        self.build_ui()

    def build_ui(self):
        self.inject_styles()

        root = tk.Frame(self.root, bg="#f4f4f5")
        root.pack(fill="both", expand=True, padx=18, pady=16)

        self.create_header(root)
        self.create_folder_panel(root)
        self.create_tools_panel(root)
        self.create_preview_panel(root)
        self.create_footer(root)

    def inject_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Z.Treeview",
            background="#ffffff",
            foreground="#111111",
            fieldbackground="#ffffff",
            rowheight=25,
            font=("Consolas", 10)
        )

        style.configure(
            "Z.Treeview.Heading",
            background="#111111",
            foreground="#ffffff",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Z.Treeview",
            background=[("selected", "#111111")],
            foreground=[("selected", "#ffffff")]
        )

        style.configure(
            "Z.Horizontal.TProgressbar",
            troughcolor="#e8e8ea",
            background="#111111",
            bordercolor="#111111"
        )

    def create_header(self, parent):
        header = tk.Frame(parent, bg="#f4f4f5")
        header.pack(fill="x", pady=(0, 12))

        logo = tk.Label(
            header,
            text="Z",
            bg="#111111",
            fg="#ffffff",
            font=("Arial", 26, "bold"),
            width=3
        )
        logo.pack(side="left", padx=(0, 14))

        text_box = tk.Frame(header, bg="#f4f4f5")
        text_box.pack(side="left", fill="x", expand=True)

        tk.Label(
            text_box,
            text="ZERNYX File Organizer",
            bg="#f4f4f5",
            fg="#111111",
            font=("Arial", 24, "bold")
        ).pack(anchor="w")

        tk.Label(
            text_box,
            text="Organizador local de archivos para escritorio, descargas y carpetas operativas",
            bg="#f4f4f5",
            fg="#666666",
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            header,
            text="PYTHON / LOCAL",
            bg="#ffffff",
            fg="#111111",
            font=("Arial", 10, "bold"),
            relief="solid",
            bd=1,
            padx=14,
            pady=8
        ).pack(side="right")

    def create_folder_panel(self, parent):
        panel = tk.Frame(parent, bg="#ffffff", highlightbackground="#111111", highlightthickness=2)
        panel.pack(fill="x", pady=(0, 10))

        box = tk.Frame(panel, bg="#ffffff")
        box.pack(fill="x", padx=14, pady=14)

        tk.Label(
            box,
            text="Carpeta a organizar",
            bg="#ffffff",
            fg="#111111",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 5))

        row = tk.Frame(box, bg="#ffffff")
        row.pack(fill="x")

        tk.Entry(
            row,
            textvariable=self.folder_path,
            bg="#f8f8f9",
            fg="#111111",
            font=("Consolas", 10),
            relief="solid",
            bd=1
        ).pack(side="left", fill="x", expand=True, ipady=7)

        tk.Button(
            row,
            text="Seleccionar carpeta",
            command=self.select_folder,
            bg="#111111",
            fg="#ffffff",
            activebackground="#333333",
            activeforeground="#ffffff",
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            width=22
        ).pack(side="left", padx=(10, 0), ipady=7)

        options = tk.Frame(panel, bg="#ffffff")
        options.pack(fill="x", padx=14, pady=(0, 12))

        self.create_check(options, "Incluir subcarpetas", self.include_subfolders).pack(side="left", padx=(0, 18))
        self.create_check(options, "Crear carpeta con fecha", self.create_date_folder).pack(side="left", padx=(0, 18))
        self.create_check(options, "No sobrescribir existentes", self.skip_existing).pack(side="left")

    def create_check(self, parent, text, variable):
        return tk.Checkbutton(
            parent,
            text=text,
            variable=variable,
            bg="#ffffff",
            fg="#111111",
            activebackground="#ffffff",
            font=("Arial", 10, "bold")
        )

    def create_tools_panel(self, parent):
        panel = tk.Frame(parent, bg="#ffffff", highlightbackground="#111111", highlightthickness=1)
        panel.pack(fill="x", pady=(0, 10))

        left = tk.Frame(panel, bg="#ffffff")
        left.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        buttons = [
            ("Analizar carpeta", self.analyze_folder, "#111111", "#ffffff"),
            ("Organizar archivos", self.organize_files, "#111111", "#ffffff"),
            ("Deshacer último", self.undo_last, "#ffffff", "#111111"),
            ("Ver historial", self.open_log, "#ffffff", "#111111"),
            ("Abrir carpeta", self.open_selected_folder, "#ffffff", "#111111")
        ]

        for text, command, bg, fg in buttons:
            tk.Button(
                left,
                text=text,
                command=command,
                bg=bg,
                fg=fg,
                activebackground="#333333" if bg == "#111111" else "#eeeeee",
                activeforeground="#ffffff" if bg == "#111111" else "#111111",
                font=("Arial", 9, "bold"),
                relief="flat" if bg == "#111111" else "solid",
                bd=1,
                cursor="hand2"
            ).pack(side="left", padx=4, ipady=6, ipadx=8)

        tk.Label(
            panel,
            textvariable=self.total_text,
            bg="#ffffff",
            fg="#111111",
            font=("Arial", 10, "bold")
        ).pack(side="right", padx=12)

    def create_preview_panel(self, parent):
        panel = tk.Frame(parent, bg="#ffffff", highlightbackground="#111111", highlightthickness=2)
        panel.pack(fill="both", expand=True, pady=(0, 10))

        title_row = tk.Frame(panel, bg="#ffffff")
        title_row.pack(fill="x", padx=12, pady=(10, 6))

        tk.Label(
            title_row,
            text="Vista previa de organización",
            bg="#ffffff",
            fg="#111111",
            font=("Arial", 12, "bold")
        ).pack(side="left")

        tk.Label(
            title_row,
            text="No mueve archivos hasta presionar Organizar",
            bg="#ffffff",
            fg="#666666",
            font=("Arial", 9)
        ).pack(side="right")

        table_box = tk.Frame(panel, bg="#ffffff")
        table_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.tree = ttk.Treeview(
            table_box,
            columns=("category", "source", "target", "size"),
            show="headings",
            style="Z.Treeview"
        )

        self.tree.heading("category", text="Categoría")
        self.tree.heading("source", text="Archivo origen")
        self.tree.heading("target", text="Destino")
        self.tree.heading("size", text="Tamaño")

        self.tree.column("category", width=130, anchor="center")
        self.tree.column("source", width=310)
        self.tree.column("target", width=310)
        self.tree.column("size", width=100, anchor="e")

        scrollbar_y = ttk.Scrollbar(table_box, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_box, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_box.grid_rowconfigure(0, weight=1)
        table_box.grid_columnconfigure(0, weight=1)

    def create_footer(self, parent):
        footer = tk.Frame(parent, bg="#f4f4f5")
        footer.pack(fill="x")

        self.progress = ttk.Progressbar(
            footer,
            orient="horizontal",
            mode="determinate",
            style="Z.Horizontal.TProgressbar"
        )
        self.progress.pack(fill="x", pady=(0, 8))

        tk.Label(
            footer,
            textvariable=self.status_text,
            bg="#f4f4f5",
            fg="#111111",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        bottom = tk.Frame(footer, bg="#f4f4f5")
        bottom.pack(fill="x", pady=(6, 0))

        tk.Label(
            bottom,
            text="Desarrollo realizado por Matias Frutos · ZERNYX",
            bg="#f4f4f5",
            fg="#666666",
            font=("Consolas", 9)
        ).pack(side="left")

        tk.Label(
            bottom,
            text="v1.0 · File Organizer",
            bg="#f4f4f5",
            fg="#111111",
            font=("Arial", 9, "bold")
        ).pack(side="right")

    def select_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta a organizar")
        if folder:
            self.folder_path.set(folder)
            self.analyze_folder()

    def analyze_folder(self):
        folder = self.folder_path.get().strip()

        if not folder:
            messagebox.showwarning("Falta carpeta", "Seleccioná una carpeta para analizar.")
            return

        if not os.path.isdir(folder):
            messagebox.showerror("Error", "La carpeta seleccionada no existe.")
            return

        self.tree.delete(*self.tree.get_children())
        self.preview_items.clear()
        self.progress["value"] = 0

        files = self.get_files(folder)

        for file_path in files:
            category = self.detect_category(file_path)
            target_folder = self.build_target_folder(folder, category)
            target_path = os.path.join(target_folder, os.path.basename(file_path))
            size = self.format_size(self.safe_get_size(file_path))

            self.preview_items.append({
                "source": file_path,
                "category": category,
                "target": target_path,
                "size": size
            })

            self.tree.insert(
                "",
                "end",
                values=(category, file_path, target_path, size)
            )

        self.total_text.set(f"Archivos detectados: {len(self.preview_items)}")
        self.status_text.set("Análisis finalizado. Revisá la vista previa antes de organizar.")

    def get_files(self, folder):
        files = []

        if self.include_subfolders.get():
            for root, dirs, filenames in os.walk(folder):
                for name in filenames:
                    path = os.path.join(root, name)
                    if self.should_ignore(path):
                        continue
                    files.append(path)
        else:
            for name in os.listdir(folder):
                path = os.path.join(folder, name)
                if os.path.isfile(path) and not self.should_ignore(path):
                    files.append(path)

        return sorted(files)

    def should_ignore(self, path):
        filename = os.path.basename(path)

        ignored = {
            LOG_FILE,
            UNDO_FILE
        }

        return filename in ignored

    def detect_category(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()

        for category, extensions in CATEGORIES.items():
            if extension in extensions:
                return category

        return "Otros"

    def build_target_folder(self, base_folder, category):
        if self.create_date_folder.get():
            date_name = datetime.datetime.now().strftime("Organizado_%Y-%m-%d")
            return os.path.join(base_folder, date_name, category)

        return os.path.join(base_folder, category)

    def organize_files(self):
        if not self.preview_items:
            messagebox.showwarning("Sin análisis", "Primero analizá una carpeta.")
            return

        confirm = messagebox.askyesno(
            "Confirmar organización",
            "Se moverán los archivos según la vista previa.\n\n¿Querés continuar?"
        )

        if not confirm:
            return

        moved = []
        errors = 0
        total = len(self.preview_items)
        self.progress["value"] = 0

        for index, item in enumerate(self.preview_items, start=1):
            source = item["source"]
            target = item["target"]

            try:
                if not os.path.exists(source):
                    continue

                os.makedirs(os.path.dirname(target), exist_ok=True)

                final_target = target

                if os.path.exists(final_target):
                    if self.skip_existing.get():
                        final_target = self.get_unique_path(final_target)
                    else:
                        os.remove(final_target)

                shutil.move(source, final_target)
                moved.append((source, final_target))

            except Exception as error:
                errors += 1
                self.write_log(source, target, f"ERROR: {error}")

            percent = int((index / total) * 100)
            self.progress["value"] = percent
            self.root.update_idletasks()

        self.save_undo(moved)
        self.write_log("ORGANIZACION", self.folder_path.get(), f"OK: {len(moved)} movidos · Errores: {errors}")

        messagebox.showinfo(
            "Proceso finalizado",
            f"Organización finalizada.\n\nArchivos movidos: {len(moved)}\nErrores: {errors}"
        )

        self.status_text.set(f"Organización finalizada · Movidos: {len(moved)} · Errores: {errors}")
        self.analyze_folder()

    def undo_last(self):
        if not os.path.exists(UNDO_FILE):
            messagebox.showinfo("Deshacer", "No hay movimientos para deshacer.")
            return

        confirm = messagebox.askyesno(
            "Deshacer último movimiento",
            "Se intentará devolver los archivos a su ubicación original.\n\n¿Continuar?"
        )

        if not confirm:
            return

        restored = 0
        errors = 0

        with open(UNDO_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split("|")

            if len(parts) != 2:
                continue

            original, moved = parts

            try:
                if os.path.exists(moved):
                    os.makedirs(os.path.dirname(original), exist_ok=True)

                    final_original = original
                    if os.path.exists(final_original):
                        final_original = self.get_unique_path(final_original)

                    shutil.move(moved, final_original)
                    restored += 1

            except Exception as error:
                errors += 1
                self.write_log(moved, original, f"ERROR DESHACER: {error}")

        os.remove(UNDO_FILE)

        messagebox.showinfo(
            "Deshacer finalizado",
            f"Archivos restaurados: {restored}\nErrores: {errors}"
        )

        self.status_text.set(f"Deshacer finalizado · Restaurados: {restored} · Errores: {errors}")
        self.analyze_folder()

    def save_undo(self, moved):
        with open(UNDO_FILE, "w", encoding="utf-8") as file:
            for source, target in moved:
                file.write(f"{source}|{target}\n")

    def write_log(self, source, target, result):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        text = (
            "------------------------------------------------------------\n"
            f"Fecha: {timestamp}\n"
            f"Origen: {source}\n"
            f"Destino: {target}\n"
            f"Resultado: {result}\n"
        )

        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(text)

    def open_log(self):
        if not os.path.exists(LOG_FILE):
            messagebox.showinfo("Historial", "Todavía no hay historial.")
            return

        try:
            os.startfile(LOG_FILE)
        except Exception:
            messagebox.showerror("Error", "No se pudo abrir el historial.")

    def open_selected_folder(self):
        folder = self.folder_path.get().strip()

        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("Carpeta no disponible", "Seleccioná una carpeta válida.")
            return

        try:
            os.startfile(folder)
        except Exception:
            messagebox.showerror("Error", "No se pudo abrir la carpeta.")

    def get_unique_path(self, path):
        if not os.path.exists(path):
            return path

        folder = os.path.dirname(path)
        filename = os.path.basename(path)
        name, extension = os.path.splitext(filename)

        counter = 1

        while True:
            candidate = os.path.join(folder, f"{name}_{counter}{extension}")

            if not os.path.exists(candidate):
                return candidate

            counter += 1

    def safe_get_size(self, path):
        try:
            return os.path.getsize(path)
        except OSError:
            return 0

    def format_size(self, size):
        size = float(size)
        units = ["B", "KB", "MB", "GB", "TB"]
        index = 0

        while size >= 1024 and index < len(units) - 1:
            size /= 1024
            index += 1

        if index == 0:
            return f"{int(size)} {units[index]}"

        return f"{size:.2f} {units[index]}"


def main():
    root = tk.Tk()
    app = ZernyxFileOrganizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()