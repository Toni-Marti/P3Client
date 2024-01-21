from GUI.Qt5Files.UIMenu import * 
from Bridge.enums import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem
import sys
from GUI.Qt5Files.UIMenu import * 
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import Bridge.controlador as con
import Bridge.state as state
import Bridge.enums as enum
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

def insertRow(tipo : enum.TableType):
    if tipo==enum.TableType.USUARIO:
        args=[ui_MW.usu_DNI_in, ui_MW.usu_nom_in, ui_MW.usu_dir_in, ui_MW.usu_tel_in, ui_MW.usu_corr_in, ui_MW.usu_corr_ugr_in, ui_MW.usu_desp_in]
        ret=con.transactionInsertRow(args)
        if ret[0]:
            ui_MW.dibujaTabla(tipo)
        else:
            popups.showError(ret[2])
    elif tipo==enum.TableType.BAJA:
        args=[ui_MW.baja_mot_in]
        ret=con.transactionInsertRow(args)
        if ret[0]:
            ui_MW.dibujaTabla(tipo)
        else:
            popups.showError(ret[2])
    elif tipo==enum.TableType.SOLICITA_BAJA:
        args=[ui_MW.sol_DNI_in, ui_MW.sol_ini_in, ui_MW.sol_fin_in, ui_MW.sol_motivo_in]
        ret=con.transactionInsertRow(args)
        if ret[0]:
            ui_MW.dibujaTabla(tipo)
        else:
            popups.showError(ret[2])
    elif tipo==enum.TableType.ANTIGUAS_BAJAS:
        args=[ui_MW.hist_DNI_in, ui_MW.hist_ini_in, ui_MW.hist_fin_in, ui_MW.hist_motivo_in]
        ret=con.transactionInsertRow(args)
        if ret[0]:
            ui_MW.dibujaTabla(tipo)
        else:
            popups.showError(ret[2])

def exitApplication():
    app.exit()

def deleteRow(tipo : enum.TableType):
    if tipo==enum.TableType.USUARIO:
        clave=state.valores_usuario[ui_MW.usu_fil_in][0]
        ret=con.transactionDeleteRow(clave)
        if ret[0]:
            ui_MW.dibujaTabla(tipo)
        else:
            popups.showError(ret[2])
    elif tipo==enum.TableType.BAJA:
        clave=state.valores_baja[ui_MW.baja_fil_in][0]
        ret=con.transactionDeleteRow(clave)
        if ret[0]:
            ui_MW.dibujaTabla(tipo)
        else:
            popups.showError(ret[2])
    elif tipo==enum.TableType.SOLICITA_BAJA:
        clave=state.valores_solicita_baja[ui_MW.baja_fil_in][0]
        ret=con.transactionDeleteRow(clave)
        if ret[0]:
            ui_MW.dibujaTabla(tipo)
        else:
            popups.showError(ret[2])
    elif tipo==enum.TableType.ANTIGUAS_BAJAS:
        clave=state.valores_antiguas_bajas[ui_MW.baja_fil_in][0]
        ret=con.transactionDeleteRow(clave)
        if ret[0]:
            ui_MW.dibujaTabla(tipo)
        else:
            popups.showError(ret[2])

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
ui_MW.usu_add_btn.clicked.connect(lambda:insertRow(tipo=enum.TableType.USUARIO))
ui_MW.usu_elim_btn.clicked.connect(lambda:deleteRow(tipo=enum.TableType.USUARIO))
ui_MW.baja_add_btn.clicked.connect(lambda:insertRow(tipo=enum.TableType.BAJA))
ui_MW.baja_elim_btn.clicked.connect(lambda:deleteRow(tipo=enum.TableType.BAJA))
ui_MW.sol_add_btn.clicked.connect(lambda:insertRow(tipo=enum.TableType.SOLICITA_BAJA))
ui_MW.sol_elim_btn.clicked.connect(lambda:deleteRow(tipo=enum.TableType.SOLICITA_BAJA))
ui_MW.hist_add_btn.clicked.connect(lambda:insertRow(tipo=enum.TableType.ANTIGUAS_BAJAS))
ui_MW.hist_elim_btn.clicked.connect(lambda:deleteRow(tipo=enum.TableType.ANTIGUAS_BAJAS))


main_win.show()
app.exec_()
con.disconnect()
