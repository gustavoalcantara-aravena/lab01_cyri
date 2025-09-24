from pymodbus.client.sync import ModbusTcpClient
import matplotlib.pyplot as plt
import numpy as np
import time
import logging
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import seaborn as sns
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Arc, RegularPolygon
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.patheffects as PathEffects
from matplotlib.colors import LinearSegmentedColormap


# Configurar estilo visual industrial
plt.style.use('dark_background')
sns.set_style("darkgrid", {"axes.facecolor": ".15"})


# Colores industriales
INDUSTRIAL_COLORS = {
    'background': '#1E1E1E',
    'panel': '#2A2A2A',
    'accent': '#3A3A3A',
    'grid': '#333333',
    'text': '#FFFFFF',
    'warning': '#FF9F1C',
    'danger': '#E71D36',
    'success': '#2EC4B6',
    'info': '#4361EE',
    'temp_gradient': ['#2EC4B6', '#FF9F1C', '#E71D36'],
    'level_gradient': ['#E71D36', '#FF9F1C', '#2EC4B6'],
    'pressure_gradient': ['#2EC4B6', '#4361EE', '#E71D36']
}


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class IndustrialSymbols:
    @staticmethod
    def draw_tank(ax, x, y, width, height, level_percent, color='#4361EE'):
        # Dibujar tanque
        tank_body = patches.Rectangle(
            (x, y), width, height,
            facecolor='none',
            edgecolor=color,
            linewidth=2
        )
        ax.add_patch(tank_body)


        # Nivel del líquido
        level_height = height * (level_percent / 100)
        liquid = patches.Rectangle(
            (x, y), width, level_height,
            facecolor=color,
            alpha=0.3
        )
        ax.add_patch(liquid)


        # Detalles del tanque
        ax.add_patch(patches.Arc(
            (x + width/2, y + height),
            width, height*0.2,
            theta1=0, theta2=180,
            edgecolor=color,
            linewidth=2
        ))


        # Agregar líneas de nivel
        for i in range(5):
            y_level = y + (height * i / 4)
            ax.plot([x, x + width], [y_level, y_level],
                   '--', color=color, alpha=0.3, linewidth=1)


    @staticmethod
    def draw_thermometer(ax, x, y, temp, max_temp=100):
        height = 0.15
        width = 0.04
        bulb_radius = width/1.5


        # Tubo
        ax.add_patch(patches.Rectangle(
            (x, y), width, height,
            facecolor='none',
            edgecolor='white',
            linewidth=2
        ))


        # Marcas de temperatura
        for i in range(5):
            y_mark = y + (height * i / 4)
            ax.plot([x, x + width*1.5], [y_mark, y_mark],
                   '-', color='white', alpha=0.5, linewidth=1)


        # Bulbo
        ax.add_patch(patches.Circle(
            (x + width/2, y),
            bulb_radius,
            facecolor='red',
            alpha=0.6
        ))


        # Nivel
        level = (temp/max_temp) * height
        ax.add_patch(patches.Rectangle(
            (x, y), width, level,
            facecolor='red',
            alpha=0.6
        ))


    @staticmethod
    def draw_pressure_gauge(ax, x, y, pressure, max_pressure=10):
        radius = 0.08
        angle = (pressure/max_pressure) * 180


        # Marco circular
        ax.add_patch(patches.Circle(
            (x, y), radius,
            facecolor='none',
            edgecolor='white',
            linewidth=2
        ))


        # Marcas de presión
        for i in range(8):
            angle_mark = np.radians(180 - (180 * i / 7))
            x_start = x + radius * 0.8 * np.cos(angle_mark)
            y_start = y + radius * 0.8 * np.sin(angle_mark)
            x_end = x + radius * 0.9 * np.cos(angle_mark)
            y_end = y + radius * 0.9 * np.sin(angle_mark)
            ax.plot([x_start, x_end], [y_start, y_end],
                   '-', color='white', alpha=0.5, linewidth=1)


        # Aguja
        angle_rad = np.radians(180 - angle)
        dx = radius * 0.8 * np.cos(angle_rad)
        dy = radius * 0.8 * np.sin(angle_rad)
        ax.plot([x, x + dx], [y, y + dy], 'r-', linewidth=2)


        # Centro de la aguja
        ax.add_patch(patches.Circle(
            (x, y), radius*0.1,
            facecolor='red',
            edgecolor='white',
            linewidth=1
        ))


