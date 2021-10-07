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
# clr.AddReference('Futek_USB_DLL_from_sensit.dll')
from FUTEK_USB_DLL import USB_DLL
# from Futek_USB_DLL_from_sensit import USB_DLL

# file with the functions used to run this example

def ConnectDisconnect():
    """
    Basic connect and disconnect function
    """
    usb = USB_DLL()

    # Serial number of the IHH500  Elite
    serial = "479586"

    # Open the connection to the device using its serial number
    usb.Open_Device_Connection(serial)
    device_count = usb.Get_Device_Count()
    print(f"device_count: {device_count}")

    # Gets the handle and current status
    handle = usb.DeviceHandle
    print(f"ihh_handle: {handle}")
    status = usb.DeviceStatus
    print(f"ihh_status: {status}")

    # Closes the connection at the end of the program
    usb.Close_Device_Connection(handle)
    device_count = usb.Get_Device_Count()
    print(f"device_count: {device_count}")
    status = usb.DeviceStatus
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
    handle = dev.DeviceHandle
    dev.Close_Device_Connection(handle)

def GetSingleData():
    """
    Connect to a device, get the data, print and disconnect.
    """
    # Serial number of the IHH500  Elite
    serial = "479586"
    dev = Connect(serial)
    handle = dev.DeviceHandle
    channel = 2
    fullscale = dev.Get_Fullscale_Value(handle, channel)
    print(f"Maximum ADC value (Fullscale): {fullscale}")
    # The offset is not affected by the Tare obtained by pressing the button on the IHH
    offset = dev.Get_Offset_Value(handle, channel)
    print(f"ADC offset value: {offset}")
    for i in range(0, 10):
        # Normal_Data_Request returns the latest ADC value from the USB. It's maximum value is given
        # by Get_Fullscale_Value and the offset (zero point) is given by Get_Offset_Value.
        measurement = dev.Normal_Data_Request(handle, channel)
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
    handle = dev.DeviceHandle
    channel = 2

    # Not available on the IHH500
    # active_page = dev.Get_Active_Page_Number(handle, channel)
    # print(f"Active page: {active_page}")

    # Not available on the IHH500
    # ADC_Sampling_Rate_Setting = dev.Get_ADC_Sampling_Rate_Setting (handle, channel)
    # print(f"ADC Sampling Rate Setting: {ADC_Sampling_Rate_Setting}")

    # Gets the offset value of the ADC
    offset_value = dev.Get_Offset_Value(handle, channel)
    print(f"Offset Value: {offset_value}")

    # Gets the full scale value of the ADC
    fullscale = dev.Get_Fullscale_Value(handle, channel)
    print(f"Maximum ADC value (Fullscale): {fullscale}")

    # Get the latest data from the ADC
    data = dev.Normal_Data_Request(handle, channel)
    print(f"Data: {data}")

    version = dev.Version_of_Board(handle)
    print(f"Version of Board: {version}")

    display_page = dev.Get_Display_Page(handle)
    print(f"Display Page: {display_page}")

    # Gets the internal register value stored in the EEPROM of the microcontroller. 
    # Not available on the IHH500
    # tgt_register = int(0x7A)
    # print(tgt_register)
    # internal_register = dev.Get_Internal_Register(handle, tgt_register)
    # print(f"Internal Register: {internal_register}")

    # Gets the data logging value stored in memory and assigns a value to the DataLogging_Counter, 
    # DataLogging_Value1 and DataLogging_Value2.
    counter = 2
    ret_data_log = dev.Get_Data_Logging(handle, counter)
    print(f"Get_Data_Logging request response: {ret_data_log}")
    # Gets a value indicating the count associated with the sample number recorded during data 
    # logging. 
    counter = dev.DataLogging_Counter
    print(f"counter: {counter}")
    # Gets a value indicating the analog-to-digital converter (ADC) value associated with the sample
    # number recorded during data logging.
    dl_v1 = dev.DataLogging_Value1
    print(f"DataLogging_Value1: {dl_v1}")
    # Gets a value indicating the elapsed time in milliseconds associated with the sample number 
    # recorded during data logging. 
    dl_v2 = dev.DataLogging_Value2
    print(f"DataLogging_Value2: {dl_v2}")
    
    # This method is used to get the property "AngleValues"
    # TODO Test whether calling Get_Rotation_Values is necessary to get AngleValue
    ret_get_rot_val = dev.Get_Rotation_Values(handle)
    print(f"Get_Rotation_Values request response: {ret_get_rot_val}")
    angle_value = dev.AngleValue
    print(f"AngleValue: {angle_value}")

    # Get_Device_Count is a Function that is used to get the USB Device count. It also assigns a 
    # value representing the DeviceStatus of the USB Device. 
    dev_count = dev.Get_Device_Count()
    print(f"Devices connected: {dev_count}")
    # The device status is an int. "Codes Overview.pdf" specifies the meaning of each possible code.
    dev_status = dev.DeviceStatus
    print(f"Device Status: {dev_status}")

    # Get_Device_Serial_Number is a Function that is used to get the USB Device Serial Number. It 
    # also assigns a value representing the DeviceStatus of the USB Device. 
    # TODO Understand what should be the value of index to get a correct response
    index = 1
    serial = dev.Get_Device_Serial_Number(str(index))
    if serial != "Error":
        print(f"Device serial number: {serial}")
        dev_status = dev.DeviceStatus
        print(f"Device Status: {dev_status}")


    # Get_Type_of_Board is a Function that returns a value representing the Type of Board (FUTEK 
    # Model Number) of the USB Device. Return Value = (05H to FFH); The Type of Board is an "Unknown 
    # Type of Board" 
    type = dev.Get_Type_of_Board(handle)
    print(f"Type of board: {type}")
    # 
    # Get_Type_of_Board
    # Get_Hardware_Version
    # Get_Firmware_Version
    # Get_Firmware_Year
    # Get_Firmware_Month

    
    Disconnect(dev)

