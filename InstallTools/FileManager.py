from pathlib import Path
import os
import shutil

HERE = Path(__file__).parent.resolve()
HERE_STR = str(HERE)


class FileManager:
    def __init__(self, path: (Path, str) = None):
        if type(path) is str:
            path = Path(path)
        if path is None:
            path = HERE
        if not path.exists():
            raise FileNotFoundError
        self.__path = path

    @staticmethod
    def __DirExists(dirname: str, path: str = None) -> bool:
        if path is None:
            path = HERE_STR
        return dirname in [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    @staticmethod
    def __FileExists(filename: str, path: str = None) -> bool:
        try:
            if path is None:
                path = HERE_STR
            f = open(path + "\\" + filename)
            f.close()
            return True
        except FileNotFoundError:
            return False

    @staticmethod
    def PathExists(path: str):
        return Path(path).exists()

    @property
    def path(self) -> str:
        return str(self.__path)

    @property
    def object(self):
        return self.__path

    @property
    def directory(self):
        return self.__path.name

    def GetDirectory(self):
        return self.directory if self.directory != "" else self.path

    def GetPath(self):
        return self.path

    def GoInsideDirectory(self, dirname: str) -> bool:
        if self.__DirExists(dirname, self.path):
            self.__path /= dirname
            return True
        return False

    def GoOutsideDirectory(self):
        self.__path = self.__path.parent
        return True

    def OpenFile(self, filename: str, mode: str = "r"):
        if self.__FileExists(filename, self.path):
            return open(self.__path / filename, mode)

    def GetDirectories(self) -> list:
        return [d for d in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, d))]

    def DirectoryExists(self, dirname: str) -> bool:
        return self.__DirExists(dirname, self.path)

    def CreateDirectory(self, dirname: str) -> bool:
        if self.__DirExists(dirname, self.path):
            return False
        os.mkdir(str(self.__path / dirname))
        return True

    def DeleteDirectory(self, dirname: str) -> bool:
        if self.__DirExists(dirname, self.path):
            shutil.rmtree(str(self.__path / dirname))
            return True
        return False

    def DeleteThisDirectory(self):
        directory = self.directory
        self.GoOutsideDirectory()
        return self.DeleteDirectory(directory)

    def DeleteThisContent(self):
        directory = self.directory
        out = self.GoOutsideDirectory()
        delete = self.DeleteDirectory(directory)
        create = self.CreateDirectory(directory)
        go_in = self.GoInsideDirectory(directory)
        return all([out, delete, create, go_in])

    def GetFiles(self):
        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

    def FileExists(self, filename: str) -> bool:
        return self.__FileExists(filename, self.path)

    def CreateFile(self, filename: str) -> bool:
        if self.__FileExists(filename, self.path):
            return False
        open(str(self.__path / filename), "x").close()
        return True

    def DeleteFile(self, filename: str) -> bool:
        if self.__FileExists(filename, self.path):
            os.remove(str(self.__path / filename))
            return True
        return False

    def CopyDirectory(self, dirname: str, new_path) -> bool:
        fm = FileManager(new_path)
        if fm.DirectoryExists(dirname):
            return False
        fm.CreateDirectory(dirname)
        try:
            shutil.copytree(self.object / dirname, Path(new_path) / dirname)
            return True
        except OSError:
            return False

    def CopyFile(self, filename: str, new_path) -> bool:
        fm = FileManager(new_path)
        if fm.FileExists(filename):
            return False
        try:
            shutil.copy2(self.object / filename, Path(new_path) / filename)
            return True
        except OSError:
            return False

    def CopyDirectoryContents(self, dirname: str, new_path):
        if not self.GoInsideDirectory(dirname):
            return
        for directory in self.GetDirectories():
            self.CopyDirectory(directory, new_path)
        for file in self.GetFiles():
            self.CopyFile(file, new_path)
        self.GoOutsideDirectory()

    def CopyContents(self, new_path):
        for directory in self.GetDirectories():
            self.CopyDirectory(directory, new_path)
        for file in self.GetFiles():
            self.CopyFile(file, new_path)

    def RenameFile(self, filename: str, new_filename: str) -> bool:
        if not self.FileExists(filename) or self.FileExists(new_filename):
            return False
        os.rename(str(self.__path / filename), str(self.__path / new_filename))
        return True

    def RenameDirectory(self, dirname: str, new_dirname: str) -> bool:
        if not self.DirectoryExists(dirname) or self.DirectoryExists(new_dirname):
            return False
        os.rename(str(self.__path / dirname), str(self.__path / new_dirname))
        return True

    def Relocate(self, path: str):
        if path[-1] == ":":
            path += self.object.root
        if FileManager.PathExists(path):
            self.__path = Path(path)
            return True
        return False
