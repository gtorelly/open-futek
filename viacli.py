"""
This file is used to test the functionality of OpenFutek without the need for a GUI
"""

# To deal with files, time, paths...
# import numpy as np
# import os
# import sys
import time

# Loading the DLL from the same folder as the python script
import clr
clr.AddReference('FUTEK_USB_DLL')
from FUTEK_USB_DLL import USB_DLL

# file with the functions used to run this example

def ConnectDisconnect():
    """
    Basic connect and disconnect function
    """

    dev = USB_DLL()

    # Serial number of the IHH500  Elite
    serial = "479586"

    # Open the connection to the device using its serial number
    dev.Open_Device_Connection(serial)
    device_count = dev.Get_Device_Count()
    print(f"device_count: {device_count}")

    # Gets the handle and current status
    ihh_handle = dev.DeviceHandle
    print(f"ihh_handle: {ihh_handle}")
    status = dev.DeviceStatus
    print(f"ihh_status: {status}")

    # Closes the connection at the end of the program
    dev.Close_Device_Connection(ihh_handle)
    device_count = dev.Get_Device_Count()
    print(f"device_count: {device_count}")
    status = dev.DeviceStatus
    print(f"ihh_status: {status}")

def Connect(serial):
    """
    Connect and return the USB connection instance.
    """
    dev = USB_DLL()
    # Open the connection to the device using its serial number
    dev.Open_Device_Connection(serial)
    return dev

def Disconnect(dev):
    """
    Disconnects the device, closing the USB connection
    """
    ihh_handle = dev.DeviceHandle
    dev.Close_Device_Connection(ihh_handle)

def GetSingleData():
    """
    Connect to a device, get the data, print and disconnect.
    """
    # Serial number of the IHH500  Elite
    serial = "479586"
    dev = Connect(serial)
    ihh_handle = dev.DeviceHandle
    channel = 2
    fullscale = dev.Get_Fullscale_Value(ihh_handle, channel)
    print(f"Maximum ADC value (Fullscale): {fullscale}")
    # The offset is not affected by the Tare obtained by pressing the button on the IHH
    offset = dev.Get_Offset_Value(ihh_handle, channel)
    print(f"ADC offset value: {offset}")
    for i in range(0, 10):
        # Normal_Data_Request returns the latest ADC value from the USB. It's maximum value is given
        # by Get_Fullscale_Value and the offset (zero point) is given by Get_Offset_Value.
        measurement = dev.Normal_Data_Request(ihh_handle, channel)
        print(f"Normal_Data_Request: {measurement}")
        # The compensated value is the measurement minus the offset. Not affected by the Tare.
        print(f"Compensated value: {int(measurement) - int(offset)}")
        time.sleep(0.1)
    Disconnect(dev)

def GetDeviceInfo():
    """
    Function written as a verifier just to check the information provided from various public 
    methods the API defines.
    """
    # Serial number of the IHH500  Elite
    serial = "479586"
    dev = Connect(serial)
    ihh_handle = dev.DeviceHandle
    channel = 2

    # Not available on the IHH500
    active_page = dev.Get_Active_Page_Number(ihh_handle, channel)
    print(f"Active page: {active_page}")

    # Not available on the IHH500
    ADC_Sampling_Rate_Setting = dev.Get_ADC_Sampling_Rate_Setting (ihh_handle, channel)
    print(f"ADC Sampling Rate Setting: {ADC_Sampling_Rate_Setting}")

    
    Disconnect(dev)

if __name__ == '__main__':
    # ConnectDisconnect()
    # GetSingleData()
    GetDeviceInfo()