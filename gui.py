import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import etap1
import os

class ProjektGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Projekt M-II: Chaotyczne przekształcanie obrazu")
        self.root.geometry("1000x600")

        self.folder_temp = "temp"
        os.makedirs(self.folder_temp, exist_ok=True)
        
        self.sciezka_oryginal = None
        self.sciezka_zaszyfrowany = os.path.join(self.folder_temp, "zaszyfrowany.png")
        self.sciezka_odszyfrowany = os.path.join(self.folder_temp, "odszyfrowany.png")

        self.stworz_panel_sterowania()
        self.stworz_panel_obrazow()

    def stworz_panel_sterowania(self):
        frame_sterowanie = tk.Frame(self.root, pady=10)
        frame_sterowanie.pack(side=tk.TOP, fill=tk.X)

        btn_wczytaj = tk.Button(frame_sterowanie, text="Wczytaj obraz", command=self.wczytaj_obraz)
        btn_wczytaj.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_sterowanie, text="Etap:").pack(side=tk.LEFT, padx=5)
        self.wybor_etapu = tk.StringVar(value="1")
        tk.OptionMenu(frame_sterowanie, self.wybor_etapu, "1", "2", "3").pack(side=tk.LEFT)

        tk.Label(frame_sterowanie, text="Klucz:").pack(side=tk.LEFT, padx=5)
        self.pole_klucz = tk.Entry(frame_sterowanie, width=10)
        self.pole_klucz.pack(side=tk.LEFT, padx=5)
        self.pole_klucz.insert(0, "42")

        btn_scramble = tk.Button(frame_sterowanie, text="Scramble", command=self.akcja_scramble, bg="lightcoral")
        btn_scramble.pack(side=tk.LEFT, padx=5)

        btn_unscramble = tk.Button(frame_sterowanie, text="Unscramble", command=self.akcja_unscramble, bg="lightgreen")
        btn_unscramble.pack(side=tk.LEFT, padx=5)

        btn_reset = tk.Button(frame_sterowanie, text="Reset", command=self.resetuj_panele, bg="lightblue")
        btn_reset.pack(side=tk.LEFT, padx=5)

    def resetuj_panele(self):
        self.sciezka_oryginal = None
        self.panel_oryginal.config(image="", text="Oryginał\n(Brak obrazu)", bg="lightgray")
        self.panel_zaszyfrowany.config(image="", text="Przekształcony\n(Brak obrazu)", bg="lightgray")
        self.panel_odszyfrowany.config(image="", text="Odtworzony\n(Brak obrazu)", bg="lightgray")

    def stworz_panel_obrazow(self):
        frame_obrazy = tk.Frame(self.root)
        frame_obrazy.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.panel_oryginal = tk.Label(frame_obrazy, text="Oryginał\n(Brak obrazu)", bg="lightgray", width=30, height=15)
        self.panel_oryginal.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.panel_zaszyfrowany = tk.Label(frame_obrazy, text="Przekształcony\n(Brak obrazu)", bg="lightgray", width=30, height=15)
        self.panel_zaszyfrowany.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.panel_odszyfrowany = tk.Label(frame_obrazy, text="Odtworzony\n(Brak obrazu)", bg="lightgray", width=30, height=15)
        self.panel_odszyfrowany.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

    # --- FUNKCJE LOGICZNE ---

    def wczytaj_obraz(self):
        sciezka = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if sciezka:
            self.sciezka_oryginal = sciezka
            self.wyswietl_obraz(self.sciezka_oryginal, self.panel_oryginal)

    def akcja_scramble(self):
        if not self.sciezka_oryginal:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz!")
            return
        
        klucz = int(self.pole_klucz.get())
        etap = self.wybor_etapu.get()

        if etap == "1":
            etap1.naive_scrambling(self.sciezka_oryginal, self.sciezka_zaszyfrowany, klucz)
            self.wyswietl_obraz(self.sciezka_zaszyfrowany, self.panel_zaszyfrowany)
            print("Zakończono Scramble.")

    def akcja_unscramble(self):
        if not self.sciezka_oryginal:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz!")
            return
        if not os.path.exists(self.sciezka_zaszyfrowany):
            messagebox.showwarning("Błąd", "Nie ma obrazu do odszyfrowania! Najpierw użyj opcji Scramble.")
            return
        
        klucz = int(self.pole_klucz.get())
        etap = self.wybor_etapu.get()

        if etap == "1":
            etap1.naive_scrambling(self.sciezka_zaszyfrowany, self.sciezka_odszyfrowany, -klucz)
            self.wyswietl_obraz(self.sciezka_odszyfrowany, self.panel_odszyfrowany)
            print("Zakończono Unscramble.")

    def wyswietl_obraz(self, sciezka, panel):
        img = Image.open(sciezka)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        panel.config(image=img_tk, text="")
        panel.image = img_tk

# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = ProjektGUI(root)
    root.mainloop()