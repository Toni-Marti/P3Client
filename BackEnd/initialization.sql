

CREATE TABLE Usuario (
DNI VARCHAR2(9) PRIMARY KEY,
Nombre VARCHAR2(30),
Direccion VARCHAR2(50),
Telefono VARCHAR2(15),
Correo VARCHAR2(50),
Correo_UGR VARCHAR2(50) CHECK (Correo_UGR LIKE '%@ugr.es' OR Correo_UGR LIKE '%@correo.ugr.es'),
Despacho VARCHAR2(50)
);


CREATE TABLE Baja(
Motivo VARCHAR2(100) PRIMARY KEY
)

CREATE TABLE SolicitaBaja(
DNI REFERENCES Usuario(DNI),
F_Inicio DATE,
F_Fin DATE, 
Motivo REFERENCES Baja(Motivo),
CHECK(F_Fin > F_Inicio),
PRIMARY KEY(DNI, F_Inicio, F_Fin)
);

CREATE TABLE AntiguasBajas(
DNI REFERENCES Usuario(DNI),
F_Inicio DATE,
F_Fin DATE, 
Motivo REFERENCES Baja(Motivo),
CHECK(F_Fin > F_Inicio),
PRIMARY KEY(DNI, F_Inicio, F_Fin)
);
COMMIT;



CREATE OR REPLACE TRIGGER GuardarAntiguasBajas
BEFORE DELETE ON SolicitaBaja
FOR EACH ROW
BEGIN
    -- Insertar la fila eliminada en AntiguasBajas
    INSERT INTO AntiguasBajas(DNI, F_Inicio, F_Fin, Motivo)
    VALUES (:OLD.DNI, :OLD.F_Inicio, :OLD.F_Fin, :OLD.Motivo);
END;

COMMIT;