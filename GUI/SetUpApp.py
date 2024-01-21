from GUI.Qt5Files.UIMenu import * 
from Bridge.enums import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem
import sys
import Bridge.controlador as con
import Bridge.state as state
import GUI.popups as popups

ui_MW : Ui_MainWindow
app = QApplication(sys.argv)

def tryToConnect():
    ret = con.connectAndFetch(ui_MW.user_input.text(), ui_MW.password_input.text())
    if ret[0]:
        dibujaTodasLasTablas()
        ui_MW.paginas.setCurrentIndex(1)
    else:
        popups.showError(ret[2])

def showDisconnect():
    con.disconnect()
    ui_MW.paginas.setCurrentIndex(0)
    popups.showMessage("Se ha desconectado de la base de datos")

def exitApplication():
    app.exit()

def dibujaTabla(tipo_tabla : TableType):
    data : list
    table : QTableWidget
    
    if tipo_tabla == TableType.USUARIO:
        data = state.valores_usuario
        table = ui_MW.table_usuario
    elif tipo_tabla == TableType.BAJA:
        data = state.valores_baja
        table = ui_MW.table_baja
    elif tipo_tabla == TableType.SOLICITA_BAJA:
        data = state.valores_solicita_baja
        table = ui_MW.table_solicitud_baja
    elif tipo_tabla == TableType.ANTIGUAS_BAJAS:
        data = state.valores_antiguas_bajas
        table = ui_MW.table_historial
    
    table.setRowCount(len(data))
    
    for r, row in enumerate(data):
        for i, val in enumerate(row):
            table.setItem(r, i, QTableWidgetItem(val))

def dibujaTodasLasTablas():
    dibujaTabla(TableType.USUARIO)
    dibujaTabla(TableType.BAJA)
    dibujaTabla(TableType.SOLICITA_BAJA)
    dibujaTabla(TableType.ANTIGUAS_BAJAS)
    


main_win = QMainWindow()

ui_MW = Ui_MainWindow()
ui_MW.setupUi(main_win)

ui_MW.paginas.setCurrentIndex(0)
ui_MW.tablas_tabs.setCurrentIndex(0)
ui_MW.connect_btn.clicked.connect(tryToConnect)
ui_MW.exit_btn.clicked.connect(exitApplication)
ui_MW.dissconect_btn.clicked.connect(showDisconnect)

main_win.show()
app.exec_()
con.disconnect()
