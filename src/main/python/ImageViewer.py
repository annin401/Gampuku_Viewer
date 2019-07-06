'''
イメージを表示する画面
MainWindowの代わり
'''
import os
from enum import Enum, auto
from PyQt5 import QtWidgets, QtCore, QtGui
from ImagePaths import ImagePaths
from ImageViewScene import ImageViewScene
from environmental_setting import environmental_setting

class ImageViewer( QtWidgets.QGraphicsView ):

    def __init__(self):

        super().__init__()

        self.image_paths =  ImagePaths()
        self.window_size = QtCore.QSize(480, 270.0) # px 初期位置
        self.initial_pos = QtCore.QPoint(400, 200) # TODO ディスプレー右下に表示させる
        self.window_setting_flag = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        self.window_opacity = 1.0 

        self.init_imageViewer()

        # for slideshow
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_image) 
        self.update_interval = 2000 # ミリ秒
        self.path_index = 0

        # for status when dragging
        self.pressed_status = Pressed_status.NORMAL
        # for move action when dragging 
        self.current_pos = self.initial_pos
        self.clicked_pos = QtCore.QPoint()

        # for context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.init_context_menu)

        # for environmental_setting
        self.env_window = environmental_setting()


    def init_imageViewer(self):

        # フラグセット
        self.setWindowFlags(self.window_setting_flag) # タイトルバーを消す
        self.setMinimumSize(160, 90) # 最小ウィンドウサイズを設定
        self.setWindowOpacity(self.window_opacity)
        self.move(self.initial_pos) # ウィンドの場所を移動
        self.resize(self.window_size) #　初期ウィンドウサイズを指定
        # TODO 初期位置右下にする

        # QGraphicsViewの設定
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)        
        self.setRenderHints(QtGui.QPainter.Antialiasing |
                QtGui.QPainter.SmoothPixmapTransform |
                QtGui.QPainter.TextAntialiasing
        )

        # QGraphicsSceneの作成・および設定.
        scene = ImageViewScene(self.window_size.width(), self.window_size.height())
        scene.setSceneRect( QtCore.QRectF( self.rect()))
        self.setScene(scene)

    def init_context_menu(self):

        # アクションの設定
        open_folder = QtWidgets.QAction("フォルダーを開く")
        open_folder.triggered.connect(self.stop_slideshow)
        open_folder.triggered.connect(self.show_set_Dialog)
        open_folder.triggered.connect(self.start_slideshow)

        open_environmental_setting = QtWidgets.QAction("環境設定を開く")
        open_environmental_setting.triggered.connect(self.init_environmental_setting)

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

    def init_environmental_setting(self):

        # 環境設定ウィンドウを表示
        self.env_window.show()
        # 画面の一番上に固定されたウィンドウとかぶるので左上に移動
        self.env_window.move(0, 0)

        # env_windowからでるsignalを接続
        self.env_window.update_interval_changed.connect(self.set_update_interval)
        self.env_window.opacity_changed.connect(self.set_opacity)
        self.env_window.window_on_top_state_changed.connect(self.set_window_setting_flag)

    def set_update_interval(self, sec: int)-> None:

        # 秒をミリ秒に直す
        m_sec = sec * 1000
        self.update_interval = m_sec

        self.timer.start(self.update_interval)

    def set_opacity(self, reversed_opacity: int)-> None:

        # 入力では1-opacityの形で与えられる
        # 透明度を小数に直し,opacityを元の形に戻す
        self.window_opacity = 1.0 - float(reversed_opacity) / 100

        if self.window_opacity < 0.05:
            # ウィンドウが不本意に非アクティブになるバグを回避するため
            self.window_opacity = 0.05

        # ウィンドウの透明度を変更
        self.setWindowOpacity(self.window_opacity)

        # フラグを更新するとウィンドウが消えるので再描画
        self.show()

    def set_window_setting_flag(self, state: int)-> None:

        if state == QtCore.Qt.Unchecked:
            self.window_setting_flag = QtCore.Qt.FramelessWindowHint
        elif state == QtCore.Qt.Checked:
            self.window_setting_flag = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint

        # フラグを更新
        self.setWindowFlags(self.window_setting_flag)

        # フラグを更新するとウィンドウが消えるので再描画
        self.show()

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
        self.update_image()

    def stop_slideshow(self):

        # 画像更新をする関数を呼び出すタイマーをストップする 
        self.timer.stop()

    def update_image(self):

        # インデックスが最後まで到達したら最初に戻す
        if self.path_index == len(self.image_paths):
            self.path_index = 0

        # 画像をセットする
        self.scene().set_file( self.image_paths[self.path_index] )

        # インデックスを更新
        self.path_index += 1 

    def resizeEvent(self, event):

        super().resizeEvent( event )   

        # ビューをリサイズ時にシーンの矩形を更新する
        self.scene().setSceneRect(QtCore.QRectF(self.rect()))
        # sceneにわたしている情報を更新
        self.scene().set_secene_size(self.width(), self.height())
        # 画像をscheneのサイズに合うようにリサイズする
        self.scene().fit_image()


    '''
    mouseEventの関数群で,四隅のドラッグでリサイズを,それ以外の場所でのドラッグで
    移動を実装している
    それぞれ別の関数に分けたほうがいい気がするが，ライブラリが用意したイベントハンドラ
    の関係で分けれていない
    '''

    def mousePressEvent(self, event):

        self.clicked_pos = event.pos() # ウィンドの左上を(0,0)にした相対位置

        grip_range = 8 # px

        if event.button() == QtCore.Qt.LeftButton:

            if (self.clicked_pos.x() < grip_range and self.clicked_pos.y() < grip_range):
                # ウィンドウの左上を掴んだ時
                self.pressed_status = Pressed_status.RESIZEABLE_UPPER_LEFT

            elif (abs(self.clicked_pos.x()-self.width()) < grip_range and
            self.clicked_pos.y() < grip_range):
                # ウィンドウの右上を掴んだ時
                self.pressed_status = Pressed_status.RESIZEABLE_UPPER_RIGHT

            elif (abs(self.clicked_pos.x()-self.width()) < grip_range and 
            abs(self.clicked_pos.y()-self.height()) < grip_range):
                # ウィンドウの右下を掴んだ時
                self.pressed_status = Pressed_status.RESIZEABLE_UNDER_RIGHT

            elif (self.clicked_pos.x() < grip_range and abs(self.clicked_pos.y()-self.height()) < grip_range):
                # ウィンドウの左下を掴んだ時
                self.pressed_status = Pressed_status.RESIZEABLE_UNDER_LEFT

            else:
                # それ以外の場所を掴んだ時
                self.pressed_status = Pressed_status.DRAGGABLE
                self.setCursor(QtCore.Qt.ClosedHandCursor) # カーソルを掴む手の絵に変更

    def mouseMoveEvent(self, event):

        """
        ドラッグの実装内の命名がひどいです。ごめんなさい
        """
        if event.button() == QtCore.Qt.LeftButton:

            if self.pressed_status == Pressed_status.RESIZEABLE_UPPER_LEFT:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                delta_x = self.width() - delta_pos.x()
                delta_y = self.height() - delta_pos.y()

                # サイズを更新
                self.resize(delta_x, delta_y)

                # 位置の更新
                self.current_pos.setX(self.current_pos.x() + delta_pos.x())
                self.current_pos.setY(self.current_pos.y() + delta_pos.y())
                self.move(self.current_pos)

            elif self.pressed_status == Pressed_status.RESIZEABLE_UPPER_RIGHT:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                delta_x = self.window_size.width() + delta_pos.x()
                delta_y = self.height() - delta_pos.y()

                # サイズを更新
                self.resize(delta_x, delta_y)
                # 位置の更新
                self.current_pos.setY(self.current_pos.y() + delta_pos.y())
                self.move(self.current_pos)

            elif self.pressed_status == Pressed_status.RESIZEABLE_UNDER_RIGHT:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                delta_x = self.window_size.width() + delta_pos.x() 
                delta_y = self.window_size.height() + delta_pos.y() 

                # サイズを更新
                self.resize(delta_x, delta_y)
            elif self.pressed_status == Pressed_status.RESIZEABLE_UNDER_LEFT:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                delta_x = self.width() - delta_pos.x()
                delta_y = self.window_size.height() + delta_pos.y()

                # サイズを更新
                self.resize(delta_x, delta_y)
                # 位置の更新
                self.current_pos.setX(self.current_pos.x() + delta_pos.x())
                self.move(self.current_pos)

            elif self.pressed_status == Pressed_status.DRAGGABLE:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                # 現在位置を更新
                self.current_pos += delta_pos 
                self.move(self.current_pos)

    def mouseReleaseEvent(self, event):

        self.pressed_status = Pressed_status.NORMAL
        self.unsetCursor()# カーソルを元に戻す

        # ウィンドウサイズの更新
        self.window_size = self.size()

class Pressed_status(Enum):

#　マウスをクリックしている時の状態を保持する列挙体

    NORMAL = auto()
    DRAGGABLE = auto()
    RESIZEABLE_UPPER_LEFT = auto()
    RESIZEABLE_UPPER_RIGHT = auto()
    RESIZEABLE_UNDER_RIGHT = auto()
    RESIZEABLE_UNDER_LEFT = auto()

# for debug
app = QtWidgets.QApplication([])
v = ImageViewer()
v.show()
v.show_set_Dialog()
v.start_slideshow()
import sys
sys.exit(app.exec_())
