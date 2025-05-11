# Waveshare 8CH Modbus RTU Controller - PyQt GUI

## Version: 1.0.2

### Changelog:
- Initial version with PyQt5 GUI
- Serial port selection, baudrate, unit ID
- Read 8 digital inputs
- Control 8 digital outputs
- Logging to GUI
- Added auto-installation of required dependencies if missing
- Added advanced serial connection settings (parity, stopbits, bytesize, timeout)
- Added feature to load previous settings and save log file location
- Added ability to zip project files for easy deployment

## Description:

This PyQt5-based GUI is designed to interface with the **Waveshare 8CH Modbus RTU Controller** via **Modbus RTU** communication over a **serial connection**. It provides the user with the ability to:

1. **Modbus RTU Communication**:
   - Connect to the Modbus RTU device with user-configurable serial settings such as port, baud rate, parity, etc.
   - Read 8 discrete inputs (digital states) from the Modbus device.
   - Write to 8 outputs (coils) to toggle their state (ON/OFF).

2. **User Interface (UI)**:
   - A simple PyQt5-based GUI to allow the user to connect to the Modbus device by selecting the serial port and other settings.
   - Displays the states of 8 inputs (ON/OFF) with color coding (green for ON, red for OFF).
   - Buttons to toggle the state of outputs.

3. **Logging**:
   - A log output area records actions and states, with timestamped log messages to give the user insight into the system's behavior (e.g., connection status, input/output states).

4. **Dynamic Serial Port Refresh**:
   - Automatically detects available serial ports and updates the UI to reflect the available options in the `Port` dropdown.

5. **Dependencies Check**:
   - Ensures required dependencies (`PyQt5`, `pymodbus`, `pyserial`) are installed, with automatic installation if missing.

6. **Error Handling**:
   - Provides log messages when errors occur during Modbus communication (e.g., failed connection, failed reading/writing to device).

7. **Zip Project**:
   - The `zip_project()` function allows you to package the script and any necessary files (such as `requirements.txt`) into a zip archive for easy distribution.

8. **Easy Setup**:
   - Includes a `requirements.txt` file to allow users to easily install dependencies using `pip`.

## How to Use:

1. **Install Dependencies**:
   - Ensure you have Python installed.
   - Install the required dependencies using the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

2. **Run the Application**:
   - Open a terminal, navigate to the project directory, and run the application:
     ```bash
     python modbus_gui.py
     ```

3. **Configure the Connection**:
   - Select the correct serial port from the dropdown.
   - Set the baud rate, unit ID, parity, stop bits, byte size, and timeout as required.
   - Click **Connect** to establish the connection to the Modbus device.

4. **Interact with the Inputs/Outputs**:
   - The application will display the current states of the 8 digital inputs.
   - Use the toggle buttons to control the 8 outputs (coils).

5. **Logging**:
   - The application will log all activities (e.g., connection status, input/output state changes) in the log area.
   
6. **Save Log File**:
   - At the start of the application, you will be prompted to choose a destination for saving the log file.
   - You can also load previous settings for easier configuration.

## Future Enhancements:
- Add more advanced Modbus functions (e.g., holding registers).
- Improve error handling and logging features.
- Provide more customization options for the user interface.

## License:
MIT License - see the LICENSE file for details.

## Author:
- Your Name
