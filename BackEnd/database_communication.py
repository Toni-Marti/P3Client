# Here is where the database is altered
import oracledb
from Bridge.enums import TableType
import Bridge.state as state

connection : oracledb.Connection = None
cursor : oracledb.Cursor

### INFO TABLAS ###
# Usuario
tab_usuario : str = "Usuario"
dni : str = "DNI"
nombre : str = "Nombre"
direccion : str = "Direccion"
telefono : str = "Telefono"
correo : str = "Correo"
correo_ugr : str = "Correo_UGR"
comp_ugr_es : str = "'%@ugr.es'"
comp_correo_ugr : str = "'%@correo.ugr.es'"
despacho : str = "Despacho"

#Baja
tab_baja : str = "Baja"
motivo : str = "Motivo"

# SolicitaBaja
tab_solbaja : str = "SolicitaBaja"
dni : str = "DNI"
f_ini : str = "F_Inicio"
f_fin : str = "F_Fin"
motivo : str = "Motivo"

#AntiguasBajas
tab_antiguasbajas : str = "AntiguasBajas"
dni : str = "DNI"
f_ini : str = "F_Inicio"
f_fin : str = "F_Fin"
motivo : str = "Motivo"



#  ████  ███  █   █ █   █ █████  ████ █████ █████  ███  █   █
# █     █   █ ██  █ ██  █ █     █       █     █   █   █ ██  █
# █     █   █ █ █ █ █ █ █ ████  █       █     █   █   █ █ █ █
# █     █   █ █  ██ █  ██ █     █       █     █   █   █ █  ██
#  ████  ███  █   █ █   █ █████  ████   █   █████  ███  █   █
 
def connect(usr : str, psswd : str):
    global connection, cursor
    
    if isConnected():
        connection.close()
    
    try:
        connection = oracledb.connect(user=usr, password=psswd, port=1521, host="oracle0.ugr.es", service_name="practbd.oracle0.ugr.es")
        cursor = connection.cursor()
    except:
        print("Couldn't connect to database.")    

def disconect():
    global connection
    
    if not state.hay_conexion_con_bd:
        return

    connection.close()
    connection = None


def isConnected() -> bool:
    if connection == None:
        return False
    
    if connection.is_healthy():
        return True
    else:
        disconect()
        return False

def _execute(command : str) -> bool:
    if not isConnected():
        return
    
    try:
        cursor.execute(command)
    except:
        print("Error executing:")
        print(command)
        return False
    else:
        return True
    

# ████   ███  █ █ █  ████
# █   █ █   █ █ █ █ █    
# ████  █   █ █ █ █  ███ 
# █ █   █   █ █ █ █     █
# █  █   ███   █ █  ████ 

def insertRow(table_type : TableType, row : list[str]) -> bool:
    if table_type == TableType.USUARIO:
        return _execute("INSERT INTO " + tab_usuario + " VALUES('" + row[0] + "','" + row[1] + "','" + row[2] + "','" + row[3] + "','" + row[4] + "','" + row[5] + "','" + row[6] + "')")
    elif table_type == TableType.BAJA:
        return _execute("INSERT INTO " + tab_baja + " VALUES('" + row[0] + "')")
    elif table_type == TableType.SOLICITA_BAJA:
        return _execute("INSERT INTO " + tab_solbaja + " VALUES('" + row[0] + "', to_date('" + row[1] + "', 'dd/mm/yyyy')" + ", to_date('" + row[2] + "', 'dd/mm/yyyy'), '" + row[3] + "')")
    elif table_type == TableType.ANTIGUAS_BAJAS:
        return _execute("INSERT INTO " + tab_antiguasbajas + " VALUES('" + row[0] + "', to_date('" + row[1] + "', 'dd/mm/yyyy')" + ", to_date('" + row[2] + "', 'dd/mm/yyyy'), '" + row[3] + "')")

