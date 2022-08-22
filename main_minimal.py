"""
This script uses the FUTEK USB DLL Api, which is written in .NET, therefore the 
pythonnet module is required, and "import clr" is from pythonnet
"""

# Qt5
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons
import numpy as np

# To deal with files, time, paths...
import clr  # From the pythonnet module
import os
import sys

# Loading the DLL from the same folder as the python script
clr.AddReference("FUTEK_USB_DLL")
from FUTEK_USB_DLL import USB_DLL

class MainWindow(QMainWindow):
    """
    Main window
    """
    def __init__(self, parent = None):
        """
        Initialization of the main window
        """
        super(MainWindow, self).__init__(parent)
        # Loads the ui
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(self.base_path, "gui", "torque_bench_minimal.ui"), self)
        self.connect_signals()
        self.output_folder_line.setText(self.base_path)

        self.dev_connected = False
        self.got_data = False
        self.update_gui()
        
    def connect_signals(self):
        """
        Connect the signals from buttons to functions.
        Disables any button that should only be enabled after a new simulation is 
        created.
        """
        self.get_data_btn.clicked.connect(self.get_logged_data)
        self.save_btn.clicked.connect(self.save_data)
        self.connect_btn.clicked.connect(self.connect_ihh)
        self.disconnect_btn.clicked.connect(self.disconnect_ihh)
        self.output_folder_btn.clicked.connect(self.choose_output_folder)

        # File Menu actions
        self.action_connect.triggered.connect(self.connect_ihh)
        self.action_disconnect.triggered.connect(self.disconnect_ihh)
        self.action_exit.triggered.connect(exit)

    def update_gui(self):
        """
        Enables and disables buttons, updating the interface.
        """
        if self.dev_connected:
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.get_data_btn.setEnabled(True)
        
        else:
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            self.get_data_btn.setEnabled(False)

        if self.got_data:
            self.save_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)

    def connect_ihh(self):
        self.usb = USB_DLL()
        serial = self.ihh_serial_line.text()
        # Serial number of the IHH500  Elite
        # serial = "479586"
        # Serial number of the IHH500  Pro
        # serial = "482217"

        # Open the connection to the device using its serial number
        self.usb.Open_Device_Connection(serial)

        # Gets the handle and current status
        self.ihh_handle = self.usb.DeviceHandle
        print(f"ihh_handle: {self.ihh_handle}")

        status = self.usb.DeviceStatus
        if status != 0:
            print("Device not detected")
            self.dev_connected = False
        else:
            print(f"ihh_status: {status}")
            self.dev_connected = True
        self.update_gui()

    def disconnect_ihh(self):
        # Closes the connection at the end of the program
        self.usb.Close_Device_Connection(self.ihh_handle)
        print("Disconnected")
        self.dev_connected = False
        device_count = self.usb.Get_Device_Count()
        print(f"device_count: {device_count}")
        status = self.usb.DeviceStatus
        print(f"ihh_status: {status}")
        self.update_gui()

    def get_logged_data(self):
        """
        Gets the logged data from the IHH.
        """
        # If the device is not connected, trying to get data will result in an error
        if not self.dev_connected:
            print("Device is disconnected.")
            return
        try:  # double checking
            status = self.usb.DeviceStatus
            if status != 0:
                print("Device not detected")
                self.dev_connected = False
        except:
            print("Device is disconnected.")
            return

        # TODO Change from lists to numpy arrays
        # Create arrays to store the data
        adc_vals = []
        tim_vals = []

        # These values may be obtained directly from these functions or from the
        # Get_Internal_Register function
        offset_d = int(self.usb.Get_Internal_Register(self.ihh_handle, 0x02))
        print(f"{offset_d = }")

        # fullscale_d = dev.Get_Fullscale_Value(handle, channel)
        # print(f'{fullscale_d = }')
        fullscale_d = int(self.usb.Get_Internal_Register(self.ihh_handle, 0x03))
        print(f"{fullscale_d = }")

        # There is no function to get the fullscale offset value directly
        reverse_fullscale_d = int(self.usb.Get_Internal_Register(self.ihh_handle, 0x04))
        print(f"{reverse_fullscale_d = }")

        # This value comes without the decimal point
        fullscale_load_a = self.usb.Get_Internal_Register(self.ihh_handle, 0x05)
        # convert to float and correct the decimals
        fullscale_load_a = float(fullscale_load_a) * 1E-3
        print(f"{fullscale_load_a = }")

        # Gets the data logging value stored in memory and assigns a value to the 
        # DataLogging_Counter, DataLogging_Value1 and DataLogging_Value2.
        # There is no way to know the length of the data_logging. An auxiliary variable
        # verifies whether the time interval between two samples is consistent
        try:
            # Gets the first and second samples to calculate the time delay
            # Selects the sample to be read
            self.usb.Get_Data_Logging(self.ihh_handle, 0)
            # Reads the sample
            time_sample_1 = self.usb.DataLogging_Value2

            self.usb.Get_Data_Logging(self.ihh_handle, 1)
            time_sample_2 = self.usb.DataLogging_Value2

            t_delta_base = time_sample_2 - time_sample_1
        except:
            print("Couldn't obtain data to calculate t_delta_base.")
            return

        # Check if the first time interval is good
        if t_delta_base > 0:
            valid_delta_t = True
            print(f"t_delta_base: {t_delta_base} ms")
        else:
            valid_delta_t = False
            print(f"Invalid data logging time interval: {t_delta_base} ms")
            return

        # Get all samples
        sample_count = 0
        while valid_delta_t:
            self.usb.Get_Data_Logging(self.ihh_handle, sample_count)
            torq_sample = self.usb.DataLogging_Value1
            time_sample = self.usb.DataLogging_Value2
            if sample_count < 2:
                tim_vals.append(time_sample)
                adc_vals.append(torq_sample)
                sample_count +=1
                continue

            delta_t = time_sample - tim_vals[-1]
            if (delta_t <= t_delta_base + 1) and (delta_t >= t_delta_base - 1):
                # print(f"Valid time interval: {delta_t} ms")
                tim_vals.append(time_sample)
                adc_vals.append(torq_sample)
                sample_count += 1
            else:
                # print(f"Invalid time interval: {delta_t}")
                valid_delta_t = False
            # Get converted values:
        tq_vals = DA_convert(
        adc_vals, offset_d, fullscale_d, reverse_fullscale_d, fullscale_load_a
        )
        # Saves the data in globally accessible variables.
        self.adc_vals = adc_vals
        self.tim_vals = tim_vals
        self.tq_vals = tq_vals
        self.got_data = True
        self.update_gui()

    def save_data(self):
        """
        Saves the data stored in the arrays.
        """
        output_folder = self.output_folder_line.text()
        create_output_folder(output_folder)
        filename = self.file_name_line.text()
        filepath = os.path.join(output_folder, filename)
        cols = np.column_stack((self.tim_vals, self.adc_vals, self.tq_vals))
        format = ["%i", "%i", "%f"]
        header = f"Time(ms)\tADC Count\tTorque (N.cm)"
        delimiter = "\t"
        np.savetxt(filepath, cols, fmt=format, header=header, delimiter=delimiter)

    def choose_output_folder(self):
        """
        Opens a windows so that the used can define the desired output folder
        """
        folder = QFileDialog.getExistingDirectory(directory=self.base_path)
        # If the output folder was properly selected, add the os separator to it
        if folder:  
            os.path.join(folder, "")  # OS independent separator
            self.output_folder_line.setText(folder)


