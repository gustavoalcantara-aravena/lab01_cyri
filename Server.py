from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import threading
import time
import random
import logging


# Configurar logging para ver la actividad del servidor
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class SimuladorProceso:
    def __init__(self):
        self.temperatura = 25.0
        self.presion = 1.0
        self.nivel = 50.0


    def simular_cambios(self):
        # Simular cambios más notables para mejor visualización
        self.temperatura += random.uniform(-2, 2)
        self.presion += random.uniform(-0.5, 0.5)
        self.nivel += random.uniform(-3, 3)


        # Mantener valores en rangos realistas
        self.temperatura = max(20, min(100, self.temperatura))
        self.presion = max(0, min(10, self.presion))
        self.nivel = max(0, min(100, self.nivel))


        return {
            'temperatura': int(self.temperatura * 100),
            'presion': int(self.presion * 100),
            'nivel': int(self.nivel * 100)
        }


class ServidorModbus:
    def __init__(self):
        # Crear almacén de datos Modbus para pymodbus 2.x
        self.store = ModbusSlaveContext(
            hr=ModbusSequentialDataBlock(0, [0] * 100),
        )
        self.context = ModbusServerContext(slaves=self.store, single=True)
        self.simulador = SimuladorProceso()


    def actualizar_datos(self):
        while True:
            try:
                # Obtener nuevos valores del simulador
                valores = self.simulador.simular_cambios()


                # Actualizar registros Modbus
                self.store.setValues(3, 0, [valores['temperatura']])
                self.store.setValues(3, 1, [valores['presion']])
                self.store.setValues(3, 2, [valores['nivel']])


                # Mostrar valores actuales
                logging.info(f"Servidor - Temperatura: {valores['temperatura']/100:.2f}°C, "
                           f"Presión: {valores['presion']/100:.2f} bar, "
                           f"Nivel: {valores['nivel']/100:.2f}%")


                time.sleep(1)
            except Exception as e:
                logging.error(f"Error en actualización: {e}")
                time.sleep(1)


    def iniciar(self):
        # Iniciar thread de actualización de datos
        thread_actualizacion = threading.Thread(target=self.actualizar_datos)
        thread_actualizacion.daemon = True
        thread_actualizacion.start()


        # Iniciar servidor Modbus
        logging.info("Iniciando servidor Modbus TCP en localhost:5020...")
        StartTcpServer(self.context, address=("localhost", 502))


if __name__ == "__main__":
    servidor = ServidorModbus()
    servidor.iniciar()
