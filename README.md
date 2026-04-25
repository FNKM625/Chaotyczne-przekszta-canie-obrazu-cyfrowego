# Projekt M-II – Chaotyczne przekształcanie obrazu cyfrowego

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![NumPy](https://img.shields.io/badge/NumPy-used-013243?logo=numpy&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-repository-black?logo=github)

Projekt dydaktyczny przedstawiający trzy odwracalne metody przekształcania obrazu cyfrowego: naiwny scrambling, czystą permutację sterowaną kluczem oraz hybrydę permutacji i substytucji.

Celem projektu nie jest stworzenie bezpiecznego szyfru, lecz praktyczne pokazanie różnicy między prostym scramblingiem, permutacją i mechanizmem wzmacniającym, a także analiza wpływu klucza na wynik i odwracalność algorytmów.

## Funkcje projektu

- Trzy etapy przekształcania obrazu.
- Osobne operacje `Scramble` i `Unscramble` dla każdego etapu.
- Odtwarzanie obrazu poprawnym oraz błędnym kluczem.
- Graficzny interfejs użytkownika w Tkinter.
- Obsługa obrazów PNG, JPG, JPEG i BMP.
- Podgląd obrazu oryginalnego, przekształconego i odtworzonego.
- Zapis wynikowych obrazów oraz plików tekstowych z odwzorowaniami i metrykami.
- Analiza korelacji sąsiednich pikseli oraz różnicy obrazu przy użyciu błędnego klucza.

## Etapy projektu

### Etap 1 – naiwny scrambling

W pierwszym etapie zastosowano prostą, odwracalną metodę przesuwania wierszy obrazu. Każdy wiersz jest przesuwany cyklicznie o wartość zależną od numeru wiersza, klucza oraz szerokości obrazu.

Metoda jest w pełni odwracalna przy poprawnym kluczu, ale zachowuje część lokalnej struktury obrazu, dlatego stanowi celowo słaby, „porażkowy” etap projektu.

### Etap 2 – czysta permutacja

Drugi etap realizuje czystą permutację pikseli bez zmiany ich wartości. Obraz jest spłaszczany do jednowymiarowej tablicy pikseli, a następnie przestawiany według permutacji zależnej od klucza.

Permutacja jest generowana deterministycznie na podstawie klucza i może być odwrócona przez permutację odwrotną. Dzięki temu obraz można poprawnie odtworzyć przy użyciu właściwego klucza.

### Etap 3 – hybryda permutacji i substytucji

Trzeci etap rozszerza etap drugi o prostą substytucję wartości pikseli. Najpierw wykonywana jest permutacja, a następnie do wartości pikseli dodawana jest wartość zależna od klucza modulo 256.

Podczas odtwarzania obraz przechodzi odwrotne operacje w odwrotnej kolejności: najpierw cofana jest substytucja, a następnie stosowana jest permutacja odwrotna.

## Interfejs użytkownika

Aplikacja posiada graficzny interfejs użytkownika oparty na bibliotece Tkinter. Główne okno zawiera panel sterowania oraz cztery pola podglądu obrazów.

Dostępne elementy GUI:
- Wczytanie obrazu wejściowego.
- Wybór etapu 1, 2 lub 3.
- Podanie poprawnego i błędnego klucza.
- Przyciski `Scramble`, `Unscramble`, `Unscramble zły klucz`, `Reset`.
- Podgląd obrazów: oryginał, scrambled, unscrambled, unscrambled z błędnym kluczem.
- Zapis obrazów i pliku tekstowego z odwzorowaniami.

## Metryki i analiza

Projekt umożliwia porównywanie działania algorytmów za pomocą prostych miar ilościowych.

Obliczane są:
- Korelacja sąsiednich pikseli w poziomie i pionie przed scramblingiem oraz po nim.
- Mean Absolute Difference (MAD) dla obrazu odtwarzanego błędnym kluczem.
- Mean Squared Error (MSE) dla obrazu odtwarzanego błędnym kluczem.

Dodatkowo aplikacja może wygenerować tekstowy raport zawierający przykładowe odwzorowania indeksów, sprawdzenie odwracalności oraz wyniki metryk dla wybranego etapu.

## Wymagania

Do uruchomienia projektu potrzebny jest Python 3 oraz następujące biblioteki:
- `numpy`.
- `Pillow`.
- `tkinter`.

## Instalacja

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/FNKM625/Chaotyczne-przekszta-canie-obrazu-cyfrowego.git
   cd Chaotyczne-przekszta-canie-obrazu-cyfrowego
   ```

2. Zainstaluj wymagane biblioteki:
   ```bash
   pip install numpy pillow
   ```

> `tkinter` zwykle jest dostępny razem z Pythonem. W niektórych systemach Linux może wymagać osobnej instalacji.

## Uruchomienie

Uruchom plik GUI:
```bash
python gui.py
```

Jeżeli w repozytorium główny plik interfejsu ma inną nazwę, uruchom odpowiedni plik odpowiadający GUI projektu.

## Jak używać

1. Kliknij **Wczytaj obraz** i wybierz plik PNG, JPG, JPEG lub BMP.
2. Wybierz etap działania: **1**, **2** lub **3**.
3. Wprowadź wartość **Klucza** oraz **Złego klucza**.
4. Kliknij **Scramble**, aby przekształcić obraz.
5. Kliknij **Unscramble**, aby odtworzyć obraz poprawnym kluczem.
6. Kliknij **Unscramble zły klucz**, aby sprawdzić zachowanie algorytmu przy niepoprawnym kluczu.
7. Użyj opcji **Pokaż odwzorowania**, aby wyświetlić raport tekstowy dla wybranego etapu.
8. Użyj **Zapisz pliki**, aby zapisać obrazy i raport do plików.

## Struktura projektu

Przykładowa struktura plików:
```text
.
├── gui.py
├── etap1.py
├── etap2.py
├── etap3.py
├── temp/
├── save/
└── README.md
```

W projekcie logika została rozdzielona na osobne moduły odpowiadające kolejnym etapom oraz moduł GUI odpowiedzialny za interakcję z użytkownikiem.

## Charakter dydaktyczny

To rozwiązanie **nie jest bezpiecznym szyfrem**. Projekt ma charakter edukacyjny i służy do pokazania:
- różnicy między permutacją a substytucją
- wpływu klucza na wynik transformacji
- znaczenia odwracalności algorytmów
- tego, że wizualny chaos obrazu nie oznacza bezpieczeństwa danych

## Możliwe rozszerzenia

- Dodanie większej liczby metryk analizy obrazu.
- Eksport wyników eksperymentów do CSV lub PDF.
- Automatyczne generowanie porównań dla wielu obrazów testowych.
- Rozbudowa mechanizmu wzmacniającego o inne odwracalne funkcje podstawienia.
- Dodanie wykresów porównujących korelację i błędy dla wszystkich etapów.