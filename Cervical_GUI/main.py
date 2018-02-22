import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from view.my_window import MyWindow
import subprocess

# try:
subprocess.Popen([r"C:\Users\Florian\Documents\projet_long\projetlong\Cervical_GUI\cervical.exe"])
# except OSError:
    # print("Application 'Cervical' Oculus non trouvée")

app     = QApplication(sys.argv)
window  = QMainWindow()
ui      = MyWindow(window)
#
window.show()
sys.exit(app.exec_())




