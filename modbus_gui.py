import sys
import time
import subprocess
import importlib
import logging
import logging.handlers  # Explicit import for handlers
import os

def ensure_dependencies():
    required = ['PyQt5', 'pymodbus', 'pyserial']
    for package in required:
        try:
            importlib.import_module(package if package != 'pyserial' else 'serial')
        except ImportError:
            print(f"Installing missing package: {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

ensure_dependencies()

from PyQt5 import QtWidgets, QtGui, QtCore
from pymodbus.client.serial import ModbusSerialClient as ModbusClient
import serial.tools.list_ports

def setup_logging():
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file = os.path.join(log_directory, 'modbus_log.log')

    logger = logging.getLogger("ModbusApp")
    logger.setLevel(logging.DEBUG)
    
    # Rotating log file setup
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    return logger

class ModbusApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waveshare 8CH Modbus RTU Controller")
        self.setGeometry(200, 200, 800, 550)

        self.client = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.poll_inputs_outputs)

        self.logger = setup_logging()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()

        # Serial Settings
        serial_group = QtWidgets.QGroupBox("Serial Settings")
        serial_layout = QtWidgets.QGridLayout()

        self.port_combo = QtWidgets.QComboBox()
        self.refresh_ports()
        serial_layout.addWidget(QtWidgets.QLabel("Port:"), 0, 0)
        serial_layout.addWidget(self.port_combo, 0, 1)

        self.baudrate_input = QtWidgets.QLineEdit("9600")
        serial_layout.addWidget(QtWidgets.QLabel("Baudrate:"), 1, 0)
        serial_layout.addWidget(self.baudrate_input, 1, 1)

        self.unit_id_input = QtWidgets.QLineEdit("1")
        serial_layout.addWidget(QtWidgets.QLabel("Unit ID:"), 2, 0)
        serial_layout.addWidget(self.unit_id_input, 2, 1)

        self.parity_combo = QtWidgets.QComboBox()
        self.parity_combo.addItems(["N", "E", "O"])
        serial_layout.addWidget(QtWidgets.QLabel("Parity:"), 0, 2)
        serial_layout.addWidget(self.parity_combo, 0, 3)

        self.stopbits_input = QtWidgets.QLineEdit("1")
        serial_layout.addWidget(QtWidgets.QLabel("Stop Bits:"), 1, 2)
        serial_layout.addWidget(self.stopbits_input, 1, 3)

        self.bytesize_input = QtWidgets.QLineEdit("8")
        serial_layout.addWidget(QtWidgets.QLabel("Byte Size:"), 2, 2)
        serial_layout.addWidget(self.bytesize_input, 2, 3)

        self.timeout_input = QtWidgets.QLineEdit("1")
        serial_layout.addWidget(QtWidgets.QLabel("Timeout (s):"), 3, 0)
        serial_layout.addWidget(self.timeout_input, 3, 1)

        self.connect_btn = QtWidgets.QPushButton("Connect")
        self.connect_btn.clicked.connect(self.toggle_connection)
        serial_layout.addWidget(self.connect_btn, 3, 2, 1, 2)

        serial_group.setLayout(serial_layout)
        main_layout.addWidget(serial_group)

        # Inputs & Outputs
        io_group = QtWidgets.QGroupBox("Inputs / Outputs")
        io_layout = QtWidgets.QGridLayout()

        self.input_labels = []
        self.output_buttons = []

        for i in range(8):
            input_label = QtWidgets.QLabel(f"Input {i+1}: OFF")
            input_label.setStyleSheet("color: red")
            self.input_labels.append(input_label)
            io_layout.addWidget(input_label, i, 0)

            btn = QtWidgets.QPushButton(f"Toggle Output {i+1}")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, ch=i: self.set_output(ch, checked))
            self.output_buttons.append(btn)
            io_layout.addWidget(btn, i, 1)

        io_group.setLayout(io_layout)
        main_layout.addWidget(io_group)

        # Logging
        self.log_text = QtWidgets.QTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(QtWidgets.QLabel("Log Output:"))
        main_layout.addWidget(self.log_text)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.logger.debug(message)

    def toggle_connection(self):
        if self.client and self.client.connected:
            self.timer.stop()
            self.client.close()
            self.client = None
            self.connect_btn.setText("Connect")
            self.log("Disconnected from device")
        else:
            port = self.port_combo.currentText()
            baudrate = int(self.baudrate_input.text())
            unit_id = int(self.unit_id_input.text())
            parity = self.parity_combo.currentText()
            stopbits = int(self.stopbits_input.text())
            bytesize = int(self.bytesize_input.text())
            timeout = int(self.timeout_input.text())

            self.client = ModbusClient(
                method='rtu',
                port=port,
                baudrate=baudrate,
                parity=parity,
                stopbits=stopbits,
                bytesize=bytesize,
                timeout=timeout
            )

            if not self.client.connect():
                self.log("Failed to connect to Modbus device")
                self.client = None
            else:
                self.unit_id = unit_id
                self.connect_btn.setText("Disconnect")
                self.log(f"Connected to {port} at {baudrate} baud")
                self.timer.start(1000)

    def poll_inputs_outputs(self):
        if not self.client:
            return

        result = self.client.read_discrete_inputs(address=0x00, count=8, unit=self.unit_id)
        if not result.isError():
            for i, state in enumerate(result.bits):
                label = self.input_labels[i]
                label.setText(f"Input {i+1}: {'ON' if state else 'OFF'}")
                label.setStyleSheet(f"color: {'green' if state else 'red'}")
        else:
            self.log("Error reading digital inputs")

        result = self.client.read_coils(address=0x00, count=8, unit=self.unit_id)
        if not result.isError():
            for i, state in enumerate(result.bits):
                self.output_buttons[i].setChecked(state)
        else:
            self.log("Error reading coil states")

    def set_output(self, channel, state):
        if not self.client:
            self.log("Not connected")
            return

        address = channel
        result = self.client.write_coil(address=address, value=state, unit=self.unit_id)
        if result.isError():
            self.log(f"Failed to write to Output {channel+1}")
        else:
            self.log(f"Output {channel+1} set to {'ON' if state else 'OFF'}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ModbusApp()
    window.show()
    sys.exit(app.exec_())
