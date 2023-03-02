import logging
import os
import zipfile
from pathlib import Path
from shutil import move, rmtree
from threading import Thread
from checking import NameCheck
from pretty_view import SortDirView


class SortDirectory:
    EXTENSIONS = {
        "images": ["JPEG", "PNG", "JPG", "SVG", "BMP"],
        "videos": ["AVI", "MP4", "MOV", "MKV"],
        "documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX", "RTF", "XLS"],
        "music": ["MP3", "OGG", "WAV", "AMR"],
        "archives": ["ZIP", "GZ", "TAR", "RAR", "7Z"],
        "programming": ["PY", "PHP", "HTML", "JS", "CSS"],
        "others": []
    }
    known_extensions = []
    unknown_extensions = []
    folders = []
    created_folders = []

    def __init__(self):
        self.name = NameCheck()
        self.sort = SortDirView()

    def create_dirs(self, start_path) -> None:
        for folder in self.EXTENSIONS.keys():
            try:
                (start_path / folder).mkdir(exist_ok=True)
            except FileExistsError:
                pass

    def grabs_folder(self, start_path: Path):
        for el in start_path.iterdir():
            if el.is_dir():
                self.folders.append(el)
        return self.folders

    def copy_files(self, folder, start_path: Path):
        for current_dir, dirs, files in os.walk(folder):
            for file in files:
                ext = str(Path(file).suffix[1:]).upper()
                if ext in self.EXTENSIONS["archives"]:
                    try:
                        with zipfile.ZipFile(os.path.join(current_dir, file), "r") as zip_ref:
                            zip_ref.extractall(start_path / "archives")
                            os.remove(os.path.join(current_dir, file))
                    except zipfile.BadZipFile as e:
                        logging.error(f"{e}. File {file} in {current_dir} is corrupted")
                else:
                    found_folder = False
                    for folder_name, extensions in self.EXTENSIONS.items():
                        if ext in extensions:
                            found_folder = True
                            try:
                                if not (start_path / folder_name).exists():
                                    (start_path / folder_name).mkdir(exist_ok=True)
                                move(os.path.join(current_dir, file), start_path / folder_name / file)
                                os.rename(start_path / folder_name / file, start_path / folder_name / self.name.check(file))
                                break
                            except Exception as error:
                                print(error)
                    if not found_folder:
                        if not (start_path / "others").exists():
                            (start_path / "others").mkdir(exist_ok=True)
                        move(os.path.join(current_dir, file), start_path / "others" / file)
                        os.rename(start_path / "others" / file, start_path / "others" / self.name.check(file))

    def delete_dirs(self, start_path):
        for root, dirs, files in os.walk(start_path, topdown=False):
            for direct in dirs:
                if direct not in self.EXTENSIONS.keys():
                    dir_path = os.path.join(start_path, direct)
                    try:
                        rmtree(dir_path, ignore_errors=True)
                    except PermissionError:
                        print("Permission error for delete", dir_path)

    def extensions(self, start_path):
        known_extensions = []
        unknown_extensions = []
        for current_dir, dirs, files in os.walk(start_path):
            for file in files:
                ext = str(Path(file).suffix[1:]).upper()
                if Path(current_dir).name == 'others':
                    if ext not in unknown_extensions:
                        unknown_extensions.append(ext)
                else:
                    if ext not in known_extensions:
                        known_extensions.append(ext)
        result = [
            "\n".join(i for i in known_extensions),
            "\n".join(i for i in unknown_extensions if i)
            ]
        return print(self.sort.create_row(result))


def threading():
    start_path = Path(input("Input path: "))
    x = SortDirectory()
    x.create_dirs(start_path)
    x.grabs_folder(start_path)
    threads = []
    for folder in x.folders:
        th = Thread(target=x.copy_files, args=(folder, start_path))
        th.start()
        threads.append(th)
    [th.join() for th in threads]
    x.delete_dirs(start_path)
    x.extensions(start_path)
    print('>>>>>>>>>>  Сортування закінчено!  <<<<<<<<<<')


def run_sort():
    try:
        threading()
        while True:
            b = input("\nDo you want to sort something else? (y/n)\n>>>> ")
            if b == "y":
                threading()
                continue
            if b == "n":
                print("Goodbye!")
                break
            else:
                print("The answer must be y/n")
    except (IndexError, FileNotFoundError, Exception) as error:
        print(error)
        pass


if __name__ == "__main__":
    run_sort()
