'''
イメージを表示する画面
MainWindowの代わり
'''
import os
from enum import Enum, auto
from PyQt5 import QtWidgets, QtCore, QtGui
from ImagePaths import ImagePaths
from ImageViewScene import ImageViewScene
from environmental_setting import Environmental_setting
from Observer import Observer

class ImageViewer( QtWidgets.QGraphicsView ):

    def __init__(self):

        super().__init__()

        self.image_paths =  ImagePaths()
        self.window_setting_flag = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        self.window_opacity = 1.0 

        # for slideshow
        self.is_active = False 
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_image) 
        self.update_interval = 2000 # ミリ秒
        self.path_index = 0

        # for status when dragging
        self.pressed_status = Pressed_status.NORMAL
        # for move action when dragging 
        self.clicked_pos = QtCore.QPoint()
        self.size_when_clicked = QtCore.QSize()

        # for context menu
        self.menu = QtWidgets.QMenu()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # for environmental_setting
        self.env_window = Environmental_setting()

        # for QSettings
        self.settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope,
        "Gampuku Viewer")
        self.settings.setIniCodec(QtCore.QTextCodec.codecForName("utf-8"))

        # for Obserber
        self.obserber = Observer()
        self.obserber.directory_changed.connect(self._directory_chage_occer_event)

        # それぞれの初期化
        self.init_imageViewer()
        self.init_environmental_setting()
        self.init_shortcut()


    def init_imageViewer(self):

        initial_size = QtCore.QSize(480.0, 270.0) # px 
        self.resize(initial_size) #　初期ウィンドウサイズを指定

        initial_pos = self._get_initial_pos_hint()
        self.move(initial_pos) # ウィンドの場所を移動

        self.setWindowFlags(self.window_setting_flag)
        self.setMinimumSize(160, 90)
        self.setBackgroundBrush(QtGui.QColor("#181A1B"))
        self.setWindowOpacity(self.window_opacity)

        # QGraphicsViewの設定
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)        
        self.setRenderHints(QtGui.QPainter.Antialiasing |
                QtGui.QPainter.SmoothPixmapTransform |
                QtGui.QPainter.TextAntialiasing
        )

        # QGraphicsSceneの作成・および設定.
        scene = ImageViewScene(self.width(), self.height())
        scene.setSceneRect( QtCore.QRectF( self.rect()))
        self.setScene(scene)

    def show_context_menu(self):

        # アクションの設定
        open_folder = QtWidgets.QAction("フォルダーを開く")
        open_folder.triggered.connect(self._select_folder_event)

        open_environmental_setting = QtWidgets.QAction("環境設定を開く")
        open_environmental_setting.triggered.connect(self.show_environmental_setting)

        exit_action = QtWidgets.QAction("終了")
        exit_action.triggered.connect(self.close)

        # メニューを構築
        self.menu.addAction(open_folder)
        self.menu.addAction(open_environmental_setting)
        self.menu.addSection("")
        self.menu.addAction(exit_action)

        # メニューを表示
        self.menu.exec_(QtGui.QCursor.pos()) # マウスの座標を引数に渡す

    def init_environmental_setting(self):

        # env_windowからでるsignalを接続
        self.env_window.update_interval_changed.connect(self.set_update_interval)
        self.env_window.opacity_changed.connect(self.set_opacity)
        self.env_window.window_on_top_state_changed.connect(self.set_window_setting_flag)

        # iniファイルから情報を読み込む
        loaded_update_interval = int(self.settings.value("update_interval", 2000))
        loaded_opacity = float(self.settings.value("opacity", 1.0))
        loaded_is_on_top = int(self.settings.value("is_on_top",
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))

        # 環境設定の情報を渡す
        self.env_window.set_update_interval(loaded_update_interval)
        self.env_window.set_opacity(loaded_opacity)
        self.env_window.set_is_on_top(loaded_is_on_top)

    def show_environmental_setting(self):

        # 環境設定ウィンドウを表示
        self.env_window.show()

        # ディスプレイの中央の座標を求める
        screen_size = QtWidgets.qApp.desktop().size()
        central_pos = QtCore.QPoint(screen_size.width() // 2 - self.env_window.size().width(),
            screen_size.height() // 2 - self.env_window.size().height())

        # 中央の移動
        self.env_window.move(central_pos)

    def _get_initial_pos_hint(self) -> QtCore.QPoint:
        """
        必ずウィンドウのサイズの初期化を行ってからこの関数を呼び出してください
        """
        # ディスプレイのタスクバーなどを除いたサイズを所得
        d_width = QtWidgets.qApp.desktop().availableGeometry().width()
        d_height = QtWidgets.qApp.desktop().availableGeometry().height()

        margin = 30 # px
        return QtCore.QPoint(d_width - self.width() - margin, d_height - self.height() - margin)

    def init_shortcut(self):

        # フォルダを選択
        open_folder_event = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+O'), self)
        open_folder_event.activated.connect(self._select_folder_event)

        # 環境設定
        show_env_window_event = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+,'), self)
        show_env_window_event.activated.connect(self.show_environmental_setting)

        # 終了
        close_event = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+W'), self)
        close_event.activated.connect(self.close)

    def set_update_interval(self,sec: int)-> None:

        # 秒をミリ秒に直す
        m_sec = sec * 1000
        self.update_interval = m_sec

        if self.is_active:
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

    def show_set_Dialog(self) -> bool:

        # iniファイルから前回選択したディレクトリパスを取り出す
        loaded_dir_path = self.settings.value("selected_dir_path", os.path.expanduser('~'))

        # ファイルダイアログを表示
        selected_dir_path = QtWidgets.QFileDialog.getExistingDirectory(self,
            'Select Folder', loaded_dir_path)

        # フォルダーが選択されなかったら終了しFalseを返す
        if selected_dir_path == '':
            return False

        # 画像パスのリストを生成
        self.image_paths.make_list(selected_dir_path)

        # 選択したディレクトリパスをiniファイルに保存
        self.settings.setValue("selected_dir_path", selected_dir_path)

        # フォルダーが選択されたらTrueを返す
        return True

    def start_slideshow(self):

        if not self.image_paths:
            return

        # 初期化
        self.path_index = 0
        # 画像更新をする関数を呼び出すタイマーをスタートする
        self.timer.start(self.update_interval)

        # 最初に表示する画像をセットする
        self.update_image()

        # 更新間隔を変更時に使用するフラグを立てる
        self.is_active = True

        # ディレクトリを監視するクラスをスタートする
        self.obserber.set__target_path(self.image_paths.get_dir_path())
        self.obserber.start()

    def restart_slideshow(self):

        if not self.image_paths:
            return 

        # 画像更新をする関数を呼び出すタイマーをスタートする
        self.timer.start(self.update_interval)

        # 更新間隔を変更時に使用するフラグを立てる
        self.is_active = True

        # ディレクトリを監視するクラスをスタートする
        self.obserber.set__target_path(self.image_paths.get_dir_path())
        self.obserber.start()

    def stop_slideshow(self):

        # 画像更新をする関数を呼び出すタイマーをストップする 
        self.timer.stop()

        self.is_active = False

    def update_image(self):

        # インデックスが最後まで到達したら最初に戻す
        if self.path_index == len(self.image_paths):
            self.path_index = 0

        try:
            # 画像をセットする
            self.scene().set_file( self.image_paths[self.path_index] )
        except ZeroDivisionError:
            # アクセス権限がない画像などboundingRectが所得できないため
            # 0除算が起こるため、その時は無視するようにする
            self.path_index += 1
            self.update_image()
            return 

        # インデックスを更新
        self.path_index += 1 

    def _select_folder_event(self):
        # フォルダーを選択する時の動作をまとめたメソッド

        self.stop_slideshow()

        is_selected = self.show_set_Dialog()

        # フォルダーの選択をキャンセルしたらそのまま再生
        if is_selected:
            self.start_slideshow()
        else:
            self.restart_slideshow()

    def _directory_chage_occer_event(self):
        # 選択してたディレクトリに新しい画像が入ったり消
        # えたりした時に呼ばれるメソッド

        self.stop_slideshow()

        # image_pathsを作り直す
        self.image_paths.make_list(self.image_paths.get_dir_path())

        self.start_slideshow()

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
        self.size_when_clicked = self.size()

        grip_range = 10 # px

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

        if event.button() == QtCore.Qt.LeftButton:

            if self.pressed_status == Pressed_status.RESIZEABLE_UPPER_LEFT:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                delta_x = self.width() - delta_pos.x()
                delta_y = self.height() - delta_pos.y()

                # サイズを更新
                self.resize(delta_x, delta_y)

                # 位置の更新
                self.move(self.pos().x() + delta_pos.x(), self.pos().y() + delta_pos.y())

            elif self.pressed_status == Pressed_status.RESIZEABLE_UPPER_RIGHT:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                delta_x = self.size_when_clicked.width() + delta_pos.x()
                delta_y = self.height() - delta_pos.y()

                # サイズを更新
                self.resize(delta_x, delta_y)
                # 位置の更新
                self.move(self.pos().x(), self.pos().y() + delta_pos.y())

            elif self.pressed_status == Pressed_status.RESIZEABLE_UNDER_RIGHT:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                delta_x = self.size_when_clicked.width() + delta_pos.x() 
                delta_y = self.size_when_clicked.height() + delta_pos.y() 

                # サイズを更新
                self.resize(delta_x, delta_y)

            elif self.pressed_status == Pressed_status.RESIZEABLE_UNDER_LEFT:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                delta_x = self.width() - delta_pos.x()
                delta_y = self.size_when_clicked.height() + delta_pos.y()

                # サイズを更新
                self.resize(delta_x, delta_y)
                # 位置の更新
                self.move(self.pos().x() + delta_pos.x(), self.pos().y())

            elif self.pressed_status == Pressed_status.DRAGGABLE:
                # マウスの移動距離を求める
                delta_pos = event.pos() - self.clicked_pos
                # 現在位置を更新
                self.move(self.pos() + delta_pos)

    def mouseReleaseEvent(self, event):

        self.pressed_status = Pressed_status.NORMAL
        self.unsetCursor()# カーソルを元に戻す

    def closeEvent(self, event):

        # 環境設定で設定したことをiniファイルの保存
        self.settings.setValue("update_interval", int(self.update_interval))
        self.settings.setValue("opacity", float(self.window_opacity))
        self.settings.setValue("is_on_top", int(self.window_setting_flag))

        # iniファイルに書き出す
        self.settings.sync()

        # 環境設定が開いている場合、閉じる
        self.env_window.close()

class Pressed_status(Enum):

#　マウスをクリックしている時の状態を保持する列挙体

    NORMAL = auto()
    DRAGGABLE = auto()
    RESIZEABLE_UPPER_LEFT = auto()
    RESIZEABLE_UPPER_RIGHT = auto()
    RESIZEABLE_UNDER_RIGHT = auto()
    RESIZEABLE_UNDER_LEFT = auto()
