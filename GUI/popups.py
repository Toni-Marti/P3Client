from PyQt5.QtWidgets import QMessageBox

def showMessage(message : str, title : str = "Info"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.setWindowTitle(title)
    msg.exec_()

def showError(message : str, title : str = "Error"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.setWindowTitle(title)
    msg.exec_()