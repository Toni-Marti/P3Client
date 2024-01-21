import BackEnd.database_communication as db_com

# Aqui se almacena la informacion que define el estado de la apliacion
hay_conexion_con_bd : bool = False

usuario_table_exists : bool
baja_table_exists : bool
solicitar_table_exists : bool
antiguas_table_exists : bool

valores_usuario : list = []
valores_baja : list = []
valores_solicita_baja : list = []
valores_antiguas_bajas : list = []

def printState():
    print("===== PRINTING STATE =====")
    
    db_com.fetchAll()
    
    if not hay_conexion_con_bd:
        print("No hay conexion con la base de datos")
        print()
        return
    
    print()
    print("Hay conexion con la base de datos")
    
    if usuario_table_exists:
        print("Tabla Usuario:")
        print(valores_usuario)
    else:
        print("Tabla Usuario:")
        print("No existe")
    print()
    
    if baja_table_exists:
        print("Tabla Baja:")
        print(valores_baja)
    else:
        print("Tabla Baja:")
        print("No existe")
    print()
    
    if solicitar_table_exists:
        print("Tabla Solicita Baja:")
        print(valores_solicita_baja)
    else:
        print("Tabla Solicita Baja:")
        print("No existe")
    print()

    if antiguas_table_exists:
        print("Tabla Antiguas Bajas:")
        print(valores_antiguas_bajas)
    else:
        print("Tabla Antiguas Bajas:")
        print("No existe")
    print()