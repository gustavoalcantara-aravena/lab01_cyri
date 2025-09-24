# Sistema Modbus TCP - Servidor y Cliente Industrial

Este proyecto implementa un sistema de comunicación Modbus TCP completo con un servidor que simula datos industriales y un cliente con interfaz gráfica para visualización en tiempo real.

## 📋 Descripción del Proyecto

- **Servidor Modbus**: Simula un proceso industrial con variables de temperatura, presión y nivel
- **Cliente Modbus**: Interfaz gráfica para monitoreo en tiempo real con gráficos y visualizaciones
- **Comunicación**: Protocolo Modbus TCP sobre puerto 502

## 🚀 Tutorial Completo de Instalación y Ejecución

### Paso 1: Preparar el Entorno

#### 1.1 Verificar Python
```bash
# Verificar que tienes Python instalado
python --version
# Debe mostrar Python 3.7 o superior
```

#### 1.2 Crear Entorno Virtual
```bash
# Navegar al directorio del proyecto
cd C:\Users\tu_usuario\Downloads\CYRI

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Si tienes problemas con PowerShell, usar CMD:
# venv\Scripts\activate
```

### Paso 2: Instalar Librerías

#### 2.1 Actualizar pip
```bash
venv\Scripts\python.exe -m pip install --upgrade pip
```

#### 2.2 Instalar Librerías Principales
```bash
# Instalar todas las librerías necesarias
venv\Scripts\python.exe -m pip install pymodbus==2.5.3 seaborn matplotlib
```

#### 2.3 Verificar Instalación
```bash
# Verificar que se instalaron correctamente
venv\Scripts\python.exe -c "import pymodbus, seaborn, matplotlib; print('✅ Todas las librerías instaladas correctamente')"
```

### Paso 3: Ejecutar el Sistema

#### 3.1 Ejecutar el Servidor (Terminal 1)

**Opción A: En segundo plano**
```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar servidor en segundo plano
venv\Scripts\python.exe LAB_01\Server.py
```

**Opción B: En primer plano (recomendado para tutorial)**
```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar servidor y ver logs
venv\Scripts\python.exe LAB_01\Server.py
```

**Salida esperada del servidor:**
```
2025-09-23 15:20:01,688 - Servidor - Temperatura: 27.87°C, Presión: 1.04 bar, Nivel: 48.56%
2025-09-23 15:20:02,689 - Servidor - Temperatura: 28.70°C, Presión: 0.66 bar, Nivel: 50.61%
Server listening on localhost:502
```

#### 3.2 Ejecutar el Cliente (Terminal 2)

**Abrir una nueva terminal:**
```bash
# Navegar al directorio del proyecto
cd C:\Users\tu_usuario\Downloads\CYRI

# Activar entorno virtual
venv\Scripts\activate

# Ejecutar cliente
venv\Scripts\python.exe LAB_01\Cliente.py
```

**Salida esperada del cliente:**
```
2025-09-23 15:20:01 [INFO] - Conexión establecida con el servidor Modbus
2025-09-23 15:20:01 [INFO] - Datos recibidos: Temperatura: 27.87°C, Presión: 1.04 bar, Nivel: 48.56%
```

### Paso 4: Verificar el Funcionamiento

#### 4.1 Verificar Conexión
```bash
# En una tercera terminal, verificar que el puerto está en uso
netstat -an | findstr :502
```

**Salida esperada:**
```
TCP    0.0.0.0:502           0.0.0.0:0              LISTENING
```

#### 4.2 Verificar Procesos
```bash
# Verificar que ambos procesos están ejecutándose
tasklist | findstr python
```

## 📦 Librerías y Versiones Específicas

### Librerías Principales

| Librería | Versión | Propósito |
|----------|---------|-----------|
| **pymodbus** | 2.5.3 | Comunicación Modbus TCP |
| **matplotlib** | 3.10.6 | Gráficos y visualizaciones |
| **seaborn** | 0.13.2 | Visualización estadística |

### Librerías de Dependencias

| Librería | Versión | Descripción |
|----------|---------|-------------|
| **numpy** | 2.3.3 | Cálculos numéricos (dependencia de matplotlib/seaborn) |
| **pandas** | 2.3.2 | Manipulación de datos (dependencia de seaborn) |

### Librerías del Sistema Python

Las siguientes librerías están incluidas con Python y no requieren instalación:

- `tkinter` - Interfaz gráfica
- `threading` - Manejo de hilos
- `time` - Funciones de tiempo
- `random` - Generación de números aleatorios
- `logging` - Sistema de logs
- `datetime` - Manejo de fechas y horas

## 🎯 Comandos Rápidos de Instalación

```bash
# Comandos completos para instalación rápida
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install pymodbus==2.5.3 seaborn matplotlib
```

## 🔧 Configuración del Sistema

### Servidor Modbus
- **Puerto**: 502
- **Dirección**: localhost
- **Variables simuladas**:
  - Temperatura (20-100°C)
  - Presión (0-10 bar)
  - Nivel (0-100%)

