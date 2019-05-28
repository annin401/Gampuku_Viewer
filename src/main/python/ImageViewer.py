'''
イメージを表示する画面
MainWindowの代わり
'''
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from ImagePaths import ImagePaths
from ImageViewScene import ImageViewScene

class ImageViewer( QtWidgets.QGraphicsView ):
        def __init__(self):
                super().__init__()

                self.image_paths =  ImagePaths()
                self.window_height = 400.0
                self.window_width = 600.0

                self.set_imageViewer()
                self.init_menu()

        def set_imageViewer(self):
                # フラグセット
                self.setWindowFlags(QtCore.Qt.CustomizeWindowHint) # タイトルバーを消す
                self.setFixedSize(self.window_width, self.window_height) # サイズを固定

                # QGraphicsViewの設定
                self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)        
                self.setRenderHints(QtGui.QPainter.Antialiasing |
                        QtGui.QPainter.SmoothPixmapTransform |
                        QtGui.QPainter.TextAntialiasing
                )

                # QGraphicsSceneの作成・および設定.
                scene = ImageViewScene(self.window_width, self.window_height)
                scene.setSceneRect( QtCore.QRectF( self.rect()))
                self.setScene(scene)
            
        def init_menu(self):
            pass # TODO メニューを作る


        def resize_event(self, event):
             # ビューをリサイズ時にシーンの矩形を更新する
             super().resizeEvent( event )   
             self.scene().setSceneRect(QtCore.QRectF(self.rect()))


        def set_ImagePaths(self):

            # ファイルダイアログを表示
            dirpath = QtWidgets.QFileDialog.getExistingDirectory(self,
                'Select Folder', os.path.expanduser('~'),
                )

            # 画像パスのリストを生成
            self.image_paths.make_list(dirpath)

        def start_slideshow(self):
            pass # TODO 
            # ビューが持つシーンにファイルパスを渡す
            # self.scene().setFile(filepath)

# for debug
# app = QtWidgets.QApplication([])
# i = ImageViewer()
# i.show()
# i.set_ImagePaths()
# print(i.image_paths.path_list)
# import sys
# sys.exit( app.exec_() )