import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
import pandas as pd

provided_file = pd.read_csv('sample.csv')
time_values = provided_file['time']
pressure_values = provided_file['press']

class CanSatGCS(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_telemetry_running = False

        self.setWindowTitle("CanSat Ground Control Station")
        self.setGeometry(100, 100, 1920, 1080)

        
        self.pressure_plot = self.create_plot("Pressure", "Time", "Pressure (Pa)")
        

        self.start_button = QPushButton("Start Simulation mode")
        self.stop_button = QPushButton("Stop Simulation mode")

        self.current_time_label = QLabel("")
        self.current_time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.current_time_label.setFont(QFont("Arial", 12))

        self.endeavour_label = QLabel("Endeavour: Team #2006")
        self.endeavour_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.endeavour_label.setFont(QFont("Arial", 12))

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(13)
        self.table_widget.setHorizontalHeaderLabels(["Attribute", "Value"])
        self.table_widget.setColumnWidth(0, 200)
        self.table_widget.setColumnWidth(1, 220)

        self.telemetry_data = 0
        self.time_values = []
        self.pressure_values = []

        self.update_table_values()

        self.start_button.clicked.connect(self.start_telemetry)
        self.stop_button.clicked.connect(self.stop_telemetry)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.start_button)
        top_layout.addWidget(self.stop_button)
        top_layout.addStretch(1)

        left_layout = QVBoxLayout()
        left_layout.addLayout(top_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.pressure_plot)

        top_layout_main = QHBoxLayout()
        top_layout_main.addWidget(self.endeavour_label)
        top_layout_main.addStretch(1)
        top_layout_main.addWidget(self.current_time_label)

        central_layout = QHBoxLayout()
        central_layout.addLayout(left_layout)
        central_layout.addLayout(right_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout_main)
        main_layout.addLayout(central_layout)
        left_layout.addWidget(self.table_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.telemetry_timer = QTimer()
        self.telemetry_timer.timeout.connect(self.update_telemetry)

        # Initialize telemetry data
        self.telemetry_data = 0
        self.time_values = []
        self.pressure_values = []

        # Timer for updating the current time
        self.update_time_timer = QTimer()
        self.update_time_timer.timeout.connect(self.update_current_time)
        self.update_time_timer.start(1000)  # Update time every 1000 ms

    def create_plot(self, title, xlabel, ylabel):
        figure, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        canvas = FigureCanvas(figure)
        return canvas

    def start_telemetry(self):
        self.is_telemetry_running = True
        self.telemetry_timer.start(1000)  # Update telemetry every 1000 ms

    def stop_telemetry(self):
        self.is_telemetry_running = False
        self.telemetry_timer.stop()

    def update_telemetry(self):
        if self.telemetry_data < len(time_values):
            # Extract the next time and pressure value from the 'sample.csv'
            current_time = time_values[self.telemetry_data]
            current_pressure = pressure_values[self.telemetry_data]

            self.time_values.append(current_time)
            self.pressure_values.append(current_pressure)

            # Plot the data
            self.plot_data(self.pressure_plot, self.time_values, self.pressure_values)

            # Update table values
            self.update_table_values()

            self.telemetry_data += 1
        else:
            # Stop telemetry when all data points have been plotted
            self.stop_telemetry()

    def plot_data(self, plot_canvas, x_values, y_values):
        figure = plot_canvas.figure
        ax = figure.gca()
        ax.plot(x_values, y_values, marker='o', linestyle='-', color='b')
        plot_canvas.draw()

    def update_current_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.current_time_label.setText(current_time)

    def update_table_values(self):
        attributes = ["TEAM_ID", "MISSION_TIME", "MODE", "SIMULATION_STATE", "ALTITUDE", "VELOCITY",
                      "PRESSURE", "VOLTAGE", "GPS TIME", "GPS LATITUDE", "GPS LONGITUDE", "TILT_X", "TILT_Y"]

        simulation_state = 'Y' if self.is_telemetry_running else 'N'

        # Update table values based on simulated data
        values = ["2006", str(self.telemetry_data), "Mode Value", simulation_state]

        # Check if pressure_values is not empty before accessing its last element
        if self.pressure_values:
            values.append(str(self.pressure_values[-1]))
        else:
            values.append("")

        # Add placeholders for the rest of the values
        values.extend(["Voltage Value", "GPS Time Value", "GPS Latitude Value", "GPS Longitude Value",
                       "Tilt_X Value", "Tilt_Y Value"])

        for row, (attribute, value) in enumerate(zip(attributes, values)):
            self.table_widget.setItem(row, 0, QTableWidgetItem(attribute))
            self.table_widget.setItem(row, 1, QTableWidgetItem(value))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gcs = CanSatGCS()
    gcs.show()
    sys.exit(app.exec())
