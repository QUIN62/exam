import tkinter as tk
from tkinter import ttk
import threading


class classShow:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Registro de Dioses")
        self.root.geometry("600x300")
        self.root.resizable(False, False)

        # Configuración de la tabla (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("ID", "God", "Pantheon", "Domain"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("God", text="God")
        self.tree.heading("Pantheon", text="Pantheon")
        self.tree.heading("Domain", text="Domain")

        # Centrando los datos en cada columna
        self.tree.column("ID", anchor="center", width=50)
        self.tree.column("God", anchor="center", width=150)
        self.tree.column("Pantheon", anchor="center", width=150)
        self.tree.column("Domain", anchor="center", width=150)

        self.tree.pack(expand=True, fill="both")

        # Botones y entrada para el ID
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Cargar todos los registros", command=self.load_all_records_thread).pack(side="left",
                                                                                                       padx=5)
        self.id_entry = tk.Entry(frame, width=10)
        self.id_entry.pack(side="left", padx=5)
        tk.Button(frame, text="Mostrar registro ingresado", command=self.load_selected_record_thread).pack(side="left",
                                                                                                           padx=5)

    def update_treeview(self, records):
        # Limpiar la tabla
        self.tree.delete(*self.tree.get_children())

        if not records:
            # Mostrar mensaje de error si no hay registros
            self.tree.insert("", "end", values=("No records found", "", "", ""))
            return

        for record in records:
            # Cambiar a claves en mayúsculas para que coincidan con los datos de la API
            record_id = record.get("id", "N/A")
            name = record.get("NAME", "N/A")
            pantheon = record.get("PANTHEON", "N/A")
            domain = record.get("DOMAIN", "N/A")

            # Insertar el registro en la tabla
            self.tree.insert("", "end", values=(record_id, name, pantheon, domain))

    def load_all_records(self):
        print("Cargando todos los registros...")  # Mensaje de depuración
        records = self.db.get_all_records()
        print("Registros obtenidos:", records)  # Verifica los datos obtenidos
        self.root.after(0, self.update_treeview, records)

    def load_selected_record(self):
        selected_id = self.id_entry.get()
        print(f"Cargando registro con ID: {selected_id}")  # Mensaje de depuración
        record = self.db.get_record_by_id(selected_id)
        if record:
            self.root.after(0, self.update_treeview, [record])  # Actualizar la interfaz con un solo registro
        else:
            # Si no se encuentra el registro, mostrar un mensaje en la tabla
            self.root.after(0, self.update_treeview, [])

    def load_all_records_thread(self):
        threading.Thread(target=self.load_all_records).start()

    def load_selected_record_thread(self):
        threading.Thread(target=self.load_selected_record).start()
