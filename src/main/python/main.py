import sys
from fbs_runtime.application_context import ApplicationContext
from MainWindow import MainWindow

class AppContext(ApplicationContext):

    def __init__(self):
        super().__init__()

        self.main_window = MainWindow()

    def run(self):
        self.main_window.show()
        return self.app.exec_()
    
if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)

