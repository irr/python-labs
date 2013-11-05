#!/usr/bin/python
"""Simple static plot, mostly for testing zooming..."""

# sudo pip-python install numpy matplotlib mplh5canvas

import matplotlib
import mplh5canvas
mplh5canvas.set_log_level("warning")
 # set the log level before using module
 # default is 'warning', it is done here
 # to illustrate the syntax
matplotlib.use('module://mplh5canvas.backend_h5canvas')
from pylab import *
import time

t = arange(0, 100, 1)
s = sin(2*pi*t/10) * 10
plot(t, s, linewidth=1.0)
xlabel('time (s)')
ylabel('voltage (mV)')
title('Frist Post')
f = gcf()
show(open_plot=True)