def deleteRow(table_type : TableType, clave : list) -> bool:
    if table_type == TableType.USUARIO:
        return _execute("DELETE FROM " + tab_usuario + " WHERE " + dni + "='" + clave[0] + "'")
    elif table_type == TableType.BAJA:
        return _execute("DELETE FROM " + tab_baja + " WHERE "+ motivo + "='" + clave[0] + "'")
    elif table_type == TableType.SOLICITA_BAJA or table_type == TableType.ANTIGUAS_BAJAS:
        tabla : str
        if table_type == TableType.SOLICITA_BAJA:
            tabla = tab_solbaja
        elif table_type == TableType.ANTIGUAS_BAJAS:
            tabla = tab_antiguasbajas
        
        return _execute("DELETE FROM " + tabla + " WHERE " + dni + "='" + clave[0] + "' AND " + f_ini + "=to_date('" + clave[1].strftime("%d/%m/%Y") + "', 'dd/mm/yyyy') AND " + f_fin + "=to_date('" + clave[2].strftime("%d/%m/%Y") + "', 'dd/mm/yyyy')")
    
def existeAtrib(table : TableType, clave : str)->bool:
    if table==TableType.USUARIO:
        cursor.execute("SELECT * FROM USUARIO")
        #print(cursor.fetchall())
        for fila in cursor.fetchall():
            if clave[0]==fila[0]:
                return True

        for fila in cursor.fetchall():
            if clave[0]==fila[0]:
                return True

    elif table==TableType.BAJA:
        cursor.execute("SELECT * FROM BAJA")
        for fila in cursor.fetchall():
            if clave[0]==fila[3]:
                return True

        for fila in cursor.fetchall():
            if clave[0]==fila[3]:
                return True
    
    return False

#  ████ █████  ███  █████ █████       █   █ ████  ████   ███  █████ █████
# █       █   █   █   █   █           █   █ █   █ █   █ █   █   █   █    
#  ███    █   █   █   █   ████        █   █ ████  █   █ █   █   █   ████ 
#     █   █   █████   █   █           █   █ █     █   █ █████   █   █    
# ████    █   █   █   █   █████        ███  █     ████  █   █   █   █████

def fetchAll():
    if not isConnected():
        return
    
    fetchTable(TableType.USUARIO)
    fetchTable(TableType.BAJA)
    fetchTable(TableType.SOLICITA_BAJA)
    fetchTable(TableType.ANTIGUAS_BAJAS)
    
def fetchTable(table_type : TableType):
    if not isConnected():
        return
    
    table_name = "?"
    table : list[list]
    
    if table_type == TableType.USUARIO:
        table_name = tab_usuario
        table = state.valores_usuario
    elif table_type == TableType.BAJA:
        table_name = tab_baja
        table = state.valores_baja
    elif table_type == TableType.SOLICITA_BAJA:
        table_name = tab_solbaja
        table = state.valores_solicita_baja
    elif table_type == TableType.ANTIGUAS_BAJAS:
        table_name = tab_antiguasbajas
        table = state.valores_antiguas_bajas

    exists = True
    table.clear()
    
    try:
        cursor.execute("SELECT * FROM " + table_name)
    except:
        exists = False
    else:
        rows = cursor.fetchall()
        for row in rows:
            table.append(row)
        
        
    
    if table_type == TableType.USUARIO:
        state.usuario_table_exists = exists
    elif table_type == TableType.BAJA:
        state.baja_table_exists = exists
    elif table_type == TableType.SOLICITA_BAJA:
        state.solicitar_table_exists = exists
    elif table_type == TableType.ANTIGUAS_BAJAS:
        state.antiguas_table_exists = exists


#  ████  ███  █   █ █████ ████   ███  █    
# █     █   █ ██  █   █   █   █ █   █ █    
# █     █   █ █ █ █   █   ████  █   █ █    
# █     █   █ █  ██   █   █ █   █   █ █    
#  ████  ███  █   █   █   █  █   ███  █████

def commit():
    if not isConnected():
        return
    
    _execute("COMMIT")
    

def savepoint():
    if not isConnected():
        return
    
    _execute("SAVEPOINT")

def rollback():
    if not isConnected():
        return
    
    _execute("ROLLBACK")
    
