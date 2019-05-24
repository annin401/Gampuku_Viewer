import sys
from fbs_runtime.application_context import ApplicationContext

class AppContext(ApplicationContext):

    def __init__(self):
        super().__init__()

    def run(self):
        return self.app.exec_()
    
if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)

