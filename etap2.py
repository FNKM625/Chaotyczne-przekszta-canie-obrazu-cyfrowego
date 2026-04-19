# etap2.py
import numpy as np
from PIL import Image


def generatepermutation(pixelcount, key):
    rng = np.random.default_rng(key)
    permutation = rng.permutation(pixelcount)
    inversepermutation = np.argsort(permutation)
    return permutation, inversepermutation


def buildmappingtext(permutation, inversepermutation, key, count=10):
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


def buildcomparisontext(pixelcount, key, count=10):
    permutation_key, inverse_key = generatepermutation(pixelcount, key)
    permutation_key1, inverse_key1 = generatepermutation(pixelcount, key + 1)

    limit = min(count, pixelcount)
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
        lines.append(f"P^-1_key(P_key({i})+1) = {inverse_key1[(permutation_key[i]+1) % pixelcount]}")

    return "\n".join(lines)


def purepermutation(inputpath, outputpath, key, encrypt=True):
    img = Image.open(inputpath)
    imgarray = np.array(img)
    originalshape = imgarray.shape

    if len(originalshape) == 2:
        flatpixels = imgarray.reshape(-1, 1)
    else:
        flatpixels = imgarray.reshape(-1, originalshape[2])

    pixelcount = flatpixels.shape[0]
    permutation, inversepermutation = generatepermutation(pixelcount, key)

    if encrypt:
        transformedflat = flatpixels[permutation]
    else:
        transformedflat = flatpixels[inversepermutation]

    if len(originalshape) == 2:
        resultarray = transformedflat.reshape(originalshape[0], originalshape[1])
    else:
        resultarray = transformedflat.reshape(originalshape)

    resultimg = Image.fromarray(resultarray)
    resultimg.save(outputpath)

    if encrypt:
        print(f"[Etap 2] Scrambling zakończony: {inputpath} -> {outputpath}, klucz = {key}")
    else:
        print(f"[Etap 2] Unscrambling zakończony: {inputpath} -> {outputpath}, klucz = {key}")