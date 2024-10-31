import tkinter as tk
from tkinter import ttk
import threading

class classShow:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Registro de Dioses")
        self.root.geometry("600x400")

        # Marco para la tabla y la barra de desplazamiento
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Tabla (Treeview)
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "God", "Pantheon", "Domain"),
                                 show="headings", yscrollcommand=scrollbar.set)

        # Encabezados de la tabla
        for col in ["ID", "God", "Pantheon", "Domain"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

        # Configuración de la barra de desplazamiento
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(expand=True, fill="both")

        # Botones y entrada de ID
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Cargar todos los registros", command=self.load_all_records_thread).pack(side="left", padx=5)
        self.id_entry = tk.Entry(frame, width=10)
        self.id_entry.pack(side="left", padx=5)
        tk.Button(frame, text="Mostrar registro ingresado", command=self.load_selected_record_thread).pack(side="left", padx=5)
        tk.Button(frame, text="Refrescar", command=self.load_all_records_thread).pack(side="left", padx=5)

    def update_treeview(self, records):
        # Limpiar la tabla y actualizar con registros nuevos
        self.tree.delete(*self.tree.get_children())
        for i, record in enumerate(records):
            row_bg = "#f0f0f0" if i % 2 == 1 else "white"  # Alternar colores
            self.tree.insert("", "end", values=(record.get("id", "N/A"),
                                                record.get("NAME", "N/A"),
                                                record.get("PANTHEON", "N/A"),
                                                record.get("DOMAIN", "N/A")),
                             tags=('odd' if i % 2 else 'even'))
        self.tree.tag_configure('odd', background="#f0f0f0")
        self.tree.tag_configure('even', background="white")

    def load_all_records(self):
        records = self.db.get_all_records()
        self.root.after(0, self.update_treeview, records)

    def load_selected_record(self):
        record = self.db.get_record_by_id(self.id_entry.get())
        self.root.after(0, self.update_treeview, [record] if record else [])

    def load_all_records_thread(self):
        threading.Thread(target=self.load_all_records).start()

    def load_selected_record_thread(self):
        threading.Thread(target=self.load_selected_record).start()
