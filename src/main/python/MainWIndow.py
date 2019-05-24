from PyQt5 import QtWidgets

class MainWindow( QtWidgets.QMainWindow ):

    def __init__(self):
        super().__init__()

        self.image_path = None # TODO クラスを作る
        self.image_view_scene = None # TODO クラスを作る
        self.image_viewer = None # TODO QGrapphicsView を入れる

        self.initUI()

    def initUI(self):

        self.contextMenu =  None # TODO コンテキストメニュー を作って入れる

    def set_file(self, filepath):
        pass # TODO

    def start_slideshow(self):
        pass # TODO