class ModernIndicator:
    def __init__(self, ax, pos, size=0.15):
        self.ax = ax
        self.pos = pos
        self.size = size


        # Crear indicador base
        self.outer_circle = Circle(pos, size, facecolor='#2A2A2A',
                                 edgecolor='#3A3A3A', linewidth=2)
        self.inner_circle = Circle(pos, size*0.8, facecolor='#1E1E1E',
                                 edgecolor='#3A3A3A', linewidth=1)
        self.led = Circle(pos, size*0.6, facecolor='gray', alpha=0.6)


        # Agregar elementos
        self.ax.add_patch(self.outer_circle)
        self.ax.add_patch(self.inner_circle)
        self.ax.add_patch(self.led)


        # Agregar efecto de brillo metálico
        gradient = Circle(pos, size*0.9, facecolor='white', alpha=0.1)
        self.ax.add_patch(gradient)


    def actualizar(self, estado):
        colors = {
            "Normal": INDUSTRIAL_COLORS['success'],
            "Advertencia": INDUSTRIAL_COLORS['warning'],
            "Crítico": INDUSTRIAL_COLORS['danger']
        }
        color = colors.get(estado, 'gray')
        self.led.set_facecolor(color)


        # Efecto de brillo
        glow = Circle(self.pos, self.size*0.7, facecolor=color, alpha=0.3)
        self.ax.add_patch(glow)


        # Efecto de resplandor
        for i in range(3):
            alpha = 0.1 - (i * 0.03)
            size_mult = 0.8 + (i * 0.1)
            glow_outer = Circle(self.pos, self.size*size_mult,
                              facecolor=color, alpha=alpha)
            self.ax.add_patch(glow_outer)
