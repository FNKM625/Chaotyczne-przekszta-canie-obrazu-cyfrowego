# etap1.py
import numpy as np
from PIL import Image
    
def naive_scrambling(input_path, output_path, key, is_encrypt = True):
    img = Image.open(input_path)
    img_array = np.array(img)
    
    height, width = img_array.shape[:2]
    result_array = np.zeros_like(img_array)
    
    for i in range(height):
        shift = (key + i * (key % 10 + 1)) % width
        result_array[i] = np.roll(img_array[i], (shift if is_encrypt else -shift), axis=0)
        
    result_img = Image.fromarray(result_array)
    result_img.save(output_path)
    if is_encrypt:
        print(f"[Etap 1] Zaszyfrowano: {input_path} -> {output_path}")
    else:
        print(f"[Etap 1] Odszyfrowano: {input_path} -> {output_path}")