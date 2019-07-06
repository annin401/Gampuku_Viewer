from PyQt5 import QtWidgets, QtGui

class ImageViewScene( QtWidgets.QGraphicsScene ):

    def __init__(self, width: float, height: float):
        super().__init__()
        self.__imageItem = None
        self.__secene_width = width
        self.__scene_height = height

    def set_secene_size(self, width: float, height: float):
        self.__secene_width = width
        self.__scene_height = height


    def set_file(self, filepath: str) -> None :

        # 既にシーンにPixmapアイテムがある場合は削除する。
        if self.__imageItem:
            self.removeItem(self.__imageItem)

        # イメージを所得
        pixmap = QtGui.QPixmap(filepath)
        # イメージをPixmapアイテムとしてシーンに追加する
        item = QtWidgets.QGraphicsPixmapItem(pixmap)

        self.addItem(item)
        self.__imageItem = item

        # 画像をscheneのサイズに合うようにリサイズする
        self.fit_image()


    def fit_image(self):
        
        if not self.__imageItem:
            return

        # sceneのサイズを指定
        self.setSceneRect(0.0, 0.0, self.__secene_width, self.__scene_height)

        # イメージの元の大きさを持つRectオブジェクト
        boundingRect = self.__imageItem.boundingRect()
        # シーンの現在の大きさを持つRectオブジェクト
        sceneRect = self.sceneRect()

        # それぞれの辺の比を求める
        itemAspectRatio = boundingRect.width() / boundingRect.height()
        sceneAspectRatio = sceneRect.width() / sceneRect.height()

        if itemAspectRatio >= sceneAspectRatio:
            # 横幅に合うようにフィット
            scaleRatio = sceneRect.width() / boundingRect.width()
        else:
            # 縦幅に合うようにフィット
            scaleRatio = sceneRect.height() / boundingRect.height()

        # 最終的にイメージのアイテムに適応するためのオブジェクト
        transform = QtGui.QTransform()

        # アスペクト比からスケール比を割り出しTransformオブジェクトに適応
        transform.scale(scaleRatio, scaleRatio)

        #変換されたオブジェクトをイメージに適応
        self.__imageItem.setTransform(transform)


        # 中央に配置する処理
        # ほんとは違うメソッドにした方が良いが比の再計算をしたくないため分けてない
        if itemAspectRatio >= sceneAspectRatio:
            # 横幅に合わせた場合
            # 変形後の画像の横幅を所得
            height_after_transforme = boundingRect.height() * scaleRatio

            # 中央の座標を所得
            # viewの縦の長さ - 画像　/ 2　で中心の座標を求めてる
            centerPos = (self.height() / 2) - (height_after_transforme / 2)

            # 画像を移動
            self.__imageItem.setPos(0, centerPos)

        else:
            # 縦幅に合わせた場合
            # 変形後の画像の横幅を所得
            width_after_transforme = boundingRect.width() * scaleRatio

            # 中央の座標を所得
            # viewの横の長さ - 画像　/ 2　で中心の座標を求めてる
            centerPos = (self.width() / 2) - (width_after_transforme / 2)

            # 画像を移動
            self.__imageItem.setPos(centerPos, 0)