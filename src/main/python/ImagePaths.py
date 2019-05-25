'''
指定されたディレクトリの下のファイルのパスをもつオブジェクト
'''
import os
from PyQt5 import QtCore

class ImagePaths( QtCore.QObject ):

    def __init__(self):
        super().__init__()

        self.__path_list = [] # 読み取り専用

    @property
    def path_list(self): # path_listのゲッタ
        return self.__path_list


    def make_list(self, dir_path: str) -> None :

        # __path_listに先に入っていたら消す
        if self.__path_list:
            self.__path_list.clear()

        # dir_path以下のファイルの名前を所得
        tmp_file_list = os.listdir(dir_path)

        # サポートする拡張子のファイルだけself.__path_listに追加
        valid_extensions = ['.JPG', '.JPEG', '.PNG', '.GIF'] # 拡張子の頻出順にすることで高速化を期待
        for file in tmp_file_list:
            for valid_extension in valid_extensions:
                extension = os.path.splitext(file) # 拡張子以外と拡張子に分ける

                if valid_extension == extension[1].upper():
                    self.__path_list.append(dir_path + os.sep + file)
                    break