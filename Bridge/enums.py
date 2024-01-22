from enum import Enum

class TableType(Enum):
    USUARIO = 1
    BAJA = USUARIO+1
    SOLICITA_BAJA = BAJA+1
    ANTIGUAS_BAJAS = SOLICITA_BAJA+1

def tableToStrg(table : TableType) -> str:
    if table == TableType.USUARIO:
        return "Usuario"
    elif table == TableType.BAJA:
        return "Baja"
    elif table == TableType.SOLICITA_BAJA:
        return "Solicita Baja"
    elif table == TableType.ANTIGUAS_BAJAS:
        return "Antiguas Bajas"

class CreateExitCode(Enum):
    SUCCES = 0
    NO_CONECTION = 1
    UNKNOWN = 2
    ALREADY_EXISTS = 3
    NEEDS_USUARIO_TABLE = 4
    NEEDS_BAJA_TABLE = 5
    NEEDS_SOLICITA_BAJA_TABLE = 6
    NEEDS_ANTIGUAS_BAJAS_TABLE = 7

class DeleteExitCode(Enum):
    SUCCES = 0
    NO_CONECTION = 1
    UNKNOWN = 2
    DOES_NOT_EXIST = 3
    REFERENCES_NOT_DELETED = 4

class InsertExitCode(Enum):
    SUCCES = 0
    NO_CONECTION = 1
    UNKNOWN = 2
    TABLE_DOES_NOT_EXIST = 3
    DUPLICATE_KEY = 4
    INCORRECT_NUMBER_OF_FIELDS = 5
    DOES_NOT_COINCIDE_WITH_REFERENCE = 6
    INVALID_VALUES = 7
    INCORRECT_FORMAT = 8

class CaFExitCode(Enum):
    SUCCES = 0
    NO_CONNECTION = 1
    UNKNOWN = 2