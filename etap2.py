# etap2.py
import numpy as np
from PIL import Image

def generate_permutation(pixel_count, key):
    rng = np.random.default_rng(key)
    permutation = rng.permutation(pixel_count)
    inversepermutation = np.argsort(permutation)
    return permutation, inversepermutation

def build_mapping_text(permutation, inversepermutation, key, count=10):
    lines = []
    limit = min(count, len(permutation))

    lines.append(f"Klucz: {key}")
    lines.append("Przykładowe odwzorowania permutacji:")
    for i in range(limit):
        lines.append(f"P({i}) = {permutation[i]}")

    lines.append("")
    lines.append("Przykładowe odwzorowania permutacji odwrotnej:")
    for i in range(limit):
        lines.append(f"P^-1({i}) = {inversepermutation[i]}")

    lines.append("")
    lines.append("Sprawdzenie P^-1(P(i)) = i:")
    for i in range(limit):
        lines.append(f"P^-1(P({i})) = {inversepermutation[permutation[i]]}")

    return "\n".join(lines)

def build_comparison_text(pixel_count, key, count=10):
    permutation_key, inverse_key = generate_permutation(pixel_count, key)
    permutation_key1, inverse_key1 = generate_permutation(pixel_count, key + 1)

    limit = min(count, pixel_count)
    lines = []

    lines.append("ETAP 2 - CZYSTA PERMUTACJA")
    lines.append("")
    lines.append(f"Klucz poprawny: {key}")
    lines.append(f"Klucz błędny:   {key + 1}")
    lines.append("")

    lines.append("1. Permutacja dla key")
    for i in range(limit):
        lines.append(f"P_key({i}) = {permutation_key[i]}")

    lines.append("")
    lines.append("2. Permutacja dla key + 1")
    for i in range(limit):
        lines.append(f"P_key+1({i}) = {permutation_key1[i]}")

    lines.append("")
    lines.append("3. Sprawdzenie poprawnego odtwarzania (key)")
    for i in range(limit):
        lines.append(f"P^-1_key(P_key({i})) = {inverse_key[permutation_key[i]]}")

    lines.append("")
    lines.append("4. Próba odtworzenia złym kluczem (key + 1)")
    for i in range(limit):
        lines.append(f"P^-1_key+1(P_key({i})) = {inverse_key1[permutation_key[i]]}")

    lines.append("")
    lines.append("5. Próba odtworzenia złym parametrem")
    for i in range(limit):
        lines.append(f"P^-1_key(P_key({i})+1) = {inverse_key1[(permutation_key[i]+1) % pixel_count]}")

    return "\n".join(lines)

def pure_permutation(input_path, output_path, key, is_encrypt=True):
    img = Image.open(input_path)
    img_array = np.array(img)
    original_shape = img_array.shape

    if len(original_shape) == 2:
        flat_pixels = img_array.reshape(-1, 1)
    else:
        flat_pixels = img_array.reshape(-1, original_shape[2])

    pixel_count = flat_pixels.shape[0]
    permutation, inverse_permutation = generate_permutation(pixel_count, key)

    if is_encrypt:
        transformed_flat = flat_pixels[permutation]
    else:
        transformed_flat = flat_pixels[inverse_permutation]

    if len(original_shape) == 2:
        result_array = transformed_flat.reshape(original_shape[0], original_shape[1])
    else:
        result_array = transformed_flat.reshape(original_shape)

    result_img = Image.fromarray(result_array)
    result_img.save(output_path)

    if is_encrypt:
        print(f"[Etap 2] Scrambling zakończony: {input_path} -> {output_path}, klucz = {key}")
    else:
        print(f"[Etap 2] Unscrambling zakończony: {input_path} -> {output_path}, klucz = {key}")