#read pressure sim values and store it .create telemetry string and transfer it via xbee to fsw
#example string: CMD,2006,SIMP,XYZ​
import matplotlib.pyplot as plt
import pandas as pd

provided_csv = pd.read_csv('sample.csv')

