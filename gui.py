# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import numpy as np
import etap1, etap2, etap3
import os

class ProjektGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Projekt M-II: Chaotyczne przekształcanie obrazu")
        self.root.geometry("1000x600")

        self.folder_temp = "temp"
        os.makedirs(self.folder_temp, exist_ok=True)
        
        self.path_original = None
        self.path_scrambled = os.path.join(self.folder_temp, "przeksztalcony.png")
        self.path_unscrambled = os.path.join(self.folder_temp, "odtworzony.png")

        self.create_control_panel()
        self.create_image_panels()

    def create_control_panel(self):
        frame_control = tk.Frame(self.root, pady=10)
        frame_control.pack(side=tk.TOP, fill=tk.X)

        btn_read = tk.Button(frame_control, text="Wczytaj obraz", command=self.btn_get_original_image)
        btn_read.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_control, text="Etap:").pack(side=tk.LEFT, padx=5)
        self.stage_selection = tk.StringVar(value="1")
        tk.OptionMenu(frame_control, self.stage_selection, "1", "2", "3").pack(side=tk.LEFT)

        tk.Label(frame_control, text="Klucz:").pack(side=tk.LEFT, padx=5)
        self.key_entry = tk.Entry(frame_control, width=10)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        self.key_entry.insert(0, "42")

        btn_scramble = tk.Button(frame_control, text="Scramble", command=self.action_scramble, bg="lightcoral")
        btn_scramble.pack(side=tk.LEFT, padx=5)

        btn_unscramble = tk.Button(frame_control, text="Unscramble", command=self.action_unscramble, bg="lightgreen")
        btn_unscramble.pack(side=tk.LEFT, padx=5)

        btn_reset = tk.Button(frame_control, text="Reset", command=self.btn_reset, bg="lightblue")
        btn_reset.pack(side=tk.LEFT, padx=5)
        
        btn_mapping = tk.Button(frame_control, text="Pokaż odwzorowania", command=self.btn_show_mapping)
        btn_mapping.pack(side=tk.LEFT, padx=5)
        
    def create_image_panels(self):
        frame_image = tk.Frame(self.root)
        frame_image.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.panel_original = tk.Label(frame_image, text="Oryginał\n(Brak obrazu)", bg="lightgray", width=30, height=15)
        self.panel_original.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.panel_scrambled = tk.Label(frame_image, text="Przekształcony\n(Brak obrazu)", bg="lightgray", width=30, height=15)
        self.panel_scrambled.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.panel_unscrambled = tk.Label(frame_image, text="Odtworzony\n(Brak obrazu)", bg="lightgray", width=30, height=15)
        self.panel_unscrambled.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

    # --- FUNKCJE BUTTON ---
    def btn_reset(self):
        self.path_original = None
        self.panel_original.config(image="", text="Oryginał\n(Brak obrazu)", bg="lightgray")
        self.panel_scrambled.config(image="", text="Przekształcony\n(Brak obrazu)", bg="lightgray")
        self.panel_unscrambled.config(image="", text="Odtworzony\n(Brak obrazu)", bg="lightgray")

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
        
        stage = self.stage_selection.get()
        
        img = Image.open(self.path_original)
        img_array = np.array(img)
        
        if stage == "1":
            height, width = img_array.shape[:2]
            
            content = etap1.build_comparison_text(height, width, key, count=10)
            self.show_text_window("Etap 1 - Przesunięcia", content)
            
        elif stage == "2" or stage == "3":
            originalshape = img_array.shape
            
            if len(originalshape) == 2:
                flatpixels = img_array.reshape(-1, 1)
            else:
                flatpixels = img_array.reshape(-1, originalshape[2])

            pixelcount = flatpixels.shape[0]
            
            if stage == "2":
                content = etap2.build_comparison_text(pixelcount, key, count=10)
                self.show_text_window("Etap 2 - Odwzorowania", content)
            
            elif stage == "3":
                content = etap3.build_comparison_text(pixelcount, key, count=10)
                self.show_text_window("Etap 3 - Hybryda", content)

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
            
    def action_unscramble(self):
        if not self.path_original:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz!")
            return
        if not os.path.exists(self.path_scrambled):
            messagebox.showwarning("Błąd", "Nie ma obrazu do odszyfrowania! Najpierw użyj opcji Scramble.")
            return
        
        key = self.key_validation(self.key_entry.get())
        if key is None:
            return        
        stage = self.stage_selection.get()

        if stage == "1":
            etap1.naive_scrambling(self.path_scrambled, self.path_unscrambled, key, is_encrypt=False)
            self.display_image(self.path_unscrambled, self.panel_unscrambled)
        elif stage == "2":
            etap2.pure_permutation(self.path_scrambled, self.path_unscrambled, key, is_encrypt=False)
            self.display_image(self.path_unscrambled, self.panel_unscrambled)
        elif stage == "3":
            etap3.hybrid_scrambling(self.path_scrambled, self.path_unscrambled, key, is_encrypt=False)
            self.display_image(self.path_unscrambled, self.panel_unscrambled)

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