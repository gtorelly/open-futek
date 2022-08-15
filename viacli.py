"""
This file is used to test the functionality of OpenFutek without the need for a GUI
"""
import numpy as np
import time

import clr  # From the pythonnet module

# Loading the DLL from the same folder as the python script
clr.AddReference("FUTEK_USB_DLL")
from FUTEK_USB_DLL import USB_DLL


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
    # serial = "479586"
    # Serial number of the IHH500  Pro
    serial = "482217"
    dev = Connect(serial)
    handle = dev.DeviceHandle
    channel = 2
    # Measurement definitions
    seconds = 21
    data_logging_rate = 50  # Hz - This is the full logging data rate
    samples = seconds * data_logging_rate

    cnt_vals = []
    adc_vals = []
    tim_vals = []

    # These values may be obtained directly from these functions or from the
    # Get_Internal_Register function
    # offset_d = dev.Get_Offset_Value(handle, channel)
    # print(f'{offset_d = }')
    offset_d = int(dev.Get_Internal_Register(handle, 0x02))
    print(f"{offset_d = }")

    # fullscale_d = dev.Get_Fullscale_Value(handle, channel)
    # print(f'{fullscale_d = }')
    fullscale_d = int(dev.Get_Internal_Register(handle, 0x03))
    print(f"{fullscale_d = }")

    # There is no function to get the fullscale offset value directly
    reverse_fullscale_d = int(dev.Get_Internal_Register(handle, 0x04))
    print(f"{reverse_fullscale_d = }")

    # This value comes without the decimal point
    fullscale_load_a = float(dev.Get_Internal_Register(handle, 0x05)) * 1E-3
    print(f"{fullscale_load_a = }")


    # Gets the data logging value stored in memory and assigns a value to the 
    # DataLogging_Counter, DataLogging_Value1 and DataLogging_Value2.
    # There is no way to know the length of the data_logging. An auxiliary variable
    # verifies whether the time interval between two samples is consistent
    try:
        # Gets the first and second samples to calculate the time delay
        dev.Get_Data_Logging(handle, 0)
        time_sample_1 = dev.DataLogging_Value2

        dev.Get_Data_Logging(handle, 1)
        time_sample_2 = dev.DataLogging_Value2

        t_delta_base = time_sample_2 - time_sample_1
    except:
        print("Couldn't obtain data.")
        return

    # Check if the first time interval is good
    if t_delta_base > 0:
        valid_delta_t = True
        print(f"t_delta_base: {t_delta_base} ms")
    else:
        valid_delta_t = False
        print(f"The first data logging time interval was invalid: {t_delta_base} ms")
        return

    # Get all samples
    sample_count = 0
    while valid_delta_t:
        dev.Get_Data_Logging(handle, sample_count)
        torq_sample = dev.DataLogging_Value1
        time_sample = dev.DataLogging_Value2
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
        




    # ret_data_log = dev.Get_Data_Logging(handle, samples)
    # if ret_data_log != 0:
    #     print("There was a problem with the data logging request")
    #     print(f"Get_Data_Logging request response: {ret_data_log}")
    #     return
    # valid_delta_t = True

    # This while loop must check whether the time interval between two samples is valid
    # while valid_delta_t:
    # for counter in range(0, samples + 1):
    #     dev.Get_Data_Logging(handle, counter)
    #     # Gets a value indicating the count associated with the sample number recorded 
    #     # during data logging.
    #     counter = dev.DataLogging_Counter
    #     cnt_vals.append(counter)
    #     # print(f"counter: {counter}")
    #     # Gets a value indicating the analog-to-digital converter (ADC) value associated
    #     # with the sample number recorded during data logging.
    #     dl_v1 = dev.DataLogging_Value1
    #     adc_vals.append(dl_v1)
    #     # print(f"DataLogging_Value1: {dl_v1}")
    #     # Gets a value indicating the elapsed time in milliseconds associated with the 
    #     # sample number recorded during data logging.
    #     dl_v2 = dev.DataLogging_Value2
    #     # print(f"DataLogging_Value2: {dl_v2}")
    #     tim_vals.append(dl_v2)

    # Get converted values:
    tq_vals = DA_convert(
        adc_vals, offset_d, fullscale_d, reverse_fullscale_d, fullscale_load_a
    )
    filename = "Test.dat"
    cols = np.column_stack((tim_vals, adc_vals, tq_vals))
    format = ["%i", "%i", "%f"]
    header = f"Time(ms)\tADC Count\tTorque (N.cm)"
    delimiter = "\t"
    np.savetxt(filename, cols, fmt=format, header=header, delimiter=delimiter)


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


