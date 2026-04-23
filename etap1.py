# etap1.py
import numpy as np
from PIL import Image
 
def calculate_shift(row_index, key, width):
    return (key + row_index * (key % 10 + 1)) % width

def build_comparison_text(height, width, key, count=10):
    limit = min(count, height)
    lines = []

    lines.append("ETAP 1 - NAIWNY SCRAMBLING")
    lines.append("")
    lines.append(f"Klucz poprawny: {key}")
    lines.append(f"Klucz błędny:   {key + 1}")
    lines.append(f"Szerokość obrazu: {width}")
    lines.append("")

    lines.append("1. Przesunięcia dla key")
    for i in range(limit):
        shift_key = calculate_shift(i, key, width)
        lines.append(f"s_key({i}) = {shift_key}")

    lines.append("")
    lines.append("2. Przesunięcia dla key + 1")
    for i in range(limit):
        shift_key1 = calculate_shift(i, key + 1, width)
        lines.append(f"s_key+1({i}) = {shift_key1}")

    lines.append("")
    lines.append("3. Poprawne odtwarzanie (0 -> po przesunięciu -> po odtworzeniu)")
    for i in range(limit):
        shift_key = calculate_shift(i, key, width)
        scrambled_pos = (0 + shift_key) % width
        restored_pos = (scrambled_pos - shift_key) % width
        lines.append(
            f"wiersz {i}: roll(-{shift_key}, roll(+{shift_key}, wiersz_{i})), 0 -> {scrambled_pos} -> {restored_pos}"
        )

    lines.append("")
    lines.append("4. Próba odtworzenia złym kluczem (0 -> po przesunięciu -> po odtworzeniu)")
    for i in range(limit):
        shift_key = calculate_shift(i, key, width)
        shift_key1 = calculate_shift(i, key + 1, width)
        scrambled_pos = (0 + shift_key) % width
        restored_wrong = (scrambled_pos - shift_key1) % width
        lines.append(
            f"wiersz {i}: roll(-{shift_key1}, roll(+{shift_key}, wiersz_{i})), 0 -> {scrambled_pos} -> {restored_wrong}"
        )

    return "\n".join(lines)
   
def naive_scrambling(input_path, output_path, key, is_encrypt = True):
    img = Image.open(input_path)
    img_array = np.array(img)
    
    height, width = img_array.shape[:2]
    result_array = np.zeros_like(img_array)
    
    for i in range(height):
        shift = calculate_shift(i, key, width)
        result_array[i] = np.roll(img_array[i], (shift if is_encrypt else -shift), axis=0)
        
    result_img = Image.fromarray(result_array)
    result_img.save(output_path)
    if is_encrypt:
        print(f"[Etap 1] Scrambling zakończony: {input_path} -> {output_path}, klucz = {key}")
    else:
        print(f"[Etap 1] Unscrambling zakończony: {input_path} -> {output_path}, klucz = {key}")