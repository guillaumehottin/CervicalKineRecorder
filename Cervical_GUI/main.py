import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from view.acquistion_back import Acquisition
from view.my_window import MyWindow

app = QApplication(sys.argv)
window = QMainWindow()
# ui = Acquisition(window)
ui = MyWindow(window)
#
#TODO RUN UNITY APP
window.show()
sys.exit(app.exec_())
