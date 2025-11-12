from datetime import datetime
from math import sin, cos, tan, radians, acos, degrees
import matplotlib.font_manager as fm
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt5.QtCore import Qt

def sombra(date, latitude, hora_do_dia, altura_arvore):
    ####################################################################
    ################### TRANSFORMAÇÃO DOS DADOS ########################
    ####################################################################

    # Converte string de data em objeto formato datetime
    date_obj = datetime.strptime(date, '%Y-%m-%d')

    # Converte string de hora em inteiros de hora e minuto
    hour, minute = map(int, hora_do_dia.split(':'))

    # Calcula a hora decimal do dia
    hora_decimais = hour + (minute / 60)

    ####################################################################
    ################# COMPRIMENTO E DIREÇÃO DA SOMBRA ##################
    ####################################################################

    # Dia do ano (NDA)
    nda = (date_obj - datetime(date_obj.year, 1, 1)).days + 1

    # Ângulo da declinação solar
    declinacao_solar = 23.45 * sin(radians(360 / 365 * (nda - 80)))

    # Ângulo horário
    h = 15 * (hora_decimais - 12)

    # Ângulo zenital
    angulo_zenital = degrees(acos(sin(radians(declinacao_solar)) * sin(radians(latitude)) + 
                                  cos(radians(declinacao_solar)) * cos(radians(latitude)) * cos(radians(h))))
        
    # Azimute solar (direção do sol)
    cos_dir_sol = (sin(radians(latitude)) * cos(radians(angulo_zenital)) - sin(radians(declinacao_solar))) / (cos(radians(latitude)) * sin(radians(angulo_zenital)))

    if cos_dir_sol > 1 or cos_dir_sol < -1:
        cos_dir_sol = cos_dir_sol / abs(cos_dir_sol)

    dir_sol = degrees(acos(cos_dir_sol))

    # Comprimento da sombra
    comp_sombra = altura_arvore * tan(radians(angulo_zenital))

    #####################################################################
    #################### VETORES PARA O GRÁFICO #########################
    #####################################################################

    # Eixo X da sombra
    if h < 0:
        xs = -sin(radians(180 - dir_sol)) * comp_sombra
    else:
        xs = sin(radians(180 - dir_sol)) * comp_sombra

    # Eixo Y da sombra
    ys = -cos(radians(180 - dir_sol)) * comp_sombra

    xsombra = [0, xs]
    ysombra = [0, ys]

    # Eixo X do sol
    if h < 0:
        xl = sin(radians(dir_sol)) * comp_sombra
    else:
        xl = -sin(radians(dir_sol)) * comp_sombra

    # Eixo Y do sol
    yl = -cos(radians(dir_sol)) * comp_sombra

    xsol = [0, xl]
    ysol = [0, yl]

    #####################################################################
    ################## GRÁFICO COM ESCALA FIXA ##########################
    #####################################################################

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.plot(xsol, ysol, '-o', markersize=10, label="Posição do sol", color="yellow", zorder=3)
    ax.plot(xsombra, ysombra, '-o', markersize=5, label="Posição da sombra", color="blue", zorder=4)
    ax.axhline(y=0, color='black', linewidth=2, zorder=2)
    ax.axvline(x=0, color='black', linewidth=2, zorder=1)
    
    # Definir os limites dos eixos com uma unidade maior
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    
    font = fm.FontProperties(weight='bold')
    texto = f"Data: {date}\nLatitude: {latitude:.2f}°\nHora do dia: {hora_do_dia}\nAltura da árvore: {altura_arvore:.2f} m\nComprimento da sombra: {comp_sombra:.2f} m\nAzimute solar: {dir_sol:.2f}°"
    ax.text(-29, 30, texto, fontsize=10, ha='left', va='top', color='black')
    
    # Adicionar as letras
    ax.text(30, 0, 'E', fontsize=14, fontproperties=font, ha='center', va='center', color='black', bbox=dict(facecolor='white', edgecolor='white'))
    ax.text(-31, 0, 'W', fontsize=14, fontproperties=font, ha='center', va='center', color='black', bbox=dict(facecolor='white', edgecolor='white'))
    ax.text(0, 30, 'N', fontsize=14, fontproperties=font, ha='center', va='center', color='black', bbox=dict(facecolor='white', edgecolor='white'))
    ax.text(0, -32, 'S', fontsize=14, fontproperties=font, ha='center', va='center', color='black', bbox=dict(facecolor='white', edgecolor='white'))

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, loc="upper right", ncol=1)
    
    plt.xticks([])
    plt.yticks([])
    
    # Remover as bordas do gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()

    return fig

