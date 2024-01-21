import sys
from GUI.Qt5Files.UIMenu import * 
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import Bridge.controlador as con
import Bridge.state as state
import GUI.popups as popups

ui_MW : Ui_MainWindow

def tryToConnect():
    ret = con.connectAndFetch(ui_MW.user_input.text(), ui_MW.password_input.text())
    if ret[0]:
        ui_MW.paginas.setCurrentIndex(1)
    else:
        popups.showError(ret[2])

app = QApplication(sys.argv)
main_win = QMainWindow()

ui_MW = Ui_MainWindow()
ui_MW.setupUi(main_win)

ui_MW.paginas.setCurrentIndex(0)
ui_MW.connect_btn.clicked.connect(tryToConnect)


main_win.show()
app.exec_()
con.disconnect()
