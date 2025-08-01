import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize
import math
import matplotlib.dates as mdates
from datetime import datetime


dates = [datetime(2025, 2, 3), datetime(2025, 5, 2), datetime(2025, 5, 20), datetime(2025, 6, 4), datetime(2025, 6, 11)]
values = [25.6, 29.7, 30.0, 30.1, 30.2]
plt.figure()
plt.errorbar(mdates.date2num(dates), values, yerr = 0.04, marker = '.', mfc = 'k', mec = 'k', linewidth = 1.5)
plt.ylabel('Resistance (m$\Omega$)')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
plt.gcf().autofmt_xdate()
plt.show()