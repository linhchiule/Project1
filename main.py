

import faulthandler
faulthandler.enable()
import sys
from PyQt6.QtWidgets import QApplication
from logic import *

import faulthandler
faulthandler.enable()

def main():
    app = QApplication(sys.argv)
    window = Logic()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
