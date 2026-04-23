import numpy as np
from PIL import Image
from etap2 import generate_permutation


def generate_substitution_value(key):
    return (key * 7 + 31) % 256


def to_grayscale_2d(img_array):
    if img_array.ndim == 2:
        return img_array.astype(np.float64)
    return np.mean(img_array.astype(np.float64), axis=2)


def adjacent_pixel_correlation(img_array):
    gray = to_grayscale_2d(img_array)

    horizontal_x = gray[:, :-1].flatten()
    horizontal_y = gray[:, 1:].flatten()

    vertical_x = gray[:-1, :].flatten()
    vertical_y = gray[1:, :].flatten()

    corr_h = np.corrcoef(horizontal_x, horizontal_y)[0, 1]
    corr_v = np.corrcoef(vertical_x, vertical_y)[0, 1]

    return corr_h, corr_v


def image_difference_metrics(img1, img2):
    a = img1.astype(np.float64)
    b = img2.astype(np.float64)

    mad = np.mean(np.abs(a - b))
    mse = np.mean((a - b) ** 2)

    return mad, mse


def apply_hybrid_array(img_array, key, is_encrypt=True):
    original_shape = img_array.shape

    if len(original_shape) == 2:
        flat_pixels = img_array.reshape(-1, 1)
    else:
        flat_pixels = img_array.reshape(-1, original_shape[2])

    pixel_count = flat_pixels.shape[0]
    permutation, inverse_permutation = generate_permutation(pixel_count, key)
    substitution_value = generate_substitution_value(key)

    if is_encrypt:
        permuted = flat_pixels[permutation].astype(np.uint16)
        transformed = (permuted + substitution_value) % 256
    else:
        unsubstituted = (flat_pixels.astype(np.uint16) - substitution_value) % 256
        transformed = unsubstituted[inverse_permutation]

    transformed = transformed.astype(np.uint8)
    return transformed.reshape(original_shape)


def build_comparison_text(img_array, key, count=10):
    original_shape = img_array.shape

    if len(original_shape) == 2:
        flat_pixels = img_array.reshape(-1, 1)
    else:
        flat_pixels = img_array.reshape(-1, original_shape[2])

    pixel_count = flat_pixels.shape[0]

    permutation_key, inverse_key = generate_permutation(pixel_count, key)
    permutation_key1, inverse_key1 = generate_permutation(pixel_count, key + 1)

    shift_key = generate_substitution_value(key)
    shift_key1 = generate_substitution_value(key + 1)

    scrambled_array = apply_hybrid_array(img_array, key, True)
    wrong_unscrambled_array = apply_hybrid_array(scrambled_array, key + 1, False)

    corr_orig_h, corr_orig_v = adjacent_pixel_correlation(img_array)
    corr_scr_h, corr_scr_v = adjacent_pixel_correlation(scrambled_array)

    mad_wrong, mse_wrong = image_difference_metrics(img_array, wrong_unscrambled_array)

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

    lines.append("")
    lines.append("5. Korelacja sąsiednich pikseli")
    lines.append(f"Przed scramblingiem - pozioma: {corr_orig_h:.6f}")
    lines.append(f"Przed scramblingiem - pionowa: {corr_orig_v:.6f}")
    lines.append(f"Po scramblingu - pozioma: {corr_scr_h:.6f}")
    lines.append(f"Po scramblingu - pionowa: {corr_scr_v:.6f}")

    lines.append("")
    lines.append("6. Różnica obrazu przy unscramblingu błędnym kluczem")
    lines.append(f"Mean Absolute Difference (MAD): {mad_wrong:.6f}")
    lines.append(f"Mean Squared Error (MSE): {mse_wrong:.6f}")

    return "\n".join(lines)


def hybrid_scrambling(input_path, output_path, key, is_encrypt=True):
    img = Image.open(input_path)
    img_array = np.array(img)

    result_array = apply_hybrid_array(img_array, key, is_encrypt)

    result_img = Image.fromarray(result_array)
    result_img.save(output_path)

    if is_encrypt:
        print(f"[Etap 3] Scrambling zakończony: {input_path} -> {output_path}, klucz = {key}")
    else:
        print(f"[Etap 3] Unscrambling zakończony: {input_path} -> {output_path}, klucz = {key}")