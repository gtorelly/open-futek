"""
This file is used to test the functionality of OpenFutek without the need for a GUI
"""

# To deal with files, time, paths...
import numpy as np
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