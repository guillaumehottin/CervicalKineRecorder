import sys
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QMainWindow

from view.my_window import MyWindow
import subprocess


def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(t))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions

try:
    subprocess.Popen([r"..\Cervical_exec\cervical.exe"])
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = MyWindow(window)
    window.show()
    sys.exit(app.exec_())
except OSError:
    print("Application 'Cervical' Oculus non trouvée")