class ClienteModbus:
    def __init__(self):
        self.client = ModbusTcpClient('localhost', port=502)


        # Configuración de datos
        self.max_points = 50
        self.datos_temperatura = []
        self.datos_presion = []
        self.datos_nivel = []
        self.tiempos = []
        self.timestamps = []


        # Estados y alarmas
        self.estado_sistema = "Normal"
        self.alarmas = []
        self.contador_lecturas = 0
        self.tiempo_inicio = datetime.now()


        # Símbolos industriales
        self.symbols = IndustrialSymbols()


        # Configuración visual
        plt.ion()
        self.crear_figura()
        self.configurar_graficos()
        self.crear_indicadores()


    def crear_figura(self):
        self.fig = plt.figure(figsize=(16, 10), facecolor=INDUSTRIAL_COLORS['background'])
        gs = GridSpec(3, 4, figure=self.fig)


        # Gráficos principales
        self.ax1 = self.fig.add_subplot(gs[0, :3])
        self.ax2 = self.fig.add_subplot(gs[1, :3])
        self.ax3 = self.fig.add_subplot(gs[2, :3])


        # Paneles laterales
        self.ax_info = self.fig.add_subplot(gs[:2, 3])
        self.ax_alarmas = self.fig.add_subplot(gs[2, 3])


        # Título principal con efecto metálico
        titulo = self.fig.suptitle('SISTEMA SCADA INDUSTRIAL',
                                 fontsize=16, color='white', y=0.98,
                                 fontweight='bold')
        titulo.set_path_effects([
            PathEffects.withStroke(linewidth=3, foreground=INDUSTRIAL_COLORS['accent']),
            PathEffects.withStroke(linewidth=4, foreground='black', alpha=0.3)
        ])


        # Crear gradientes personalizados para las líneas
        self.temp_cmap = LinearSegmentedColormap.from_list('temp',
                                                          INDUSTRIAL_COLORS['temp_gradient'])
        self.pres_cmap = LinearSegmentedColormap.from_list('pres',
                                                          INDUSTRIAL_COLORS['pressure_gradient'])
        self.level_cmap = LinearSegmentedColormap.from_list('level',
                                                           INDUSTRIAL_COLORS['level_gradient'])


        # Inicializar líneas con gradientes y efectos
        self.line_temp, = self.ax1.plot([], [], color=INDUSTRIAL_COLORS['success'],
                                       linewidth=2.5,
                                       path_effects=[PathEffects.withStroke(linewidth=4,
                                       foreground='#333333')])
        self.line_pres, = self.ax2.plot([], [], color=INDUSTRIAL_COLORS['info'],
                                       linewidth=2.5,
                                       path_effects=[PathEffects.withStroke(linewidth=4,
                                       foreground='#333333')])
        self.line_nivel, = self.ax3.plot([], [], color=INDUSTRIAL_COLORS['success'],
                                        linewidth=2.5,
                                        path_effects=[PathEffects.withStroke(linewidth=4,
                                        foreground='#333333')])


    def crear_indicadores(self):
        # Crear indicadores modernos con efecto metálico
        self.indicador_temp = ModernIndicator(self.ax_info, (0.2, 0.8))
        self.indicador_pres = ModernIndicator(self.ax_info, (0.2, 0.5))
        self.indicador_nivel = ModernIndicator(self.ax_info, (0.2, 0.2))


        # Agregar símbolos industriales con efectos mejorados
        self.symbols.draw_thermometer(self.ax_info, 0.7, 0.7, 50)
        self.symbols.draw_pressure_gauge(self.ax_info, 0.8, 0.5, 5)
        self.symbols.draw_tank(self.ax_info, 0.7, 0.1, 0.2, 0.2, 50)


    def configurar_graficos(self):
        for ax, titulo, color in [
            (self.ax1, 'MONITOREO DE TEMPERATURA', INDUSTRIAL_COLORS['success']),
            (self.ax2, 'MONITOREO DE PRESIÓN', INDUSTRIAL_COLORS['info']),
            (self.ax3, 'MONITOREO DE NIVEL', INDUSTRIAL_COLORS['success'])
        ]:
            # Estilo industrial mejorado
            ax.set_facecolor(INDUSTRIAL_COLORS['background'])
            ax.grid(True, linestyle='--', alpha=0.2, color=INDUSTRIAL_COLORS['grid'])


            # Título con efecto metálico mejorado
            title = ax.set_title(titulo, color=color, fontsize=10, pad=10, fontweight='bold')
            title.set_path_effects([
                PathEffects.withStroke(linewidth=2, foreground=INDUSTRIAL_COLORS['accent']),
                PathEffects.withStroke(linewidth=3, foreground='black', alpha=0.3)
            ])


            # Bordes y marcas mejorados
            ax.tick_params(colors=INDUSTRIAL_COLORS['text'], grid_alpha=0.2)
            for spine in ax.spines.values():
                spine.set_color(INDUSTRIAL_COLORS['accent'])
                spine.set_linewidth(2)


            # Marco industrial mejorado
            bbox = FancyBboxPatch(
                (-0.05, -0.05), 1.1, 1.1,
                boxstyle="round,pad=0.02",
                fc=INDUSTRIAL_COLORS['panel'],
                ec=INDUSTRIAL_COLORS['accent'],
                transform=ax.transAxes,
                zorder=0
            )
            ax.add_patch(bbox)


        # Configurar límites y etiquetas
        self.ax1.set_ylim(0, 100)
        self.ax2.set_ylim(0, 10)
        self.ax3.set_ylim(0, 100)


        for ax, label in [
            (self.ax1, 'Temperatura (°C)'),
            (self.ax2, 'Presión (bar)'),
            (self.ax3, 'Nivel (%)')
        ]:
            ax.set_ylabel(label, color=INDUSTRIAL_COLORS['text'], fontweight='bold')
            ax.set_xlabel('Tiempo (s)', color=INDUSTRIAL_COLORS['text'], fontweight='bold')


    def crear_panel_estado(self):
        self.ax_info.clear()
        self.ax_info.axis('off')


        # Panel industrial mejorado
        panel = FancyBboxPatch(
            (0.02, 0.02), 0.96, 0.96,
            boxstyle="round,pad=0.02",
            fc=INDUSTRIAL_COLORS['panel'],
            ec=INDUSTRIAL_COLORS['accent'],
            transform=self.ax_info.transAxes
        )
        self.ax_info.add_patch(panel)


        # Título del panel con efecto metálico mejorado
        titulo = self.ax_info.text(0.5, 0.95, 'PANEL DE CONTROL',
                                 ha='center', va='top',
                                 color=INDUSTRIAL_COLORS['text'],
                                 fontsize=12, fontweight='bold')
        titulo.set_path_effects([
            PathEffects.withStroke(linewidth=2, foreground=INDUSTRIAL_COLORS['accent']),
            PathEffects.withStroke(linewidth=3, foreground='black', alpha=0.3)
        ])


        # Información del sistema con estilo industrial mejorado
        self.mostrar_info_sistema()
        self.mostrar_valores_actuales()
        self.actualizar_simbolos_industriales()


    def mostrar_info_sistema(self):
        y_pos = 0.85
        for etiqueta, valor in [
            ('TIEMPO DE OPERACIÓN', self.obtener_tiempo_operacion()),
            ('LECTURAS REALIZADAS', str(self.contador_lecturas)),
            ('ESTADO DEL SISTEMA', self.estado_sistema),
            ('ÚLTIMA ACTUALIZACIÓN', datetime.now().strftime('%H:%M:%S'))
        ]:
            # Marco metálico mejorado
            rect = FancyBboxPatch(
                (0.05, y_pos-0.03), 0.9, 0.04,
                boxstyle="round,pad=0.01",
                fc=INDUSTRIAL_COLORS['accent'],
                ec=INDUSTRIAL_COLORS['info'],
                alpha=0.3,
                transform=self.ax_info.transAxes
            )
            self.ax_info.add_patch(rect)


            # Texto con efecto metálico mejorado
            texto = self.ax_info.text(0.07, y_pos, f"{etiqueta}:",
                                    color=INDUSTRIAL_COLORS['text'],
                                    fontsize=9, fontweight='bold')
            valor_texto = self.ax_info.text(0.93, y_pos, f"{valor}",
                                          color=INDUSTRIAL_COLORS['info'],
                                          fontsize=9, ha='right',
                                          fontweight='bold')


            for t in [texto, valor_texto]:
                t.set_path_effects([
                    PathEffects.withStroke(linewidth=1,
                                         foreground=INDUSTRIAL_COLORS['accent']),
                    PathEffects.withStroke(linewidth=2, foreground='black', alpha=0.3)
                ])


            y_pos -= 0.06


    def mostrar_valores_actuales(self):
        if not self.datos_temperatura:
            return


        # Panel de valores actuales
        valores_panel = FancyBboxPatch(
            (0.05, 0.1), 0.9, 0.55,
            boxstyle="round,pad=0.02",
            fc=INDUSTRIAL_COLORS['panel'],
            ec=INDUSTRIAL_COLORS['success'],
            transform=self.ax_info.transAxes,
            alpha=0.3
        )
        self.ax_info.add_patch(valores_panel)


        # Valores actuales con sus indicadores
        valores = [
            ('TEMPERATURA', self.datos_temperatura[-1], '°C', 0.85,
             INDUSTRIAL_COLORS['success']),
            ('PRESIÓN', self.datos_presion[-1], 'bar', 0.55,
             INDUSTRIAL_COLORS['info']),
            ('NIVEL', self.datos_nivel[-1], '%', 0.25,
             INDUSTRIAL_COLORS['success'])
        ]


        for etiqueta, valor, unidad, y_pos, color in valores:
            # Marco para el valor
            valor_rect = FancyBboxPatch(
                (0.35, y_pos-0.03), 0.25, 0.04,
                boxstyle="round,pad=0.01",
                fc=INDUSTRIAL_COLORS['accent'],
                ec=color,
                alpha=0.3,
                transform=self.ax_info.transAxes
            )
            self.ax_info.add_patch(valor_rect)


            # Valor actual con efecto metálico
            valor_texto = self.ax_info.text(0.47, y_pos,
                                          f"{valor:.1f}{unidad}",
                                          color=INDUSTRIAL_COLORS['text'],
                                          fontsize=10, ha='center',
                                          fontweight='bold')
            valor_texto.set_path_effects([
                PathEffects.withStroke(linewidth=2,
                                     foreground=INDUSTRIAL_COLORS['accent'])
            ])


            # Estado
            estado = self.evaluar_estado(valor, 0, 100 if unidad in ['°C', '%'] else 10)
            estado_color = self.obtener_color_estado(estado)


            # Marco para el estado
            estado_rect = FancyBboxPatch(
                (0.35, y_pos-0.08), 0.25, 0.04,
                boxstyle="round,pad=0.01",
                fc=INDUSTRIAL_COLORS['accent'],
                ec=estado_color,
                alpha=0.3,
                transform=self.ax_info.transAxes
            )
            self.ax_info.add_patch(estado_rect)


            # Mostrar estado
            estado_texto = self.ax_info.text(0.47, y_pos-0.05, estado,
                                           color=estado_color,
                                           fontsize=8, ha='center')
            estado_texto.set_path_effects([
                PathEffects.withStroke(linewidth=1,
                                     foreground=INDUSTRIAL_COLORS['accent'])
            ])


    def actualizar_simbolos_industriales(self):
        if not self.datos_temperatura:
            return


        # Actualizar símbolos con valores actuales y efectos mejorados
        self.symbols.draw_thermometer(self.ax_info, 0.7, 0.7,
                                    self.datos_temperatura[-1])
        self.symbols.draw_pressure_gauge(self.ax_info, 0.8, 0.5,
                                       self.datos_presion[-1])
        self.symbols.draw_tank(self.ax_info, 0.7, 0.1, 0.2, 0.2,
                             self.datos_nivel[-1])


    def actualizar_alarmas(self):
        self.ax_alarmas.clear()
        self.ax_alarmas.axis('off')


        # Panel de alarmas mejorado
        panel = FancyBboxPatch(
            (0.02, 0.02), 0.96, 0.96,
            boxstyle="round,pad=0.02",
            fc=INDUSTRIAL_COLORS['panel'],
            ec=INDUSTRIAL_COLORS['danger'],
            transform=self.ax_alarmas.transAxes
        )
        self.ax_alarmas.add_patch(panel)


        # Título con efecto de advertencia mejorado
        titulo = self.ax_alarmas.text(0.5, 0.9, 'REGISTRO DE ALARMAS',
                                    ha='center',
                                    color=INDUSTRIAL_COLORS['danger'],
                                    fontsize=10, fontweight='bold')
        titulo.set_path_effects([
            PathEffects.withStroke(linewidth=2,
                                 foreground=INDUSTRIAL_COLORS['accent']),
            PathEffects.withStroke(linewidth=3, foreground='black', alpha=0.3)
        ])


        # Mostrar alarmas con estilo industrial mejorado
        y_pos = 0.7
        for alarma in self.alarmas[-3:]:
            rect = FancyBboxPatch(
                (0.05, y_pos-0.03), 0.9, 0.04,
                boxstyle="round,pad=0.01",
                fc=INDUSTRIAL_COLORS['accent'],
                ec=INDUSTRIAL_COLORS['danger'],
                alpha=0.3,
                transform=self.ax_alarmas.transAxes
            )
            self.ax_alarmas.add_patch(rect)


            texto = self.ax_alarmas.text(0.07, y_pos, alarma,
                                       color=INDUSTRIAL_COLORS['danger'],
                                       fontsize=8, fontweight='bold')
            texto.set_path_effects([
                PathEffects.withStroke(linewidth=1,
                                     foreground=INDUSTRIAL_COLORS['accent']),
                PathEffects.withStroke(linewidth=2, foreground='black', alpha=0.3)
            ])


            y_pos -= 0.2


    def obtener_tiempo_operacion(self):
        delta = datetime.now() - self.tiempo_inicio
        horas = delta.seconds // 3600
        minutos = (delta.seconds % 3600) // 60
        segundos = delta.seconds % 60
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


    def evaluar_estado(self, valor, min_val, max_val):
        if min_val <= valor <= max_val:
            if min_val + (max_val - min_val) * 0.1 <= valor <= max_val - (max_val - min_val) * 0.1:
                return "Normal"
            return "Advertencia"
        return "Crítico"


    def obtener_color_estado(self, estado):
        return {
            "Normal": INDUSTRIAL_COLORS['success'],
            "Advertencia": INDUSTRIAL_COLORS['warning'],
            "Crítico": INDUSTRIAL_COLORS['danger']
        }.get(estado, INDUSTRIAL_COLORS['danger'])


    def verificar_alarmas(self, temp, pres, nivel):
        timestamp = datetime.now().strftime('%H:%M:%S')
        if temp > 90:
            self.alarmas.append(f"{timestamp} - ¡Temperatura crítica! ({temp:.1f}°C)")
        if pres > 8:
            self.alarmas.append(f"{timestamp} - ¡Presión elevada! ({pres:.1f} bar)")
        if nivel < 10:
            self.alarmas.append(f"{timestamp} - ¡Nivel bajo! ({nivel:.1f}%)")


        self.alarmas = self.alarmas[-10:]


    def leer_datos(self):
        try:
            temp = self.client.read_holding_registers(0, 1, unit=1).registers[0] / 100.0
            time.sleep(0.1)
            pres = self.client.read_holding_registers(1, 1, unit=1).registers[0] / 100.0
            time.sleep(0.1)
            nivel = self.client.read_holding_registers(2, 1, unit=1).registers[0] / 100.0


            self.contador_lecturas += 1
            self.verificar_alarmas(temp, pres, nivel)


            return temp, pres, nivel
        except Exception as e:
            logging.error(f"Error en lectura: {e}")
            return None, None, None


    def actualizar_graficos(self):
        if len(self.tiempos) > self.max_points:
            self.tiempos.pop(0)
            self.datos_temperatura.pop(0)
            self.datos_presion.pop(0)
            self.datos_nivel.pop(0)
            self.timestamps.pop(0)


        # Actualizar líneas con gradientes de color
        if self.datos_temperatura:
            temp_colors = self.temp_cmap(np.clip(np.array(self.datos_temperatura) / 100, 0, 1))
            pres_colors = self.pres_cmap(np.clip(np.array(self.datos_presion) / 10, 0, 1))
            level_colors = self.level_cmap(np.clip(np.array(self.datos_nivel) / 100, 0, 1))


            self.line_temp.set_color(temp_colors[-1])
            self.line_pres.set_color(pres_colors[-1])
            self.line_nivel.set_color(level_colors[-1])


        self.line_temp.set_data(self.tiempos, self.datos_temperatura)
        self.line_pres.set_data(self.tiempos, self.datos_presion)
        self.line_nivel.set_data(self.tiempos, self.datos_nivel)


        if self.tiempos:
            for ax in [self.ax1, self.ax2, self.ax3]:
                ax.set_xlim(max(0, self.tiempos[-1] - self.max_points),
                          self.tiempos[-1] + 2)


        self.crear_panel_estado()
        self.actualizar_alarmas()


        if self.datos_temperatura:
            self.indicador_temp.actualizar(
                self.evaluar_estado(self.datos_temperatura[-1], 0, 100))
            self.indicador_pres.actualizar(
                self.evaluar_estado(self.datos_presion[-1], 0, 10))
            self.indicador_nivel.actualizar(
                self.evaluar_estado(self.datos_nivel[-1], 0, 100))


        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def iniciar(self):
        if not self.client.connect():
            logging.error("Error de conexión con el servidor Modbus")
            return


        logging.info("Conexión establecida con el servidor Modbus")
        tiempo_inicio = time.time()


        try:
            while True:
                temp, pres, nivel = self.leer_datos()
                if temp is not None:
                    tiempo_actual = int(time.time() - tiempo_inicio)
                    self.tiempos.append(tiempo_actual)
                    self.timestamps.append(datetime.now())
                    self.datos_temperatura.append(temp)
                    self.datos_presion.append(pres)
                    self.datos_nivel.append(nivel)
                    self.actualizar_graficos()
                time.sleep(1)


        except KeyboardInterrupt:
            logging.info("Finalizando monitoreo...")
        finally:
            self.client.close()
            plt.ioff()
            plt.close()


if __name__ == "__main__":
    cliente = ClienteModbus()
    cliente.iniciar()


