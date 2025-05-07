from modelo.persona import Persona

class Cliente(Persona):
    def __init__(self, nombre, apellido_paterno, apellido_materno, rfc, curp, sexo, fecha_nacimiento, domicilio_fiscal,
                 numero_contrato, telefono_fijo, telefono_movil, correo_electronico, nombre_asesor, usuario, password):
        Persona.__init__(self, nombre, apellido_paterno, apellido_materno, rfc, curp, sexo, fecha_nacimiento,
                         domicilio_fiscal)

        self.numero_contrato = numero_contrato
        self.telefono_fijo = telefono_fijo
        self.telefono_movil = telefono_movil
        self.correo_electronico = correo_electronico
        self.nombre_asesor = nombre_asesor
        self.usuario = usuario
        self.password = password
        self.cuentas_bancarias = []

    def agregar_cuenta_bancaria(self, cueta_bancaria):
        self.cuentas_bancarias.append(cueta_bancaria)


