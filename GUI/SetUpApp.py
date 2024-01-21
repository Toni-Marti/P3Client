import sys
from GUI.Qt5Files.UIMenu import * 
from PyQt5.QtWidgets import QMainWindow, QApplication
import Bridge.controlador as con
import Bridge.state as state

ui_main_win : Ui_MainWindow

def tryToConnect():
    ret = con.connectAndFetch(ui)
    if ret[0]:
        ui_main_win.paginas.setCurrentIndex(1)

app = QApplication(sys.argv)
main_win = QMainWindow()

ui_main_win = Ui_MainWindow()
ui_main_win.setupUi(main_win)

ui_main_win.paginas.setCurrentIndex(0)


main_win.show()
app.exec_()
con.disconnect()
