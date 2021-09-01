
from PyQt5 import QtWidgets, QtCore, uic

class core(QtCore.QObject):
    """
    This class is used to create a thread that reads information from the sensor continuously.
    The signal "signal_sensors" emits a list that is read by the function "update_sensors". The list
    contains flow, volume and pressure.
    """
    def __init__(self, flw_q, prs_q):
        super().__init__()
        # Classes that creates the instances of IO classes
        self.gauge = pressure_gauge()
        # self.meter = flowmeter()
        # Associates the received queues with local variables
        self.flw_q = flw_q
        self.prs_q = prs_q

    def work(self):
        """
        Reads data from the IHH until the stop button is pressed on the interface
        """
        data = []
        while not stop_event.is_set():
            # Gets the rotation values (necessary to use the function AngleValue and RPMValue)
            dev.Get_Rotation_Values(ihh_handle)
            print(f"Angle: {dev.AngleValue}")
            print(f"RPM: {dev.RPMValue}")
            # Obtains the lines shown on the display, stores them in LCDLine1, 2, 3, 4
            dev.Get_Display_Page(ihh_handle)
            lines = [dev.LCDLine1, dev.LCDLine2, dev.LCDLine3, dev.LCDLine4]
            for line in lines:
                print(line)
            time.sleep(0.5)
