"""
Moduł do kopiowania plików z jednego katalogu do drugiego,
używając osobnego wątku dla każdego pliku.
"""

import os
import shutil
import threading
from typing import List


def copy_file(src: str, dst: str) -> None:
    """
    Kopiuje pojedynczy plik z src do dst, wyświetlając komunikaty postępu.

    :param src: Ścieżka do pliku źródłowego.
    :param dst: Ścieżka do pliku docelowego.
    """
    filename = os.path.basename(src)
    print(f"Kopiowanie pliku {filename}...")
    shutil.copy2(src, dst)
    print(f"Ukończono kopiowanie pliku {filename}")


def copy_all_files(src_dir: str, dst_dir: str) -> None:
    """
    Kopiuje wszystkie pliki z katalogu src_dir do katalogu dst_dir
    używając osobnego wątku dla każdego pliku.

    :param src_dir: Katalog źródłowy.
    :param dst_dir: Katalog docelowy.
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    files: List[str] = [
        f for f in os.listdir(src_dir)
        if os.path.isfile(os.path.join(src_dir, f))
    ]

    threads: List[threading.Thread] = []

    for filename in files:
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        thread = threading.Thread(target=copy_file, args=(src_path, dst_path))
        thread.start()
        threads.append(thread)

    # Czekaj na zakończenie wszystkich wątków
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    source_dir = "source_dir"
    dest_dir = "dest_dir"

    copy_all_files(source_dir, dest_dir)

"""
REZULTAT:
Kopiowanie pliku plik1.txt...
Kopiowanie pliku plik2.txt...
Kopiowanie pliku obrazek.png...
Kopiowanie pliku dokument.pdf...
Ukończono kopiowanie pliku dokument.pdf
Ukończono kopiowanie pliku obrazek.png
Ukończono kopiowanie pliku plik1.txt
Ukończono kopiowanie pliku plik2.txt
"""