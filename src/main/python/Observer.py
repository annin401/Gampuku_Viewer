'''
Observer.py

Copyright © 2019 Hashidzume Hikaru. All rights reserved.
Released under the GPL license.
'''
import os
from watchdog import events, observers
from PyQt5 import QtWidgets, QtCore

class Observer(QtCore.QObject):
    directory_changed = QtCore.pyqtSignal()

    def __init__(self, path=''):
        super().__init__()

        self.__target_path = path
        self.__observer = observers.Observer()
        self.__event_handler = ChanegeHandla()

        self.__event_handler.directory_changed.connect(self.directory_changed.emit)

    def set__target_path(self, path:str) -> None:
        self.__target_path = path

    def start(self):

        try:
            self.__observer.schedule(self.__event_handler, self.__target_path,
                recursive=True)
        except FileNotFoundError:
            return

        # ディレクトリを変更した時にでも実行できるようにする
        try:
            self.__observer.start()
        except RuntimeError:
            return

    def stop(self):
        self.__observer.stop()

class ChanegeHandla(QtCore.QObject, events.FileSystemEventHandler):
    
    directory_changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def on_created(self, event):
        self.directory_changed.emit()

    def on_modified(self, event):
        self.directory_changed.emit()

    def on_deleted(self, event):
        self.directory_changed.emit()

    def on_moved(self, event):
        self.directory_changed.emit()