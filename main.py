"""
This script uses the FUTEK USB DLL Api, which is written in .NET, therefore the pythonnet module
is required, and "import clr" is from pythonnet
"""

# Qt5
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons
import numpy as np

# To deal with files, time, paths...
import clr
import os
# import pickle
import sys
import time

import core  # Module that contains the core functions

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# barra de ferramentas no grafico
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
# Garante que todas as partes do gráfico estejam dentro da figura
from matplotlib import rcParams
# Changes to rcParams are system-wide, so at the end of the program, the defaults need to be reset
rcParams.update({'figure.autolayout': True})

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
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                "torque_bench.ui"), self)
        self.ConnectSignals()
        self.CreatePlots()
        # self.CreateThreads()

        # Creates a timer to update the information on the main screen
        self.data_display_timer = QTimer()
        data_update_interval = 500  # ms
        self.data_display_timer.start(data_update_interval)
        self.data_display_timer.timeout.connect(self.UpdateDataDisplay)
        self.run = False
        self.dev_connected = False
        
    def ConnectSignals(self):
        """
        Connect the signals from buttons to functions.
        Disables any button that should only be enabled after a new simulation is created.
        """
        # Data Acquisition Window
        self.start_btn.clicked.connect(self.StartMeasurement)
        self.stop_btn.clicked.connect(self.StopMeasurement)
        self.save_btn.clicked.connect(self.SaveMeasurement)
        self.clear_btn.clicked.connect(self.Clear)

        # File Menu
        self.action_connect.triggered.connect(self.Connect)
        self.action_disconnect.triggered.connect(self.Disconnect)
        self.action_exit.triggered.connect(self.Exit)

    def CreateThreads(self):
        # Sensors thread
        self.worker = core()
        self.thread_ = QThread()
        self.worker_sensors.moveToThread(self.thread_sensors)
        # Passing the arrays to the thread
        # self.worker_sensors.signal_sensors.connect(self.update_sensors)
        self.thread_sensors.started.connect(self.worker_sensors.work)
        self.thread_sensors.start()

    def CreatePlots(self):
        """
        Initial configuration of the plots
        """
        self.plot_fig = plt.figure()
        self.plot_canvas = FigureCanvas(self.plot_fig)
        self.plot_layout.addWidget(self.plot_canvas)
        self.nav = NavigationToolbar(self.plot_canvas, self.acquisition_tab)
        self.plot_layout.addWidget(self.nav)
        self.subplot_sim = self.plot_fig.add_subplot(111)
        self.subplot_sim.grid(True, axis="y")
        self.show()

    def UpdateDataDisplay(self):
        """
        Function that updates the data displayed on the data acquisition screen periodically.
        """
        if not self.dev_connected:  # If there is no device connected, just put zeros and return
            self.rpm_txt.setText("0")
            self.torque_txt.setText("0")
            self.deg_txt.setText("0")
            self.kw_txt.setText("0")
            self.pk_txt.setText("0")
            self.track_txt.setText("0")
            self.vly_txt.setText("0")
            print("UpdateDataDisplay")
            return

        # In case there is a device connected, updates the interface
        # Gets the rotation values (necessary to use the function AngleValue and RPMValue)
        # self.usb.Get_Rotation_Values(self.ihh)
        self.rpm_txt.setText(f"{self.usb.RPMValue:.4f}")
        self.torque_txt.setText("0")
        self.deg_txt.setText(f"{self.usb.AngleValue:.4f}")
        self.kw_txt.setText("0")
        self.pk_txt.setText("0")
        self.track_txt.setText("0")
        self.vly_txt.setText("0")
        print("UpdateDataDisplay, after connection")

    def Connect(self):
        self.usb = USB_DLL()

        # Serial number of the IHH500  Elite
        serial = "479586"

        # Open the connection to the device using its serial number
        self.usb.Open_Device_Connection(serial)

        # Gets the handle and current status
        self.ihh = self.usb.DeviceHandle
        print(f"ihh_handle: {self.ihh}")
        status = self.usb.DeviceStatus
        if status != 0:
            print("Device not detected")
            self.dev_connected = False
        else:
            print(f"ihh_status: {status}")
            self.dev_connected = True

    def StartMeasurement(self):
        """
        Starts reading the data from the IHH
        """
        self.run = True

        self.thread_sensors.start()

    #TODO
    def StopMeasurement(self):
        """
        Stops and ends the measurement
        """
        self.run = False
        print("Stop")

    #TODO
    def SaveMeasurement(self):
        """
        Stops and ends the measurement
        """
        print("SaveMeasurement")

    #TODO
    def Clear(self):
        """
        Stops and ends the measurement
        """
        print("Clear")

    def Disconnect(self):
        self.dev_connected = False
        # Closes the connection at the end of the program
        dev = self.ihh
        ihh_handle = dev.DeviceHandle
        dev.Close_Device_Connection(ihh_handle)
        device_count = dev.Get_Device_Count()
        print(f"device_count: {device_count}")
        status = dev.DeviceStatus
        print(f"ihh_status: {status}")

    #TODO
    def Exit(self):
        """
        Stops and ends the measurement
        """
        print("Exit")

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