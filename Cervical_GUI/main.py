import sys
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout

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
    try:
        subprocess.Popen([r".\cervical.exe"])
        app = QApplication(sys.argv)
        window = QMainWindow()
        ui = MyWindow(window)
        window.show()
        sys.exit(app.exec_())
    except OSError:

        print("Application 'Cervical' Oculus non trouvée")
        app = QApplication(sys.argv)
        w = QWidget()

        text = QLabel(w)
        text.setText("Nous n'avons pas pu lancer l'application 'Cervical' pour le casque Oculus Rift.\n"
                     "Assurez vous que 'cervical.exe' se situe bien dans le répertoire du programme.")

        w.setWindowTitle("Application 'Cervical' Oculus non trouvée")
        w.resize(400,80)
        text.move(10,20)
        w.show()
        sys.exit(app.exec_())