def create_output_folder(folder):
    """
    Checks whether the selected output folder exists or must be created.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        
def DA_convert(
    track_d_val, offset_d, fullscale_d, reverse_fullscale_d, fullscale_load_a
):
    """
    Converts a digital value (or array) to a float value.
    variables with _d are digital, integer in the ADC range (16-bit usually)
    variables with _a are analog, float.
    Inputs:
    track_d_val: Measurement, named "Tracking ADC Value" by FUTEK's software.
                Corresponds to the measured ADC value, integer.
    offset_d: Offset of the ADC circuit, corresponds to the zero of analog range.
    fullscale_d: ADC value corresponding to fullscale_load_a
    reverse_fullscale_d: ADC value corresponding to a negative fullscale_load_a
    fullscale_load_a: Calibrated limit of the measurement scale.

    Output: Converted analog value in the same units as fullscale_load_a.

    The conversion formula is:
    output = fullscale_load_a * (track_d_val-offset_d) / (fs-offset_d)
    where:
        fs = fullscale_d if track_d_val-offset > 0
        fs = reverse_fullscale_d if track_d_val-offset < 0

    """
    output = np.zeros(len(track_d_val), dtype=np.float64)
    track_d = fullscale_load_a * (np.asarray(track_d_val, dtype=np.float64) - offset_d)
    for i, val in enumerate(track_d):
        if val > 0:
            output[i] = val / (fullscale_d - offset_d)
        else:
            output[i] = val / (offset_d - reverse_fullscale_d)
    return output


if __name__ == '__main__':
    # Create the GUI application                      
    app = QApplication(sys.argv)
    # instantiate the main window
    mw = MainWindow()
    # show it
    mw.show()
    # start the Qt main loop execution, exiting from this script
    # with the same return code of Qt application
    sys.exit(app.exec_())     