def GetDataLog():
    """
    Function that saves the data acquired via Data Logging and plots a figure.
    """
    # Serial number of the IHH500  Elite
    serial = "479586"
    dev = Connect(serial)
    handle = dev.DeviceHandle
    channel = 2
    # Measurement definitions
    seconds = 10
    data_logging_rate = 50  # Hz - This is the full logging data rate
    samples = seconds * data_logging_rate


    counter = dev.DataLogging_Counter
    print(f"counter: {counter}")
    ret_data_log = dev.Get_Data_Logging(handle, 10)
    counter = dev.DataLogging_Counter
    print(f"counter: {counter}")

    num_samples = dev.get_FastDataLoggingADCValue(handle)
    print(f"Get_Data_Logging: {num_samples}")
    return
    # Gets the data logging value stored in memory and assigns a value to the DataLogging_Counter, 
    # DataLogging_Value1 and DataLogging_Value2.
    for counter in range(0, samples + 1):
        ret_data_log = dev.Get_Data_Logging(handle, counter)
        print(f"Get_Data_Logging request response: {ret_data_log}")
        # Gets a value indicating the count associated with the sample number recorded during data 
        # logging. 
        counter = dev.DataLogging_Counter
        print(f"counter: {counter}")
        # Gets a value indicating the analog-to-digital converter (ADC) value associated with the sample
        # number recorded during data logging.
        dl_v1 = dev.DataLogging_Value1
        print(f"DataLogging_Value1: {dl_v1}")
        # Gets a value indicating the elapsed time in milliseconds associated with the sample number 
        # recorded during data logging. 
        dl_v2 = dev.DataLogging_Value2
        print(f"DataLogging_Value2: {dl_v2}")
    



if __name__ == '__main__':
    # ConnectDisconnect()
    # GetSingleData()
    # GetDeviceInfo()
    GetDataLog()
    # Testing

"""
List of commands available for the IHH500
Connection Commands
    Open_Device_Connection
    Close_Device_Connection

Data Link Commands
    Slave_Activity_Inquiry

Set Commands
    Set_Sensor_Identification_Number
    Set_Calibration_Register
    Set_Loading_Point
    Set_Load_of_Loading_Point
    Set_Sensor_Configuration
    Set_Load_Switch
    Set_Number_of_Loading_Points
    Set_ADC_Configuration2
    Set_Average_Setting

Get Commands
    Get_Offset_Value
    Get_Fullscale_Value
    Normal_Data_Request
    Version_of_Board
    Reset_Board
    Get_Display_Page
    Get_Internal_Register
    Get_Data_Logging
    Get_Rotation_Values
    Get_Device_Count
    Get_Device_Serial_Number
    Get_Type_of_Board
    Get_Hardware_Version
    Get_Firmware_Version
    Get_Firmware_Year
    Get_Firmware_Month

Control Commands
    Change_Battery_Enter
    Change_Tare_Up
    Change_Display_Back
    Change_Reset_Left
    Change_Menu
    Change_Unit_Right
    Change_Shunt_Exit
    Change_Hold_Down

Debugging Commands
    Read_Memory_Register
    Write_Memory_Register
    Read_EEPROM_Register
    Write_EEPROM_Register
    Read_TEDS_Register
    Write_TEDS_Register
    Read_Channel_Register
    Write_Channel_Register
"""