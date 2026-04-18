import numpy as np
from PIL import Image
    
def naive_scrambling(input_path, output_path, key):
    img = Image.open(input_path)
    img_array = np.array(img)
    
    height, width = img_array.shape[:2]
    scrambling_array = np.zeros_like(img_array)
    
    for i in range(height):
        shift = (abs(key) + i * (abs(key) % 10 + 1)) % width
        shift = shift if key > 0 else -shift
        scrambling_array[i] = np.roll(img_array[i], shift, axis=0)
        
    scrambling_img = Image.fromarray(scrambling_array)
    scrambling_img.save(output_path)
    if key > 0:
        print(f"[Etap 1] Zaszyfrowano: {input_path} -> {output_path}")
    else:
        print(f"[Etap 1] Odszyfrowano: {input_path} -> {output_path}")