"""
Moduł obliczający sumę kontrolną SHA256 dla każdego pliku w katalogu,
z wykorzystaniem multiprocessing.Pool do równoległego przetwarzania.

Źródła i dokumentacja:
- hashlib: https://docs.python.org/3/library/hashlib.html
- multiprocessing.Pool: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
"""

import os
import hashlib
from multiprocessing import Pool
from typing import Dict, List, Tuple


def sha256_for_file(filepath: str) -> Tuple[str, str]:
    """
    Oblicza sumę kontrolną SHA256 dla pojedynczego pliku.

    Args:
        filepath (str): Ścieżka do pliku.

    Returns:
        Tuple[str, str]: Krotka zawierająca nazwę pliku i jego hash SHA256.
    """
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    filename = os.path.basename(filepath)
    return filename, sha256_hash.hexdigest()


def get_files_in_directory(directory: str) -> List[str]:
    """
    Zwraca listę pełnych ścieżek do plików w danym katalogu.

    Args:
        directory (str): Ścieżka do katalogu.

    Returns:
        List[str]: Lista ścieżek do plików.
    """
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def main() -> None:
    """
    Główna funkcja programu.
    Pobiera listę plików z katalogu, oblicza ich sumy SHA256 równolegle,
    a następnie drukuje słownik z nazwami plików i ich hashami.
    """
    directory = os.getcwd()  # aktualny katalog
    files = get_files_in_directory(directory)

    with Pool() as pool:
        results = pool.map(sha256_for_file, files)

    # Tworzymy słownik nazwa_pliku: hash
    hashes: Dict[str, str] = dict(results)

    print(hashes)


if __name__ == "__main__":
    main()
