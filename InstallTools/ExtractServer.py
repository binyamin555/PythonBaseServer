from shutil import unpack_archive
from pathlib import Path
from FileManager import FileManager


HERE = Path(__file__).parent.resolve()
pyserver_path = "PyServer"
path__to_server = str((HERE / pyserver_path).resolve())


def extract(filename, tmp_dir):
    fm = FileManager()
    fm.GoInsideDirectory(tmp_dir)
    if fm.DirectoryExists(pyserver_path):
        fm.DeleteDirectory(pyserver_path)

    unpack_archive(filename, path__to_server)
