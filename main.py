import clr
import time

# Loading the DLL from the same folder as the python script
clr.AddReference('FUTEK_USB_DLL')
from FUTEK_USB_DLL import USB_DLL

usb = USB_DLL()

# Serial number of the IHH500  Elite
serial = "479586"

# Open the connection to the device using its serial number
usb.Open_Device_Connection(serial)

# Gets the handle and current status
ihh_handle = usb.DeviceHandle
print(f"ihh_handle: {ihh_handle}")
status = usb.DeviceStatus
print(f"ihh_status: {status}")

# Reading information from the screen
t = time.time()
while time.time() - t < 1:
    # Gets the rotation values (necessary to use the function AngleValue and RPMValue)
    usb.Get_Rotation_Values(ihh_handle)
    print(f"Angle: {usb.AngleValue}")
    print(f"RPM: {usb.RPMValue}")
    # Obtains the lines shown on the display, stores them in LCDLine1, 2, 3, 4
    usb.Get_Display_Page(ihh_handle)
    lines = [usb.LCDLine1, usb.LCDLine2, usb.LCDLine3, usb.LCDLine4]
    for line in lines:
        print(line)
    time.sleep(0.5)

# usb.Change_Display_Back(ihh_handle)


# Closes the connection at the end of the program
usb.Close_Device_Connection(ihh_handle)
device_count = usb.Get_Device_Count()
print(f"device_count: {device_count}")
status = usb.DeviceStatus
print(f"ihh_status: {status}")

if __name__ == '__main__':
    start()