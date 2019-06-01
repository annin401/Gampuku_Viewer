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

                # for slideshow
                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self.update) 
                self.update_interval = 2000 # ミリ秒

                # for self.update
                self.path_index = 0

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


        def show_set_Dialog(self):

            # ファイルダイアログを表示
            dirpath = QtWidgets.QFileDialog.getExistingDirectory(self,
                'Select Folder', os.path.expanduser('~'),
                )

            # フォルダーが選択されなかったら終了
            if dirpath == '':
                return 

            # 画像パスのリストを生成
            self.image_paths.make_list(dirpath)

        def start_slideshow(self):

            if not self.image_paths:
                return 

            # 画像更新をする関数を呼び出すタイマーをスタートする
            self.timer.start(self.update_interval)

            # 最初に表示する画像をセットする
            self.update()


        def update(self):

            # インデックスが最後まで到達したら最初に戻す
            if self.path_index == len(self.image_paths):
                self.path_index = 0

            # 画像をセットする
            self.scene().set_file( self.image_paths[self.path_index] )

            # インデックスを更新
            self.path_index += 1 

        def resize_event(self, event):
             # ビューをリサイズ時にシーンの矩形を更新する
             super().resizeEvent( event )   
             self.scene().setSceneRect(QtCore.QRectF(self.rect()))

#for debug 
app = QtWidgets.QApplication([])
i = ImageViewer()
i.show()
i.show_set_Dialog()
i.start_slideshow()
import sys
sys.exit( app.exec_() )
