# Aqui se encuentran las funciones que comunican el front end con el back end
from Bridge.enums import *
import Bridge.state as state
import BackEnd.database_communication as db_com


# █████ █   █ █████ █████ ████  █   █  ███  █    
#   █   ██  █   █   █     █   █ ██  █ █   █ █    
#   █   █ █ █   █   ████  ████  █ █ █ █   █ █    
#   █   █  ██   █   █     █ █   █  ██ █████ █    
# █████ █   █   █   █████ █  █  █   █ █   █ █████

def _getExists(table : TableType) -> bool:
    if table == TableType.USUARIO:
        return state.usuario_table_exists
    elif table == TableType.BAJA:
        return state.baja_table_exists
    elif table == TableType.SOLICITA_BAJA:
        return state.solicitar_table_exists
    elif table == TableType.ANTIGUAS_BAJAS:
        return state.antiguas_table_exists



#  ███   ████ █████ █████  ███  █   █  ████
# █   █ █       █     █   █   █ ██  █ █    
# █   █ █       █     █   █   █ █ █ █  ███ 
# █████ █       █     █   █   █ █  ██     █
# █   █  ████   █   █████  ███  █   █ ████ 

def upadteConnectionState():
    state.hay_conexion_con_bd = db_com.isConnected()

def _insertRowCustomMethod(table_type : TableType, fila : list, db_insert_method : callable) -> list:
    upadteConnectionState()
    if not state.hay_conexion_con_bd:
        return [False, [InsertExitCode.NO_CONECTION], "No hay conexion con la base de datos."]
    
    if table_type == TableType.USUARIO:
        if not state.usuario_table_exists:
            return [False, [InsertExitCode.TABLE_DOES_NOT_EXIST], "La tabla Usuario no existe."]
        
        if len(fila) != 7:
            return [False, [InsertExitCode.INCORRECT_NUMBER_OF_FIELDS], "La tabla Usuario ha de tener 7 campos."]
        
        dni : str = fila[0]
        nombre : str = fila[1]
        direccion : str = fila[2]
        telefono : str = fila[3]
        correo : str = fila[4]
        correougr : str = fila[5]
        despacho : str = fila[6]

        if not dni[:8].isdigit() or not dni[8].isalpha():
            return [False, [InsertExitCode.INCORRECT_FORMAT], "Formato de DNI inválido"]

        if not nombre.isalpha():
            return [False, [InsertExitCode.INCORRECT_FORMAT], "Un nombre solo puede tener letras"]
        
        if not telefono[1:].isdigit():
            return [False, [InsertExitCode.INCORRECT_FORMAT], "Número de teléfono con letras"]
    
        if correougr[-7:]!="@ugr.es" and correougr[-14:]!="@correo.ugr.es":
            #print(correougr[-6:])
            return [False, [InsertExitCode.INCORRECT_FORMAT], "Correo UGR inválido"]
    

    elif table_type == TableType.BAJA:
        if not state.baja_table_exists:
            return [False, [InsertExitCode.TABLE_DOES_NOT_EXIST], "La tabla Baja no existe."]
        
        if len(fila) != 1:
            return [False, [InsertExitCode.INCORRECT_NUMBER_OF_FIELDS], "La tabla Baja ha de tener 1 campo."]
        
        motivo : str = fila[0]

    elif table_type == TableType.SOLICITA_BAJA or table_type == TableType.ANTIGUAS_BAJAS:
        exists = table_type == TableType.SOLICITA_BAJA ? state.solicitar_table_exists : state.antiguas_table_exists 
        if exists:
            return [False, [InsertExitCode.TABLE_DOES_NOT_EXIST], "La tabla SolicitaBaja no existe."]
        
        if len(fila) != 4:
            return [False, [InsertExitCode.INCORRECT_NUMBER_OF_FIELDS], "La tabla SolcitaBaja ha de tener 4 campos."]
    
        dni : str = fila[0]
        f_ini : str = fila[1]
        f_fin : str = fila[2]
        motivo : str = fila[3]

        if not dni[:8].isdigit() or not dni[8].isalpha():
            return [False, [InsertExitCode.INCORRECT_FORMAT], "Formato de DNI inválido"]
        
        #dd/mm/yyyy
        if int(f_ini[0:2])>int(f_fin[0:2]):
            if int(f_ini[3:5])>int(f_fin[3:5]):
                if int(f_ini[6:10])>int(f_fin[6:10]):
                    return [False, [InsertExitCode.INVALID_VALUES], "La fecha inicial es posterior a la fecha final"]
        
    if db_insert_method(table_type, fila):
        db_com.fetchTable(table_type)
        return [True, [InsertExitCode.SUCCES], "Se ha insertado la fila correctamente."]
    else:
        return [False, [InsertExitCode.UNKNOWN], "Error desconocido"]
    

def transactionInsertRow(table_type : TableType, fila : list) -> list:
    return _insertRowCustomMethod(table_type, fila, db_com.transactionInsertRow)

def insertRow(table_type : TableType, fila : list) -> list:
    return _insertRowCustomMethod(table_type, fila, db_com.insertRow)
        
        
def transactionDeleteRow(table_type : TableType, clave : str) -> bool:
    if db_com.transactionDeleteRow(clave):
        db_com.fetchTable(table_type)
        return [True,[DeleteExitCode.SUCCES], "Se ha borrado la fila correctamente"]
    else:
        return [False,[DeleteExitCode.UNKNOWN], "Error desconocido al borrar la fila"]

def commit() -> bool:
    upadteConnectionState()
    if not state.hay_conexion_con_bd:
        return False

    db_com.commit()
    return True

def savePoint() -> bool:
    upadteConnectionState()
    if not state.hay_conexion_con_bd:
        return False

    db_com.savepoint()
    return True

def rollBack() -> bool:
    upadteConnectionState()
    if not state.hay_conexion_con_bd:
        return False

    db_com.rollback()
    db_com.fetchAll()
    return True

def connectAndFetch(user : str, passwd : str) -> list:
    db_com.connect(user, passwd)
    upadteConnectionState()
    if not state.hay_conexion_con_bd:
        return [False, [CaFExitCode.NO_CONNECTION], "No se ha podido conectar con la base de datos"]
    
    db_com.fetchAll()
    
    return [True, [CaFExitCode.SUCCES], "Se ha conectado con la base de datos y actualizado las tablas."]

def disconnect():
    db_com.disconect()
    upadteConnectionState()
    
    
    
