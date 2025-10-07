# -*- coding: utf-8 -*-
import sqlite3

class Database:
    datafile = "clinica.db"
    def __init__(self):
        # Se habilita la conexion con la dB
        self.conn = sqlite3.connect(Database.datafile)
        self.cur = self.conn.cursor()
        
        
    def __del__(self):
        # Se cierra la conexion con la dB
        self.conn.close()
        
        
    def listar_medicos(self):
        # Retorna una lista de tuplas con la informacion de los medicos
        # con el formato [(med_id, nombre, apellido), ...]
        #
        # Se utiliza para llenar la informacion de la tabla tabMedicos
        
        sql = """SELECT * FROM medicos ORDER BY med_id"""
        Inf_med = [item for item in self.cur.execute(sql)]
        return Inf_med
    
    
    def listar_pacientes_medico(self, med_id):
        # Retorna una lista de tuplas con la información de un paciente que se 
        # encuentra asignado a un medico (segun el med_id) con el formato
        # [(pac_id, apellido, nombre, altura, edad, sexo), ...], ordenado 
        # alfabeticamente por apellido
        #
        # Se utiliza para llenar la informacion de la tabla tabPacientes
        sql = """SELECT pacientes.pac_id,
                        pacientes.apellido,
                        pacientes.nombre,
                        pacientes.altura,
                        pacientes.edad,
                        pacientes.sexo
                 FROM medicos
                     JOIN medico_paciente
                     JOIN pacientes
                 ON medicos.med_id = medico_paciente.med_id
                     AND medico_paciente.pac_id = pacientes.pac_id
                 WHERE medico_paciente.med_id = ?
                 ORDER BY pacientes.apellido"""
        Inf_pac = [item for item in self.cur.execute(sql,(med_id,))]
        return Inf_pac
    
        
    
    def nombre_paciente(self, id_pac):
        # Retorna una string con el nombre del paciente con el formato "apellido, nombre"
        #
        # Se utiliza para el titulo del gráfico
        sql = """SELECT pacientes.apellido,
                        pacientes.nombre
                 FROM medicos
                     JOIN medico_paciente
                     JOIN pacientes
                 ON medicos.med_id = medico_paciente.med_id
                     AND medico_paciente.pac_id = pacientes.pac_id
                 WHERE pacientes.pac_id = ?"""
        Ape_pac = [item[0] for item in self.cur.execute(sql,(id_pac,))]
        Nom_pac = [item[1] for item in self.cur.execute(sql,(id_pac,))]
        
        # for i,j in zip(Ape_pac, Nom_pac):
        #     return str(i+j)
        return Ape_pac[0], Nom_pac[0]
    
    
    def data_peso(self, pac_id):
        # Retorna una lista con los pesos registrados de un paciente en el 
        # historial de pesos: [peso1, peso2, ...]
        #
        # Se utiliza para el reporte gráfico
        sql = """SELECT historial_pesos.peso
                 FROM medicos
                     JOIN medico_paciente
                     JOIN pacientes
                     JOIN historial_pesos
                 ON medicos.med_id = medico_paciente.med_id
                     AND medico_paciente.pac_id = pacientes.pac_id
                     AND pacientes.pac_id = historial_pesos.pac_id
                 WHERE pacientes.pac_id = ?"""
        
        pesos = [item[0] for item in self.cur.execute(sql,(pac_id,))]
        
        # for i,j in zip(Ape_pac, Nom_pac):
        #     return str(i+j)
        return  pesos
    