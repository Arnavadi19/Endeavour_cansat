import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit
from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

class CanSatGCS(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CanSat Ground Control Station")
        self.setGeometry(100, 100, 1000, 800)

        self.telemetry_label = QLabel("Telemetry Data:")
        self.telemetry_display = QTextEdit()
        self.telemetry_display.setReadOnly(True)

        self.altitude_plot = self.create_plot("Altitude", "Time", "Altitude (m)")
        self.pressure_plot = self.create_plot("Pressure", "Time", "Pressure (Pa)")
        self.velocity_plot = self.create_plot("Velocity", "Time", "Velocity (m/s)")
        self.temperature_plot = self.create_plot("Temperature", "Time", "Temperature (°C)")

        self.start_button = QPushButton("Start Simulation mode")
        self.stop_button = QPushButton("Stop Simluation mode")

        self.start_button.clicked.connect(self.start_telemetry)
        self.stop_button.clicked.connect(self.stop_telemetry)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.telemetry_label)
        left_layout.addWidget(self.telemetry_display)
        left_layout.addWidget(self.start_button)
        left_layout.addWidget(self.stop_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.altitude_plot)
        right_layout.addWidget(self.pressure_plot)
        right_layout.addWidget(self.velocity_plot)
        right_layout.addWidget(self.temperature_plot)

        central_layout = QHBoxLayout()
        central_layout.addLayout(left_layout)
        central_layout.addLayout(right_layout)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        self.telemetry_timer = QTimer()
        self.telemetry_timer.timeout.connect(self.update_telemetry)

        # Initialize telemetry data
        self.telemetry_data = 0
        self.time_values = []
        self.altitude_values = []
        self.pressure_values = []
        self.velocity_values = []
        self.temperature_values = []

    def create_plot(self, title, xlabel, ylabel):
        figure, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        canvas = FigureCanvas(figure)
        return canvas

    def start_telemetry(self):
        self.telemetry_timer.start(1000)  # Update telemetry every 1000 ms

    def stop_telemetry(self):
        self.telemetry_timer.stop()

    def update_telemetry(self):
        # Simulated telemetry update with random data
        self.telemetry_data += 1
        self.time_values.append(self.telemetry_data)
        self.altitude_values.append(random.uniform(0, 100))  # Replace with actual altitude data
        self.pressure_values.append(random.uniform(90000, 110000))  # Replace with actual pressure data
        self.velocity_values.append(random.uniform(0, 5))  # Replace with actual velocity data
        self.temperature_values.append(random.uniform(20, 30))  # Replace with actual temperature data

        self.telemetry_display.append(f"Telemetry Data: {self.telemetry_data}")
        self.plot_data(self.altitude_plot, self.time_values, self.altitude_values)
        self.plot_data(self.pressure_plot, self.time_values, self.pressure_values)
        self.plot_data(self.velocity_plot, self.time_values, self.velocity_values)
        self.plot_data(self.temperature_plot, self.time_values, self.temperature_values)

    def plot_data(self, plot_canvas, x_values, y_values):
        figure = plot_canvas.figure
        ax = figure.gca()
        ax.clear()
        ax.plot(x_values, y_values, marker='o', linestyle='-', color='b')
        plot_canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gcs = CanSatGCS()
    gcs.show()
    sys.exit(app.exec())
