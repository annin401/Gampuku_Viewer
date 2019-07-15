'''
main.py

Copyright © 2019 Hashidzume Hikaru. All rights reserved.
Released under the GPL license.
'''
import sys
from fbs_runtime.application_context import ApplicationContext
from ImageViewer import ImageViewer

class AppContext(ApplicationContext):

    def __init__(self):
        super().__init__()

        self.image_viewer = ImageViewer()

    def run(self):
        self.image_viewer.show()
        self.image_viewer.show_set_Dialog()
        self.image_viewer.start_slideshow()
        return self.app.exec_()
    
if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)