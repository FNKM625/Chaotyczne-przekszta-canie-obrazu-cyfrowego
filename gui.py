# gui.py
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import tkinter as tk
import numpy as np
import etap1, etap2, etap3
import os, shutil

class ProjektGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Projekt M-II: Chaotyczne przekształcanie obrazu")
        self.root.geometry("1300x600")
        self.root.minsize(1300, 600)

        self.folder_temp = "temp"
        shutil.rmtree(self.folder_temp, ignore_errors=True)
        os.makedirs(self.folder_temp, exist_ok=True)
        self.path_original = None
        self.path_scrambled = os.path.join(self.folder_temp, "przeksztalcony.png")
        self.path_unscrambled = os.path.join(self.folder_temp, "odtworzony.png")
        self.path_unscrambled_wrong = os.path.join(self.folder_temp, "odtworzony_zly_klucz.png")

        self.folder_save = "save"
        os.makedirs(self.folder_save, exist_ok=True)
        self.folder_save = os.path.join(self.folder_save, "")

        self.create_control_panel()
        self.create_image_panels()

    def create_control_panel(self):
        frame_control = tk.Frame(self.root, pady=10)
        frame_control.pack(side=tk.TOP, fill=tk.X)

        try:
            img_logo = Image.open("UWB.png")
            img_h = img_logo.height
            img_w = img_logo.width
            img_scale = 0.5
            img_logo = img_logo.resize((int(img_w * img_scale), int(img_h * img_scale)))
            self.logo_tk_panel = ImageTk.PhotoImage(img_logo)
            
            label_logo = tk.Label(frame_control, image=self.logo_tk_panel)
            label_logo.pack(side=tk.LEFT, padx=10)
        except Exception:
            pass
        
        btn_read = tk.Button(frame_control, text="Wczytaj obraz", command=self.btn_get_original_image)
        btn_read.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_control, text="Etap:").pack(side=tk.LEFT, padx=5)
        self.stage_selection = tk.StringVar(value="1")
        tk.OptionMenu(frame_control, self.stage_selection, "1", "2", "3").pack(side=tk.LEFT)

        tk.Label(frame_control, text="Klucz:").pack(side=tk.LEFT, padx=5)
        self.key_entry = tk.Entry(frame_control, width=10)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        self.key_entry.insert(0, "42")
        
        tk.Label(frame_control, text="Zły klucz:").pack(side=tk.LEFT, padx=5)
        self.wrong_key_entry = tk.Entry(frame_control, width=10)
        self.wrong_key_entry.pack(side=tk.LEFT, padx=5)
        self.wrong_key_entry.insert(0, "43")

        btn_scramble = tk.Button(frame_control, text="Scramble", command=self.action_scramble, bg="lightblue")
        btn_scramble.pack(side=tk.LEFT, padx=5)
            
        btn_unscramble = tk.Button(frame_control, text="Unscramble", command=self.action_unscramble, bg="lightgreen")
        btn_unscramble.pack(side=tk.LEFT, padx=5)
        
        btn_unscramble_wrong = tk.Button(frame_control, text="Unscramble zły klucz", command=lambda: self.action_unscramble(type="Wrong Key"), bg="red3")
        btn_unscramble_wrong.pack(side=tk.LEFT, padx=5)
 
        btn_reset = tk.Button(frame_control, text="Reset", command=self.btn_reset, bg="lightblue")
        btn_reset.pack(side=tk.LEFT, padx=5)
        
        btn_mapping = tk.Button(frame_control, text="Pokaż odwzorowania", command=self.btn_show_mapping)
        btn_mapping.pack(side=tk.LEFT, padx=5)
        
        btn_save_files = tk.Button(frame_control, text="Zapisz pliki", command=self.btn_save_files, bg="lightblue")
        btn_save_files.pack(side=tk.LEFT, padx=5)
        
    def create_image_panels(self):
        frame_image = tk.Frame(self.root)
        frame_image.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        panel_width = 300
        panel_height = 320

        # Oryginał
        self.frame_original = tk.LabelFrame(
            frame_image,
            text="Oryginał",
            bd=2,
            relief="solid",
            width=panel_width,
            height=panel_height,
            font=("Arial", 11, "bold"),
            labelanchor="n"
        )
        self.frame_original.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        self.frame_original.pack_propagate(False)

        self.panel_original = tk.Label(
            self.frame_original,
            text="Brak obrazu",
            bg="lightgray"
        )
        self.panel_original.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrambled
        self.frame_scrambled = tk.LabelFrame(
            frame_image,
            text="Scrambled",
            bd=2,
            relief="solid",
            width=panel_width,
            height=panel_height,
            font=("Arial", 11, "bold"),
            labelanchor="n"
        )
        self.frame_scrambled.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        self.frame_scrambled.pack_propagate(False)

        self.panel_scrambled = tk.Label(
            self.frame_scrambled,
            text="Brak obrazu",
            bg="lightgray"
        )
        self.panel_scrambled.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Unscrambled
        self.frame_unscrambled = tk.LabelFrame(
            frame_image,
            text="Unscrambled",
            bd=2,
            relief="solid",
            width=panel_width,
            height=panel_height,
            font=("Arial", 11, "bold"),
            labelanchor="n"
        )
        self.frame_unscrambled.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        self.frame_unscrambled.pack_propagate(False)

        self.panel_unscrambled = tk.Label(
            self.frame_unscrambled,
            text="Brak obrazu",
            bg="lightgray"
        )
        self.panel_unscrambled.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Unscrambled wrong
        self.frame_unscrambled_wrong = tk.LabelFrame(
            frame_image,
            text="Unscrambled (zły klucz)",
            bd=2,
            relief="solid",
            width=panel_width,
            height=panel_height,
            font=("Arial", 11, "bold"),
            labelanchor="n"
        )
        self.frame_unscrambled_wrong.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        self.frame_unscrambled_wrong.pack_propagate(False)

        self.panel_unscrambled_wrong = tk.Label(
            self.frame_unscrambled_wrong,
            text="Brak obrazu",
            bg="lightgray"
        )
        self.panel_unscrambled_wrong.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- FUNKCJE BUTTON ---
    def btn_reset(self):
        self.path_original = None
        self.panel_original.config(image="", text="Oryginał\n(Brak obrazu)", bg="lightgray")
        self.panel_scrambled.config(image="", text="Przekształcony\n(Brak obrazu)", bg="lightgray")
        self.panel_unscrambled.config(image="", text="Odtworzony\n(Brak obrazu)", bg="lightgray")
        self.panel_unscrambled_wrong.config(image="", text="Odtworzony (zły klucz)\n(Brak obrazu)", bg="lightgray")
        
    def btn_get_original_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.path_original = path
            self.display_image(self.path_original, self.panel_original)
            
    def btn_show_mapping(self):
        if not self.path_original:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz!")
            return

        key = self.key_validation(self.key_entry.get())
        if key is None:
            return

        wrong_key = self.key_validation(self.wrong_key_entry.get())
        if wrong_key is None:
            return

        stage = self.stage_selection.get()
        mapping_file_path = self.get_mapping_file_path(stage, key, wrong_key)

        if os.path.exists(mapping_file_path):
            content = self.load_text_from_file(mapping_file_path)
        else:
            img = Image.open(self.path_original)
            img_array = np.array(img)

            if stage == "1":
                content = etap1.build_comparison_text(img_array, key, wrong_key, count=10)
                self.save_text_to_file(mapping_file_path, content)

            elif stage == "2":
                content = etap2.build_comparison_text(img_array, key, wrong_key, count=10)
                self.save_text_to_file(mapping_file_path, content)

            elif stage == "3":
                content = etap3.build_comparison_text(img_array, key, wrong_key, count=10)
                self.save_text_to_file(mapping_file_path, content)

        if stage == "1":
            self.show_text_window("Etap 1 - Przesunięcia", content)
        elif stage == "2":
            self.show_text_window("Etap 2 - Odwzorowania", content)
        elif stage == "3":
            self.show_text_window("Etap 3 - Hybryda", content)

    def btn_save_files(self):
        window = tk.Toplevel(self.root)
        window.title("Wybierz pliki do zapisania")
        window.geometry("350x260")
        window.resizable(False, False)
        window.grab_set()

        tk.Label(
            window,
            text="Wybierz co najmniej jeden plik do zapisania:",
            font=("Arial", 11, "bold")
        ).pack(pady=10)

        save_scrambled = tk.BooleanVar(value=False)
        save_unscrambled = tk.BooleanVar(value=False)
        save_unscrambled_wrong = tk.BooleanVar(value=False)
        save_mapping = tk.BooleanVar(value=False)

        tk.Checkbutton(window, text="Scrambled", variable=save_scrambled).pack(anchor="w", padx=20, pady=5)
        tk.Checkbutton(window, text="Unscrambled", variable=save_unscrambled).pack(anchor="w", padx=20, pady=5)
        tk.Checkbutton(window, text="Unscrambled - zły klucz", variable=save_unscrambled_wrong).pack(anchor="w", padx=20, pady=5)
        tk.Checkbutton(window, text="Odwzorowania (plik tekstowy)", variable=save_mapping).pack(anchor="w", padx=20, pady=5)

        def confirm_save():
            selected = []
            
            if save_scrambled.get():
                if os.path.exists(self.path_scrambled):
                    selected.append((self.path_scrambled, "przeksztalcony"))
                else:
                    messagebox.showwarning("Błąd", "Obraz Scrambled nie istnieje.")
                    return

            if save_unscrambled.get():
                if os.path.exists(self.path_unscrambled):
                    selected.append((self.path_unscrambled, "odtworzony"))
                else:
                    messagebox.showwarning("Błąd", "Obraz Unscrambled nie istnieje.")
                    return

            if save_unscrambled_wrong.get():
                if os.path.exists(self.path_unscrambled_wrong):
                    selected.append((self.path_unscrambled_wrong, "odtworzony_zly_klucz"))
                else:
                    messagebox.showwarning("Błąd", "Obraz odtworzony złym kluczem nie istnieje.")
                    return
                
            if save_mapping.get():
                stage = self.stage_selection.get()
                key = self.key_validation(self.key_entry.get())
                wrong_key = self.key_validation(self.wrong_key_entry.get())
                mapping_file_path = self.get_mapping_file_path(stage, key, wrong_key)
                
                if os.path.exists(mapping_file_path):
                    selected.append((mapping_file_path, "odwzorowania"))
                else: 
                    messagebox.showwarning("Błąd", "Plik z odwzorowaniami nie istnieje.")
                    return

            if not selected:
                messagebox.showwarning("Błąd", "Zaznacz co najmniej jeden obraz do zapisania.")
                return

            actual_time = datetime.now().strftime("%Y%m%d_%H%M%S")

            for source_path, default_name in selected:
                self.save_file(source_path, default_name, actual_time)

            window.destroy()

        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Zapisz", command=confirm_save, bg="lightgreen", width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Anuluj", command=window.destroy, bg="lightcoral", width=12).pack(side=tk.LEFT, padx=10)

    # --- FUNKCJE LOGICZNE ---
    def display_image(self, path, panel):
        img = Image.open(path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        panel.config(image=img_tk, text="")
        panel.image = img_tk
        
    def key_validation(self, key):
        try:
            key_int = int(key)
            return key_int
        except ValueError as e:
            messagebox.showerror("Błąd", "Nieprawidłowy klucz! Wprowadź liczbę całkowitą.")
            return None
        
    def save_file(self, source_path, default_name, actual_time):
        default_filename = f"{default_name}_{actual_time}{os.path.splitext(source_path)[1]}"

        save_path = filedialog.asksaveasfilename(initialdir=self.folder_save, initialfile=default_filename, defaultextension=os.path.splitext(source_path)[1], filetypes=[("All files", "*.*")])
        if save_path:
            try:
                shutil.copy(source_path, save_path)
                messagebox.showinfo("Sukces", f"Obraz zapisany jako: {save_path}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można zapisać obrazu: {e}")
    
    def get_mapping_file_path(self, stage, key, wrong_key):
        original_name = os.path.splitext(os.path.basename(self.path_original))[0]
        filename = f"{original_name}_etap{stage}_correctkey{key}_wrongkey{wrong_key}.txt"
        return os.path.join(self.folder_temp, filename)
    
    def save_text_to_file(self, file_path, content):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def load_text_from_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    # --- FUNKCJE ETAPÓW ---
    def action_scramble(self):
        if not self.path_original:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz!")
            return
        
        key = self.key_validation(self.key_entry.get())
        if key is None:
            return
        stage = self.stage_selection.get()

        if stage == "1":
            etap1.naive_scrambling(self.path_original, self.path_scrambled, key)
            self.display_image(self.path_scrambled, self.panel_scrambled)
        elif stage == "2":
            etap2.pure_permutation(self.path_original, self.path_scrambled, key)
            self.display_image(self.path_scrambled, self.panel_scrambled)
        elif stage == "3":
            etap3.hybrid_scrambling(self.path_original, self.path_scrambled, key)
            self.display_image(self.path_scrambled, self.panel_scrambled)
            
    def action_unscramble(self, type="Correct Key"):
        if not self.path_original:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz!")
            return
        if not os.path.exists(self.path_scrambled):
            messagebox.showwarning("Błąd", "Nie ma obrazu do odszyfrowania! Najpierw użyj opcji Scramble.")
            return
        
        if type == "Wrong Key":
            key = self.key_validation(self.wrong_key_entry.get())
            panel = self.panel_unscrambled_wrong
            path = self.path_unscrambled_wrong
        else:
            key = self.key_validation(self.key_entry.get())
            panel = self.panel_unscrambled
            path = self.path_unscrambled

        if key is None:
            return        
        stage = self.stage_selection.get()

        if stage == "1":
            etap1.naive_scrambling(self.path_scrambled, path, key, is_encrypt=False)
            self.display_image(path, panel)
        elif stage == "2":
            etap2.pure_permutation(self.path_scrambled, path, key, is_encrypt=False)
            self.display_image(path, panel)
        elif stage == "3":
            etap3.hybrid_scrambling(self.path_scrambled, path, key, is_encrypt=False)
            self.display_image(path, panel)

    def show_text_window(self, title, content):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("700x500")

        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(frame, wrap="word", font=("Consolas", 10), yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")

# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = ProjektGUI(root)
    root.mainloop()