def calculate_solar_position(date, latitude):
    # Lista para armazenar os resultados
    xsol_list = []
    ysol_list = []
    
    # Loop from 07:00 to 18:00
    for hour in range(7, 18):
        # Converter a hora
        hora_do_dia = f'{hour:02d}:00'

        # Converter a data de entrada
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        hour, minute = map(int, hora_do_dia.split(':'))
        hora_decimais = hour + (minute / 60)

        # Parâmetros da sombra
        nda = (date_obj - datetime(date_obj.year, 1, 1)).days + 1
        declinacao_solar = 23.45 * sin(radians(360 / 365 * (nda - 80)))
        h = 15 * (hora_decimais - 12)
        angulo_zenital = degrees(acos(sin(radians(declinacao_solar)) * sin(radians(latitude)) +
                                      cos(radians(declinacao_solar)) * cos(radians(latitude)) * cos(radians(h))))
        cos_dir_sol = (sin(radians(latitude)) * cos(radians(angulo_zenital)) - sin(radians(declinacao_solar))) / (
                cos(radians(latitude)) * sin(radians(angulo_zenital)))
        if cos_dir_sol > 1 or cos_dir_sol < -1:
            cos_dir_sol = cos_dir_sol / abs(cos_dir_sol)
        dir_sol = degrees(acos(cos_dir_sol))
        comp_sombra = 22 * tan(radians(angulo_zenital))

        # Pontos para plotar
        if h < 0:
            xl = sin(radians(dir_sol)) * comp_sombra
        else:
            xl = -sin(radians(dir_sol)) * comp_sombra
        if h < 0:
            yl = -cos(radians(dir_sol)) * comp_sombra
        else:
            yl = -cos(radians(dir_sol)) * comp_sombra

        # Salvando os pontos
        xsol_list.append(xl)
        ysol_list.append(yl)
    
    return xsol_list, ysol_list

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sombra")
        self.setMinimumSize(1000, 600)  # Aumentei a largura mínima da janela

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)  # Usando QHBoxLayout para organizar horizontalmente

        input_layout = QFormLayout()

        self.date_entry = QLineEdit(self)
        self.latitude_entry = QLineEdit(self)
        self.hora_entry = QLineEdit(self)
        self.altura_entry = QLineEdit(self)

        input_layout.addRow("Data (YYYY-MM-DD):", self.date_entry)
        input_layout.addRow("Latitude (graus decimais):", self.latitude_entry)
        input_layout.addRow("Hora do dia (HH:MM):", self.hora_entry)
        input_layout.addRow("Altura da árvore (metros):", self.altura_entry)

        button_layout = QVBoxLayout()

        plot_sombra_button = QPushButton("Plotar Sombra", self)
        plot_trajetoria_button = QPushButton("Plotar Trajetória Solar", self)

        plot_sombra_button.clicked.connect(self.plot_sombra_graph)
        plot_trajetoria_button.clicked.connect(self.plot_trajetoria_solar)

        button_layout.addWidget(plot_sombra_button)
        button_layout.addWidget(plot_trajetoria_button)

        input_layout.addRow("", button_layout)

        main_layout.addLayout(input_layout)

        annotation_label = QLabel("Universidade Federal do Espírito Santo\n Programa de Pós-graduação em Ciências Florestais\n Laboratório de Modelagem Hidrológica")
        annotation_label.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(annotation_label)
        
        # Adicionar a anotação com a versão do programa
        version_label = QLabel("(MORO et al., 2023)")
        version_label.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(version_label)

        self.canvas = FigureCanvas(plt.figure(figsize=(6, 6)))
        main_layout.addWidget(self.canvas)

    def plot_sombra_graph(self):
        date = self.date_entry.text()
        latitude = float(self.latitude_entry.text())
        hora_do_dia = self.hora_entry.text()
        altura_arvore = float(self.altura_entry.text())

        fig = sombra(date, latitude, hora_do_dia, altura_arvore)
        self.update_canvas(fig)

    def plot_trajetoria_solar(self):
        date = self.date_entry.text()
        latitude = float(self.latitude_entry.text())
        #altura_arvore = float(self.altura_entry.text())

        xsol, ysol = calculate_solar_position(date, latitude)
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(xsol, ysol, '-o', markersize=5, label="Trajetória solar", color="yellow")
        plt.axhline(y=0, color='black', linewidth=2, zorder=2)
        plt.axvline(x=0, color='black', linewidth=2, zorder=1)
        plt.xlim(-50, 50)
        
        texto = f"Trajetória solar ao longo do dia\nData: {date}\nLatitude: {latitude:.2f}°"
        ax.text(-48, 48, texto, fontsize=10, ha='left', va='top', color='black')

        font = fm.FontProperties(weight='bold')
        plt.text(50, 0, 'E', fontsize=14, fontproperties=font, ha='center', va='center', color='black', bbox=dict(facecolor='white', edgecolor='white'))
        plt.text(-50, 0, 'W', fontsize=14, fontproperties=font, ha='center', va='center', color='black', bbox=dict(facecolor='white', edgecolor='white'))
        plt.text(0, 50, 'N', fontsize=14, fontproperties=font, ha='center', va='center', color='black', bbox=dict(facecolor='white', edgecolor='white'))
        plt.text(0, -50, 'S', fontsize=14, fontproperties=font, ha='center', va='center', color='black', bbox=dict(facecolor='white', edgecolor='white'))
        plt.box(False)
        plt.grid(False)
        
        plt.ylim(-50, 50)
        plt.xticks([])
        plt.yticks([])

        plt.legend(loc= "upper right")
        plt.tight_layout()

        self.update_canvas(fig)

    def update_canvas(self, fig):
        self.canvas.figure.clear()
        self.canvas.figure = fig
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()