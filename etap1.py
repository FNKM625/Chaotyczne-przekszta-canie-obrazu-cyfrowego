# etap1.py
import numpy as np
from PIL import Image
    
def naive_scrambling(input_path, output_path, key, shift_info):
    img = Image.open(input_path)
    img_array = np.array(img)
    
    height, width = img_array.shape[:2]
    scrambling_array = np.zeros_like(img_array)
    
    for i in range(height):
        shift = (key + i * (key % 10 + 1)) % width
        scrambling_array[i] = np.roll(img_array[i], shift * shift_info, axis=0)
        
    scrambling_img = Image.fromarray(scrambling_array)
    scrambling_img.save(output_path)
    if shift_info > 0:
        print(f"[Etap 1] Zaszyfrowano: {input_path} -> {output_path}")
    else:
        print(f"[Etap 1] Odszyfrowano: {input_path} -> {output_path}")