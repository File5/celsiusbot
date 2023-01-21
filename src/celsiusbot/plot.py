import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def generate_plot(data):
    hours_fmt = mdates.DateFormatter('%H:%M')
    fig, ax = plt.subplots()

    x = data['time']

    t_lims = 10, 30

    ax.set_title(x[0].strftime('%d.%m.%Y'))
    #plt.xticks(np.arange(0, 11, 1))
    ax.xaxis.set_major_formatter(hours_fmt)
    ax.set_yticks(np.arange(*t_lims, 1))
    ax.grid(which='both', axis='both')
    #plt.margins(x=0.1)
    ax.plot(x, data['temperature'], color='red', label='temperature')
    #ax.set_ylim(*t_lims)
    ax.set_ylabel('temperature (°C)', color='red')

    ax2 = ax.twinx()
    ax2.plot(x, data['humidity'], color='blue', label='humidity')
    #ax2.set_yticks(np.arange(0, 101, 10))
    ax2.set_ylim(0, 100)
    ax2.set_ylabel('humidity (%)', color='blue')

    x = data['time'][-1]
    t = data['temperature'][-1]
    h = data['humidity'][-1]
    ax2.plot(x, h, 'o', color='blue')
    ax2.annotate('{:2d} %'.format(round(h)), (x, h), xytext=(20, 0), textcoords='offset pixels', color='blue')
    ax.plot(x, t, 'ro')
    ax.annotate('{:4.1f} °C'.format(t), (x, t), xytext=(20, 0), textcoords='offset pixels', color='red')
    fig.savefig('plot.png')
