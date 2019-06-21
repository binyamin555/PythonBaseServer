from ExtractServer import extract
from DownloadFromServer import download, tmp
from FileManager import FileManager


if __name__ == '__main__':
    target_name = "PyServerBuildV1.0.2"
    path = download(target_name)
    extract(path, tmp)
    fm = FileManager()
    print(fm.path)
    FileManager().DeleteDirectory(tmp)
