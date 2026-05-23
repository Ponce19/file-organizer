import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import shutil


CATEGORIAS = {
    "PDF": [".pdf"],
    "DOCX": [".docx"],
    "PPTX": [".pptx"],
    "XLSX": [".xlsx"],
    "IMAGENES": [".jpg", ".jpeg", ".png"]
}


""" CLASE PRINCIPAL """

class FileOrganizerApp:

    def __init__(self, root):

        self.root = root

        self.root.title("File Organizer v1.0.0")

        self.root.geometry("700x500")

        self.root.resizable(False, False)

        # Variable para guardar el directorio
        self.selected_directory = tk.StringVar()

        # Diccionario para guardar checkboxes
        self.checkbox_vars = {}

        # Crear interfaz
        self.create_ui()

    """ INTERFAZ GRÁFICA """
    
    def create_ui(self):

        # Título principal
        title = tk.Label(
            self.root,
            text="FILE ORGANIZER",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=15)
        
        """ SECCIÓN DIRECTORIO """

        directory_frame = tk.Frame(self.root)

        directory_frame.pack(fill="x", padx=20)

        directory_label = tk.Label(
            directory_frame,
            text="Carpeta Seleccionada:"
        )

        directory_label.pack(anchor="w")

        input_frame = tk.Frame(directory_frame)

        input_frame.pack(fill="x", pady=5)

        self.directory_entry = tk.Entry(
            input_frame,
            textvariable=self.selected_directory
        )

        self.directory_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        browse_button = tk.Button(
            input_frame,
            text="Examinar",
            command=self.select_directory
        )

        browse_button.pack(side="left", padx=5)

        
        """SECCIÓN CHECKBOXES"""

        categories_frame = tk.LabelFrame(
            self.root,
            text="Tipos de Archivos",
            padx=10,
            pady=10
        )

        categories_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # Crear checkboxes dinámicamente
        for category in CATEGORIAS:

            var = tk.BooleanVar(value=True)

            checkbox = tk.Checkbutton(
                categories_frame,
                text=category,
                variable=var
            )

            checkbox.pack(anchor="w")

            self.checkbox_vars[category] = var

        """ BOTÓN PRINCIPAL """

        organize_button = tk.Button(
            self.root,
            text="ORGANIZAR ARCHIVOS",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=10,
            command=self.organize_files
        )

        organize_button.pack(pady=10)

        """ ÁREA DE LOGS """

        logs_frame = tk.LabelFrame(
            self.root,
            text="Registro",
            padx=10,
            pady=10
        )

        logs_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.logs_text = tk.Text(
            logs_frame,
            height=12
        )

        self.logs_text.pack(fill="both", expand=True)

    
    """ SELECCIONAR DIRECTORIO """

    def select_directory(self):

        folder = filedialog.askdirectory()

        if folder:

            self.selected_directory.set(folder)

    """ ESCRIBIR LOGS """

    def write_log(self, message):

        self.logs_text.insert(
            tk.END,
            message + "\n"
        )

        self.logs_text.see(tk.END)

    """ ORGANIZAR ARCHIVOS """

    def organize_files(self):

        directory = self.selected_directory.get()

        # Validar carpeta
        if not directory:

            messagebox.showwarning(
                "Advertencia",
                "Selecciona una carpeta primero."
            )

            return

        path = Path(directory)

        # Categorías seleccionadas
        selected_categories = {

            category: extensions

            for category, extensions in CATEGORIAS.items()

            if self.checkbox_vars[category].get()
        }

        moved_files = 0

        # Recorrer archivos
        for file in path.iterdir():

            # Validar si es archivo
            if file.is_file():

                # Revisar categorías
                for category, extensions in selected_categories.items():

                    # Comparar extensión
                    if file.suffix.lower() in extensions:

                        # Crear carpeta destino
                        destination_folder = path / category

                        destination_folder.mkdir(exist_ok=True)

                        # Ruta final
                        destination = destination_folder / file.name

                        # Mover archivo
                        shutil.move(
                            str(file),
                            str(destination)
                        )

                        # Mostrar log
                        self.write_log(
                            f"Movido: {file.name} -> {category}/"
                        )

                        moved_files += 1

                        break

        # Mensaje final
        messagebox.showinfo(
            "Completado",
            f"Organización finalizada.\n"
            f"Archivos movidos: {moved_files}"
        )


# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    app = FileOrganizerApp(root)

    root.mainloop()