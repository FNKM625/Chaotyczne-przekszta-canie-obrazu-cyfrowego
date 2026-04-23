import numpy as np
from PIL import Image
from etap2 import generate_permutation as gperm

def generate_substitution_value(key):
    return (key * 7 + 31) % 256

def build_comparison_text(pixel_count, key, count=10):
    permutation_key, inverse_key = gperm(pixel_count, key)
    permutation_key1, inverse_key1 = gperm(pixel_count, key + 1)

    shift_key = generate_substitution_value(key)
    shift_key1 = generate_substitution_value(key + 1)

    limit = min(count, pixel_count)
    lines = []

    lines.append("ETAP 3 - HYBRYDA (PERMUTACJA + SUBSTYTUCJA)")
    lines.append("")
    lines.append(f"Klucz poprawny: {key}")
    lines.append(f"Klucz błędny: {key + 1}")
    lines.append(f"Substytucja dla key: x -> (x + {shift_key}) mod 256")
    lines.append(f"Substytucja dla key+1: x -> (x + {shift_key1}) mod 256")
    lines.append("")

    lines.append("1. Permutacja dla key")
    for i in range(limit):
        lines.append(f"P_key({i}) = {permutation_key[i]}")

    lines.append("")
    lines.append("2. Poprawne odtwarzanie indeksów")
    for i in range(limit):
        lines.append(f"P^-1_key(P_key({i})) = {inverse_key[permutation_key[i]]}")

    lines.append("")
    lines.append("3. Próba odtworzenia złym kluczem")
    for i in range(limit):
        lines.append(f"P^-1_key+1(P_key({i})) = {inverse_key1[permutation_key[i]]}")

    lines.append("")
    lines.append("4. Przykład substytucji wartości")
    sample_values = [0, 32, 64, 128, 200]
    for x in sample_values:
        y = (x + shift_key) % 256
        restored = (y - shift_key) % 256
        wrong_restored = (y - shift_key1) % 256
        lines.append(
            f"x={x} -> y={y} -> poprawnie={restored}, błędnym kluczem={wrong_restored}"
        )

    return "\n".join(lines)

def hybrid_scrambling(input_path, output_path, key, is_encrypt=True):
    img = Image.open(input_path)
    img_array = np.array(img)
    original_shape = img_array.shape

    if len(original_shape) == 2:
        flat_pixels = img_array.reshape(-1, 1)
    else:
        flat_pixels = img_array.reshape(-1, original_shape[2])

    pixel_count = flat_pixels.shape[0]
    permutation, inverse_permutation = gperm(pixel_count, key)
    substitution_value = generate_substitution_value(key)

    if is_encrypt:
        permuted = flat_pixels[permutation].astype(np.uint16)
        transformed = (permuted + substitution_value) % 256
    else:
        unsubstituted = (flat_pixels.astype(np.uint16) - substitution_value) % 256
        transformed = unsubstituted[inverse_permutation]

    transformed = transformed.astype(np.uint8)

    if len(original_shape) == 2:
        result_array = transformed.reshape(original_shape[0], original_shape[1])
    else:
        result_array = transformed.reshape(original_shape)

    result_img = Image.fromarray(result_array)
    result_img.save(output_path)

    if is_encrypt:
        print(f"[Etap 3] Scrambling zakończony: {input_path} -> {output_path}, klucz = {key}")
    else:
        print(f"[Etap 3] Unscrambling zakończony: {input_path} -> {output_path}, klucz = {key}")