if __name__ == "__main__":
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

"""
Class variables of the USB_DLL class obtained with "print(USB_DLL.__dict__)"
'__repr__': <slot wrapper '__repr__' of 'USB_DLL' objects>
'__hash__': <slot wrapper '__hash__' of 'USB_DLL' objects>
'__call__': <slot wrapper '__call__' of 'USB_DLL' objects>
'__str__': <slot wrapper '__str__' of 'USB_DLL' objects>
'__lt__': <slot wrapper '__lt__' of 'USB_DLL' objects>
'__le__': <slot wrapper '__le__' of 'USB_DLL' objects>
'__eq__': <slot wrapper '__eq__' of 'USB_DLL' objects>
'__ne__': <slot wrapper '__ne__' of 'USB_DLL' objects>
'__gt__': <slot wrapper '__gt__' of 'USB_DLL' objects>
'__ge__': <slot wrapper '__ge__' of 'USB_DLL' objects>
'__iter__': <slot wrapper '__iter__' of 'USB_DLL' objects>
'__init__': <slot wrapper '__init__' of 'USB_DLL' objects>
'__getitem__': <slot wrapper '__getitem__' of 'USB_DLL' objects>
'__setitem__': <slot wrapper '__setitem__' of 'USB_DLL' objects>
'__delitem__': <slot wrapper '__delitem__' of 'USB_DLL' objects>
'__new__': <built-in method __new__ of CLR Metatype object at 0x000001943D8BAEF0>
'__doc__': 'Void .ctor()', '__module__': 'FUTEK_USB_DLL', 'ErrorDescription': <property 'ErrorDescription'>
'__overloads__': FUTEK_USB_DLL.USB_DLL(), 'Overloads': FUTEK_USB_DLL.USB_DLL()
'AngleValue': <property 'AngleValue'>
'Change_Battery_Enter': <method 'Change_Battery_Enter'>
'Change_Display_Back': <method 'Change_Display_Back'>
'Change_Hold_Down': <method 'Change_Hold_Down'>
'Change_Menu': <method 'Change_Menu'>
'Change_Reset_Left': <method 'Change_Reset_Left'>
'Change_Shunt_Exit': <method 'Change_Shunt_Exit'>
'Change_Tare_Up': <method 'Change_Tare_Up'>
'Change_Unit_Right': <method 'Change_Unit_Right'>
'Close_Device_Connection': <method 'Close_Device_Connection'>
'Create_Back_Up': <method 'Create_Back_Up'>
'CultureInformation': <property 'CultureInformation'>
'DataHighByte': <property 'DataHighByte'>
'DataLogging_Counter': <property 'DataLogging_Counter'>
'DataLogging_Value1': <property 'DataLogging_Value1'>
'DataLogging_Value2': <property 'DataLogging_Value2'>
'DataLowByte': <property 'DataLowByte'>
'DestinationIPAddress1': <property 'DestinationIPAddress1'>
'DestinationIPAddress2': <property 'DestinationIPAddress2'>
'DestinationIPAddress3': <property 'DestinationIPAddress3'>
'DestinationIPAddress4': <property 'DestinationIPAddress4'>
'DestinationMACAddress1': <property 'DestinationMACAddress1'>
'DestinationMACAddress2': <property 'DestinationMACAddress2'>
'DestinationMACAddress3': <property 'DestinationMACAddress3'>
'DestinationMACAddress4': <property 'DestinationMACAddress4'>
'DestinationMACAddress5': <property 'DestinationMACAddress5'>
'DestinationMACAddress6': <property 'DestinationMACAddress6'>
'DestinationPortNumber1': <property 'DestinationPortNumber1'>
'DestinationPortNumber2': <property 'DestinationPortNumber2'>
'DeviceHandle': <property 'DeviceHandle'>
'DeviceStatus': <property 'DeviceStatus'>
'DisplayPage': <property 'DisplayPage'>
'Fast_Data_Request': <method 'Fast_Data_Request'>
'Get_Active_Page_Number': <method 'Get_Active_Page_Number'>
'Get_ADC_PGA_Setting': <method 'Get_ADC_PGA_Setting'>
'Get_ADC_Sampling_Rate_Setting': <method 'Get_ADC_Sampling_Rate_Setting'>
'Get_Analog_Voltage_Output': <method 'Get_Analog_Voltage_Output'>
'get_AngleValue': <method 'get_AngleValue'>
'Get_Average_Setting': <method 'Get_Average_Setting'>
'Get_Bridge_Resistance': <method 'Get_Bridge_Resistance'>
'Get_Calibration_Code': <method 'Get_Calibration_Code'>
'Get_Calibration_Day': <method 'Get_Calibration_Day'>
'Get_Calibration_Month': <method 'Get_Calibration_Month'>
'Get_Calibration_Year': <method 'Get_Calibration_Year'>
'Get_CrossTalk': <method 'Get_CrossTalk'>
'get_CultureInformation': <method 'get_CultureInformation'>
'Get_Data_Logging': <method 'Get_Data_Logging'>
'get_DataHighByte': <method 'get_DataHighByte'>
'get_DataLogging_Counter': <method 'get_DataLogging_Counter'>
'get_DataLogging_Value1': <method 'get_DataLogging_Value1'>
'get_DataLogging_Value2': <method 'get_DataLogging_Value2'>
'get_DataLowByte': <method 'get_DataLowByte'>
'Get_Decimal_Point': <method 'Get_Decimal_Point'>
'Get_Destination_IP_Address': <method 'Get_Destination_IP_Address'>
'Get_Destination_MAC_Address': <method 'Get_Destination_MAC_Address'>
'Get_Destination_Port_Number': <method 'Get_Destination_Port_Number'>
'get_DestinationIPAddress1': <method 'get_DestinationIPAddress1'>
'get_DestinationIPAddress2': <method 'get_DestinationIPAddress2'>
'get_DestinationIPAddress3': <method 'get_DestinationIPAddress3'>
'get_DestinationIPAddress4': <method 'get_DestinationIPAddress4'>
'get_DestinationMACAddress1': <method 'get_DestinationMACAddress1'>
'get_DestinationMACAddress2': <method 'get_DestinationMACAddress2'>
'get_DestinationMACAddress3': <method 'get_DestinationMACAddress3'>
'get_DestinationMACAddress4': <method 'get_DestinationMACAddress4'>
'get_DestinationMACAddress5': <method 'get_DestinationMACAddress5'>
'get_DestinationMACAddress6': <method 'get_DestinationMACAddress6'>
'get_DestinationPortNumber1': <method 'get_DestinationPortNumber1'>
'get_DestinationPortNumber2': <method 'get_DestinationPortNumber2'>
'Get_Device_Count': <method 'Get_Device_Count'>
'Get_Device_Serial_Number': <method 'Get_Device_Serial_Number'>
'get_DeviceHandle': <method 'get_DeviceHandle'>
'get_DeviceStatus': <method 'get_DeviceStatus'>
'Get_Direction': <method 'Get_Direction'>
'Get_Display_Page': <method 'Get_Display_Page'>
'get_DisplayPage': <method 'get_DisplayPage'>
'get_ErrorDescription': <method 'get_ErrorDescription'>
'Get_Excitation': <method 'Get_Excitation'>
'get_FastDataLoggingADCValue': <method 'get_FastDataLoggingADCValue'>
'get_FastDataLoggingCounter': <method 'get_FastDataLoggingCounter'>
'get_FastDataLoggingDateAndTime': <method 'get_FastDataLoggingDateAndTime'>
'get_FastDataLoggingNumberOfSamples': <method 'get_FastDataLoggingNumberOfSamples'>
'get_FastDataLoggingSampleNumber': <method 'get_FastDataLoggingSampleNumber'>
'Get_Firmware_Month': <method 'Get_Firmware_Month'>
'Get_Firmware_Version': <method 'Get_Firmware_Version'>
'Get_Firmware_Year': <method 'Get_Firmware_Year'>
'Get_Fullscale_Load': <method 'Get_Fullscale_Load'>
'Get_Fullscale_Value': <method 'Get_Fullscale_Value'>
'Get_Gain_Switch': <method 'Get_Gain_Switch'>
'Get_Hardware_Version': <method 'Get_Hardware_Version'>
'Get_Internal_Register': <method 'Get_Internal_Register'>
'get_LCDLine1': <method 'get_LCDLine1'>
'get_LCDLine2': <method 'get_LCDLine2'>
'get_LCDLine3': <method 'get_LCDLine3'>
'get_LCDLine4': <method 'get_LCDLine4'>
'Get_Load_of_Loading_Point': <method 'Get_Load_of_Loading_Point'>
'Get_Loading_Point': <method 'Get_Loading_Point'>
'Get_Number_of_Active_Channels': <method 'Get_Number_of_Active_Channels'>
'Get_Number_of_Loading_Points': <method 'Get_Number_of_Loading_Points'>
'Get_Offset_Load': <method 'Get_Offset_Load'>
'Get_Offset_Value': <method 'Get_Offset_Value'>
'Get_Output_Type': <method 'Get_Output_Type'>
'get_PacketReceived': <method 'get_PacketReceived'>
'get_PacketSent': <method 'get_PacketSent'>
'Get_Polarity': <method 'Get_Polarity'>
'Get_Pulses_Per_Rotation': <method 'Get_Pulses_Per_Rotation'>
'Get_Rotation_Values': <method 'Get_Rotation_Values'>
'get_RPMValue': <method 'get_RPMValue'>
'Get_Sensitivity': <method 'Get_Sensitivity'>
'Get_Sensor_Identification_Number': <method 'Get_Sensor_Identification_Number'>
'Get_Sensor_Sensitivity': <method 'Get_Sensor_Sensitivity'>
'Get_Shunt_Resistor': <method 'Get_Shunt_Resistor'>
'Get_Shunt_Value': <method 'Get_Shunt_Value'>
'Get_Source_IP_Address': <method 'Get_Source_IP_Address'>
'Get_Source_MAC_Address': <method 'Get_Source_MAC_Address'>
'Get_Source_Port_Number': <method 'Get_Source_Port_Number'>
'get_SourceIPAddress1': <method 'get_SourceIPAddress1'>
'get_SourceIPAddress2': <method 'get_SourceIPAddress2'>
'get_SourceIPAddress3': <method 'get_SourceIPAddress3'>
'get_SourceIPAddress4': <method 'get_SourceIPAddress4'>
'get_SourceMACAddress1': <method 'get_SourceMACAddress1'>
'get_SourceMACAddress2': <method 'get_SourceMACAddress2'>
'get_SourceMACAddress3': <method 'get_SourceMACAddress3'>
'get_SourceMACAddress4': <method 'get_SourceMACAddress4'>
'get_SourceMACAddress5': <method 'get_SourceMACAddress5'>
'get_SourceMACAddress6': <method 'get_SourceMACAddress6'>
'get_SourcePortNumber1': <method 'get_SourcePortNumber1'>
'get_SourcePortNumber2': <method 'get_SourcePortNumber2'>
'Get_Span_1_Potentiometer': <method 'Get_Span_1_Potentiometer'>
'Get_Span_2_Potentiometer': <method 'Get_Span_2_Potentiometer'>
'Get_Type_of_Board': <method 'Get_Type_of_Board'>
'Get_Type_of_Calibration': <method 'Get_Type_of_Calibration'>
'Get_Unit_Code': <method 'Get_Unit_Code'>
'get_VirtualMode': <method 'get_VirtualMode'>
'get_VirtualSerialNumber': <method 'get_VirtualSerialNumber'>
'Get_Voltage_Output': <method 'Get_Voltage_Output'>
'Get_Zero_Potentiometer': <method 'Get_Zero_Potentiometer'>
'LCDLine1': <property 'LCDLine1'>
'LCDLine2': <property 'LCDLine2'>
'LCDLine3': <property 'LCDLine3'>
'LCDLine4': <property 'LCDLine4'>
'Normal_Data_Request': <method 'Normal_Data_Request'>
'Open_Device_Connection': <method 'Open_Device_Connection'>
'PacketReceived': <property 'PacketReceived'>
'PacketSent': <property 'PacketSent'>
'Read_Channel_Register': <method 'Read_Channel_Register'>
'Read_EEPROM_Register': <method 'Read_EEPROM_Register'>
'Read_Memory_Register': <method 'Read_Memory_Register'>
'Read_Page_Register': <method 'Read_Page_Register'>
'Read_TEDS_Channel_Register': <method 'Read_TEDS_Channel_Register'>
'Read_TEDS_Register': <method 'Read_TEDS_Register'>
'Reset_Angle': <method 'Reset_Angle'>
'Reset_Board': <method 'Reset_Board'>
'Restore_Back_Up': <method 'Restore_Back_Up'>
'RPMValue': <property 'RPMValue'>
'Set_Active_Page_Number': <method 'Set_Active_Page_Number'>
'Set_ADC_Configuration': <method 'Set_ADC_Configuration'>
'Set_ADC_Configuration2': <method 'Set_ADC_Configuration2'>
'Set_Average_Setting': <method 'Set_Average_Setting'>
'Set_Bridge_Resistance': <method 'Set_Bridge_Resistance'>
'Set_Calibration_Code': <method 'Set_Calibration_Code'>
'Set_Calibration_Day': <method 'Set_Calibration_Day'>
'Set_Calibration_Mode': <method 'Set_Calibration_Mode'>
'Set_Calibration_Month': <method 'Set_Calibration_Month'>
'Set_Calibration_Register': <method 'Set_Calibration_Register'>
'Set_Calibration_Year': <method 'Set_Calibration_Year'>
'Set_CrossTalk': <method 'Set_CrossTalk'>
'set_CultureInformation': <method 'set_CultureInformation'>
'Set_Decimal_Point': <method 'Set_Decimal_Point'>
'Set_Destination_IP_Address': <method 'Set_Destination_IP_Address'>
'Set_Destination_MAC_Address': <method 'Set_Destination_MAC_Address'>
'Set_Destination_Port_Number': <method 'Set_Destination_Port_Number'>
'Set_Digital_Components': <method 'Set_Digital_Components'>
'Set_Direction': <method 'Set_Direction'>
'set_FastDataLoggingCounter': <method 'set_FastDataLoggingCounter'>
'Set_Load_of_Loading_Point': <method 'Set_Load_of_Loading_Point'>
'Set_Load_Switch': <method 'Set_Load_Switch'>
'Set_Loading_Point': <method 'Set_Loading_Point'>
'Set_Number_of_Active_Channels': <method 'Set_Number_of_Active_Channels'>
'Set_Number_of_Loading_Points': <method 'Set_Number_of_Loading_Points'>
'Set_Pulses_Per_Rotation': <method 'Set_Pulses_Per_Rotation'>
'Set_Sensitivity': <method 'Set_Sensitivity'>
'Set_Sensor_Configuration': <method 'Set_Sensor_Configuration'>
'Set_Sensor_Identification_Number': <method 'Set_Sensor_Identification_Number'>
'Set_Shunt_Value': <method 'Set_Shunt_Value'>
'Set_Source_IP_Address': <method 'Set_Source_IP_Address'>
'Set_Source_Port_Number': <method 'Set_Source_Port_Number'>
'Set_Type_of_Calibration': <method 'Set_Type_of_Calibration'>
'Set_Unit_Code': <method 'Set_Unit_Code'>
'set_VirtualMode': <method 'set_VirtualMode'>
'Set_Voltage_Output': <method 'Set_Voltage_Output'>
'Set_Zero_Correction': <method 'Set_Zero_Correction'>
'Slave_Activity_Inquiry': <method 'Slave_Activity_Inquiry'>
'SourceIPAddress1': <property 'SourceIPAddress1'>
'SourceIPAddress2': <property 'SourceIPAddress2'>
'SourceIPAddress3': <property 'SourceIPAddress3'>
'SourceIPAddress4': <property 'SourceIPAddress4'>
'SourceMACAddress1': <property 'SourceMACAddress1'>
'SourceMACAddress2': <property 'SourceMACAddress2'>
'SourceMACAddress3': <property 'SourceMACAddress3'>
'SourceMACAddress4': <property 'SourceMACAddress4'>
'SourceMACAddress5': <property 'SourceMACAddress5'>
'SourceMACAddress6': <property 'SourceMACAddress6'>
'SourcePortNumber1': <property 'SourcePortNumber1'>
'SourcePortNumber2': <property 'SourcePortNumber2'>
'Version_of_Board': <method 'Version_of_Board'>
'VirtualMode': <property 'VirtualMode'>
'VirtualSerialNumber': <property 'VirtualSerialNumber'>
'Write_Channel_Register': <method 'Write_Channel_Register'>
'Write_EEPROM_Register': <method 'Write_EEPROM_Register'>
'Write_Memory_Register': <method 'Write_Memory_Register'>
'Write_TEDS_Channel_Register': <method 'Write_TEDS_Channel_Register'>
'Write_TEDS_Register': <method 'Write_TEDS_Register'>
"""

"""

"""
