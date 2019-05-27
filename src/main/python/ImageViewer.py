'''
イメージを表示する画面
MainWindowの代わり
'''
from PyQt5 import QtWidgets, QtCore, QtGui
from ImagePaths import ImagePaths
from ImageViewScene import ImageViewScene

class ImageViewer( QtWidgets.QGraphicsView ):
        def __init__(self):
                super().__init__()

                self.image_paths =  ImagePaths()
                self.image_view_scene = None # TODO クラスを作る
                self.window_height = 400.0
                self.window_width = 600.0

                self.set_imageViewer()
                self.initMenu()

        def set_imageViewer(self):
                # フラグセット
                self.setWindowFlags(QtCore.Qt.CustomizeWindowHint) # タイトルバーを消す
                self.setFixedSize(self.window_width, self.window_height)

                # QGraphicsViewの設定
                self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)        
                self.setRenderHints(QtGui.QPainter.Antialiasing |
                        QtGui.QPainter.SmoothPixmapTransform |
                        QtGui.QPainter.TextAntialiasing
                )

                # QGraphicsSceneの作成・および設定.
                scene = None  # TODO viewを作る
                # scene.setSceneRect( QtWidgets.QRectF( self.rect()))
                # self.setScene( scene )
            
        def initMenu(self):
            pass # TODO メニューを作る


        def resizeEvent( self, event ):
             # ビューをリサイズ時にシーンの矩形を更新する
             super().resizeEvent( event )   
             self.scene().setSceneRect(QtWidgets.QRectF(self.rect()))


        def set_ImagePaths( self, filepath ):
            # TODO ここに色々追加する
            # ビューが持つシーンにファイルパスを渡して初期化処理を
            # 実行するメソッド。
            self.image_view_scene.setFile(filepath)
            self.setAlignment(QtCore.Qt.AlignRight)

        def start_slideshow( self ):
            pass # TODO 