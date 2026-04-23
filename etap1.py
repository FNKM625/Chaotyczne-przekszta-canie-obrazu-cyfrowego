import numpy as np
from PIL import Image


def calculate_shift(row_index, key, width):
    return (key + row_index * (key % 10 + 1)) % width


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


def scramble_array(img_array, key, is_encrypt=True):
    height, width = img_array.shape[:2]
    result_array = np.zeros_like(img_array)

    for i in range(height):
        shift = calculate_shift(i, key, width)
        result_array[i] = np.roll(img_array[i], (shift if is_encrypt else -shift), axis=0)

    return result_array


def build_comparison_text(img_array, key, count=10):
    height, width = img_array.shape[:2]
    limit = min(count, height)

    scrambled_array = scramble_array(img_array, key, True)
    wrong_unscrambled_array = scramble_array(scrambled_array, key + 1, False)

    corr_orig_h, corr_orig_v = adjacent_pixel_correlation(img_array)
    corr_scr_h, corr_scr_v = adjacent_pixel_correlation(scrambled_array)

    mad_wrong, mse_wrong = image_difference_metrics(img_array, wrong_unscrambled_array)

    lines = []

    lines.append("ETAP 1 - NAIWNY SCRAMBLING")
    lines.append("")
    lines.append(f"Klucz poprawny: {key}")
    lines.append(f"Klucz błędny: {key + 1}")
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
            f"wiersz {i}: 0 -> {scrambled_pos} -> {restored_pos}"
        )

    lines.append("")
    lines.append("4. Próba odtworzenia złym kluczem (0 -> po przesunięciu -> po odtworzeniu)")
    for i in range(limit):
        shift_key = calculate_shift(i, key, width)
        shift_key1 = calculate_shift(i, key + 1, width)
        scrambled_pos = (0 + shift_key) % width
        restored_wrong = (scrambled_pos - shift_key1) % width
        lines.append(
            f"wiersz {i}: 0 -> {scrambled_pos} -> {restored_wrong}"
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


def naive_scrambling(input_path, output_path, key, is_encrypt=True):
    img = Image.open(input_path)
    img_array = np.array(img)

    result_array = scramble_array(img_array, key, is_encrypt)

    result_img = Image.fromarray(result_array)
    result_img.save(output_path)

    if is_encrypt:
        print(f"[Etap 1] Scrambling zakończony: {input_path} -> {output_path}, klucz = {key}")
    else:
        print(f"[Etap 1] Unscrambling zakończony: {input_path} -> {output_path}, klucz = {key}")