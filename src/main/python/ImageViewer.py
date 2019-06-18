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
        self.initial_pos = QtCore.QPoint(400, 200) # TODO ディスプレー右下に表示させる

        self.init_imageViewer()

        # for slideshow
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update) 
        self.update_interval = 2000 # ミリ秒
        self.path_index = 0

        # for status when dragging
        self.STATUS_NORMAL = 0
        self.STATUS_MOVEABLE = 1
        self.dragging_status = self.STATUS_NORMAL
        # for move action when dragging 
        self.current_pos = self.initial_pos
        self.clicked_pos = QtCore.QPoint()

        # for context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.init_context_menu)

    def init_imageViewer(self):

        # フラグセット
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # タイトルバーを消す
        self.setFixedSize(self.window_width, self.window_height) # サイズを固定
        self.move(self.initial_pos) # ウィンドの場所を移動
        # TODO 初期位置右下にする

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

    def init_context_menu(self):

        # アクションの設定
        open_folder = QtWidgets.QAction("フォルダーを開く")
        open_folder.triggered.connect(self.stop_slideshow)
        open_folder.triggered.connect(self.show_set_Dialog)
        open_folder.triggered.connect(self.start_slideshow)

        open_environmental_setting = QtWidgets.QAction("環境設定を開く")

        exit_action = QtWidgets.QAction("終了")
        exit_action.triggered.connect(self.close)

        # メニューを構築
        self.menu = QtWidgets.QMenu()
        self.menu.addAction(open_folder)
        self.menu.addAction(open_environmental_setting)
        self.menu.addSection("")
        self.menu.addAction(exit_action)

        # メニューを表示
        self.menu.exec_(QtGui.QCursor.pos()) # マウスの座標を引数に渡す

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

        # 初期化
        self.path_index = 0

        # 画像更新をする関数を呼び出すタイマーをスタートする
        self.timer.start(self.update_interval)

        # 最初に表示する画像をセットする
        self.update()

    def stop_slideshow(self):

        # 画像更新をする関数を呼び出すタイマーをストップする 
        self.timer.stop()

    def update(self):

        # インデックスが最後まで到達したら最初に戻す
        if self.path_index == len(self.image_paths):
            self.path_index = 0

        # 画像をセットする
        self.scene().set_file( self.image_paths[self.path_index] )

        # インデックスを更新
        self.path_index += 1 

    def resizeEvent(self, event):

        # ビューをリサイズ時にシーンの矩形を更新する
        super().resizeEvent( event )   
        self.scene().setSceneRect(QtCore.QRectF(self.rect()))


    '''
    mouseEventの関数群で,四隅のドラッグでリサイズを,それ以外の場所でのドラッグで
    移動を実装している
    それぞれ別の関数に分けたほうがいい気がするが，ライブラリが用意したイベントハンドラ
    の関係で分けれていない
    '''

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:

            # ウィンドウの移動のための設定
            self.dragging_status = self.STATUS_MOVEABLE
            self.clicked_pos = event.pos() # ウィンドの左上を(0,0)にした相対位置
            self.setCursor(QtCore.Qt.ClosedHandCursor) # カーソルを掴む手の絵に変更

    def mouseMoveEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:

            if self.dragging_status == self.STATUS_MOVEABLE:
                # マウスの移動距離を求める
                distance = event.pos() - self.clicked_pos
                # 現在位置を更新
                self.current_pos += distance 
                self.move(self.current_pos)

    def mouseReleaseEvent(self, event):

        self.dragging_status = self.STATUS_NORMAL
        self.unsetCursor()# カーソルを元に戻す

# for debug
app = QtWidgets.QApplication([])
v = ImageViewer()
v.show()
v.show_set_Dialog()
v.start_slideshow()
import sys
sys.exit(app.exec_())
