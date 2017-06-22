#For Python3.x - Tkinter section needs to be changed for Python2.x
import os
from tkinter.filedialog import askopenfilename

import pandas as pd
from NanoBetaCharlie import NanoBetaCharlie

filename = askopenfilename()
df = pd.read_csv(filename, header=None)

report = NanoBetaCharlie(df)

path_to_desktop = os.path.expanduser('~/Desktop/output.csv') 
report.clean().to_csv(path_to_desktop, encoding='utf-8')