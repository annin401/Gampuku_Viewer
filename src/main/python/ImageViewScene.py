from PyQt5 import QtWidgets, QtGui

class ImageViewScene( QtWidgets.QGraphicsScene ):

    def __init__(self, width: float, height: float):
                super().__init__()
                self.__imageItem = None
                self.__secene_width = width
                self.__scene_height = height


    def set_file(self, filepath: str) -> None :

        # 既にシーンにPixmapアイテムがある場合は削除する。
        if self.__imageItejm:
        self.removeItem(self.__imageItem)

        # イメージを所得
        pixmap = QtGui.QPixmap(filepath)
        # イメージをPixmapアイテムとしてシーンに追加する
        item = QtWidgets.QGraphicsPixmapItem(pixmap)

        self.addItem(item)
        self.__imageItem = item

        # 画像をscheneのサイズに合うようにリサイズする
        self.fitImage()


    def fitImage(self):
        
        if not self.imageItem:
            return

        # sceneのサイズを指定
        self.setSceneRect(0.0, 0.0, self.__secene_width, self.__scene_height)