### Cliente Modbus
- **Interfaz gráfica**: Tkinter
- **Gráficos**: Matplotlib con Seaborn
- **Frecuencia de actualización**: 1 segundo

## 📁 Estructura del Proyecto

```
CYRI/
├── venv/                          # Entorno virtual
├── LAB_01/
│   ├── Server.py                  # Servidor Modbus TCP
│   └── Cliente.py                 # Cliente con interfaz gráfica
├── README.md                      # Este archivo
└── test_cliente_simple.py         # Cliente de prueba
```

## 🐛 Solución de Problemas

### Error: "cannot import name 'StartTcpServer'"
**Causa**: Versión incorrecta de pymodbus
**Solución**:
```bash
pip uninstall pymodbus
pip install pymodbus==2.5.3
```

### Error: "ExceptionResponse exception_code=4"
**Causa**: Servidor no está ejecutándose
**Solución**:
1. Verificar que el servidor esté corriendo
2. Comprobar que el puerto 502 esté disponible
3. Reiniciar ambos procesos

### Error de política de ejecución en PowerShell
**Solución**:
```bash
# Usar CMD en lugar de PowerShell
venv\Scripts\activate
```

### Error: "BaseModbusDataBlock.async_getValues() takes from 2 to 3 positional arguments"
**Causa**: Incompatibilidad de versiones
**Solución**: Asegurar usar pymodbus 2.5.3

## 📊 Funcionalidades del Sistema

### Servidor Modbus
- ✅ Simulación de proceso industrial en tiempo real
- ✅ Actualización de datos cada segundo
- ✅ Logging detallado de actividad
- ✅ Manejo robusto de errores
- ✅ Configuración de variables industriales

### Cliente Modbus
- ✅ Interfaz gráfica intuitiva con Tkinter
- ✅ Gráficos en tiempo real con Matplotlib
- ✅ Visualización de múltiples variables simultáneamente
- ✅ Reconexión automática al servidor
- ✅ Sistema de logging para monitoreo

## 🔍 Verificación de Instalación Completa

```bash
# Verificar versión de Python
python --version

# Verificar entorno virtual
venv\Scripts\python.exe --version

# Verificar librerías instaladas
venv\Scripts\python.exe -m pip list | findstr -i "pymodbus matplotlib seaborn numpy pandas"

# Verificar importaciones
venv\Scripts\python.exe -c "import pymodbus, seaborn, matplotlib, numpy, pandas; print('✅ Todas las librerías funcionan correctamente')"
```

## 📝 Logs y Monitoreo

### Formato de Logs
- **Timestamp**: `YYYY-MM-DD HH:MM:SS,mmm`
- **Nivel**: INFO, ERROR, DEBUG
- **Mensaje**: Descripción detallada del evento

### Ejemplo de Logs del Servidor
```
2025-09-23 15:20:01,688 - Servidor - Temperatura: 27.87°C, Presión: 1.04 bar, Nivel: 48.56%
2025-09-23 15:20:02,689 - Servidor - Temperatura: 28.70°C, Presión: 0.66 bar, Nivel: 50.61%
```

### Ejemplo de Logs del Cliente
```
2025-09-23 15:20:01 [INFO] - Conexión establecida con el servidor Modbus
2025-09-23 15:20:01 [INFO] - Datos recibidos: Temperatura: 27.87°C, Presión: 1.04 bar, Nivel: 48.56%
```

## 🚨 Notas Importantes

### Versión Crítica de pymodbus
- **IMPORTANTE**: Usar pymodbus 2.5.3 específicamente
- Las versiones 3.x tienen cambios significativos en la API
- No actualizar a versiones más recientes sin modificar el código

### Importaciones Específicas
```python
# Servidor
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# Cliente
from pymodbus.client.sync import ModbusTcpClient
```

### Orden de Ejecución
1. **Primero**: Ejecutar el servidor
2. **Segundo**: Ejecutar el cliente
3. **Verificar**: Que ambos estén funcionando

## 🎓 Casos de Uso

### Para Desarrollo
- Simulación de procesos industriales
- Pruebas de comunicación Modbus
- Desarrollo de interfaces SCADA

### Para Aprendizaje
- Entender protocolo Modbus TCP
- Aprender comunicación cliente-servidor
- Visualización de datos en tiempo real

### Para Producción
- Monitoreo de variables industriales
- Interfaz de supervisión
- Sistema de alarmas básico

---

## 📞 Soporte

Si encuentras problemas:

1. **Verificar versiones**: Asegurar usar las versiones exactas especificadas
2. **Revisar logs**: Los mensajes de error suelen indicar el problema
3. **Reiniciar procesos**: Detener y volver a ejecutar servidor y cliente
4. **Verificar puertos**: Comprobar que el puerto 502 esté disponible

**Desarrollado para**: Laboratorio de Comunicaciones y Redes Industriales (CYRI)  
**Versión**: 1.0  
**Última actualización**: Septiembre 2025
