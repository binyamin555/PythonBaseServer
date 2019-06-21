from urllib.request import urlretrieve
from FileManager import FileManager, Path


tmp = "tmp"
target = "PyServer.zip"
url = "https://xpo-os.000webhostapp.com/downloads/pyserver/" + target


def download(filename):
    fm = FileManager(Path(__file__).parent)
    if not fm.DirectoryExists(tmp):
        fm.CreateDirectory(tmp)
    fm.GoInsideDirectory(tmp)
    if fm.FileExists(filename):
        fm.DeleteThisContent()
    path, _ = urlretrieve(url, str(fm.object / (filename + ".zip")))
    return path
