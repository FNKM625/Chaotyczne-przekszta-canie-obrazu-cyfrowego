import numpy as np
from PIL import Image


def generate_permutation(pixel_count, key):
    np.random.seed(key)

    permutation = np.arange(pixel_count)
    permutation = knuth_shuffle(pixel_count, permutation)
    
    inverse_permutation = np.argsort(permutation)
    return permutation, inverse_permutation


def knuth_shuffle(pixel_count, permutation):
    for i in range(pixel_count - 1, 0, -1):
        j = np.random.randint(i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    return permutation


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


def apply_permutation_array(img_array, key, is_encrypt=True):
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

    return transformed_flat.reshape(original_shape)


def build_mapping_text(permutation, inverse_permutation, key, count=10):
    lines = []
    limit = min(count, len(permutation))

    lines.append(f"Klucz: {key}")
    lines.append("Przykładowe odwzorowania permutacji:")
    for i in range(limit):
        lines.append(f"P({i}) = {permutation[i]}")

    lines.append("")
    lines.append("Przykładowe odwzorowania permutacji odwrotnej:")
    for i in range(limit):
        lines.append(f"P^-1({i}) = {inverse_permutation[i]}")

    lines.append("")
    lines.append("Sprawdzenie P^-1(P(i)) = i:")
    for i in range(limit):
        lines.append(f"P^-1(P({i})) = {inverse_permutation[permutation[i]]}")

    return "\n".join(lines)


def build_comparison_text(img_array, key, wrong_key, count=10):
    original_shape = img_array.shape

    if len(original_shape) == 2:
        flat_pixels = img_array.reshape(-1, 1)
    else:
        flat_pixels = img_array.reshape(-1, original_shape[2])

    pixel_count = flat_pixels.shape[0]

    permutation_key, inverse_key = generate_permutation(pixel_count, key)
    permutation_key1, inverse_key1 = generate_permutation(pixel_count, wrong_key)

    scrambled_array = apply_permutation_array(img_array, key, True)
    wrong_unscrambled_array = apply_permutation_array(scrambled_array, wrong_key, False)

    corr_orig_h, corr_orig_v = adjacent_pixel_correlation(img_array)
    corr_scr_h, corr_scr_v = adjacent_pixel_correlation(scrambled_array)

    mad_wrong, mse_wrong = image_difference_metrics(img_array, wrong_unscrambled_array)

    limit = min(count, pixel_count)
    lines = []

    lines.append("ETAP 2 - CZYSTA PERMUTACJA")
    lines.append("")
    lines.append(f"Klucz poprawny: {key}")
    lines.append(f"Klucz błędny: {wrong_key}")
    lines.append("")

    lines.append("1. Permutacja dla key")
    for i in range(limit):
        lines.append(f"P_key({i}) = {permutation_key[i]}")

    lines.append("")
    lines.append("2. Permutacja dla wrong_key")
    for i in range(limit):
        lines.append(f"P_wrong_key({i}) = {permutation_key1[i]}")

    lines.append("")
    lines.append("3. Sprawdzenie poprawnego odtwarzania (key)")
    for i in range(limit):
        lines.append(f"P^-1_key(P_key({i})) = {inverse_key[permutation_key[i]]}")

    lines.append("")
    lines.append("4. Próba odtworzenia złym kluczem (wrong_key)")
    for i in range(limit):
        lines.append(f"P^-1_wrong_key(P_wrong_key({i})) = {inverse_key[permutation_key1[i]]}")

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


def pure_permutation(input_path, output_path, key, is_encrypt=True):
    img = Image.open(input_path)
    img_array = np.array(img)

    result_array = apply_permutation_array(img_array, key, is_encrypt)

    result_img = Image.fromarray(result_array)
    result_img.save(output_path)

    if is_encrypt:
        print(f"[Etap 2] Scrambling zakończony: {input_path} -> {output_path}, klucz = {key}")
    else:
        print(f"[Etap 2] Unscrambling zakończony: {input_path} -> {output_path}, klucz = {key}")