import numpy as np
import matplotlib.pyplot as p
#from astropy.time import Time
from Tkinter import Tk
from tkFileDialog import askopenfilename
from math import log10
from astropy.time import Time,TimeDelta


#def satpos(tle,time):

    #observer=ephem.Observer()
    #observer.lat="39:29:34.94"
    #observer.long= "09:14:42" 
    #observer.elevation=700.
    #satellite=ephem.readtle(tle[0],tle[1],tle[2])
    







Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
name = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print name

#times_data=Time(data_time_dati,format='iso')
#tle=['EUTELSAT 7A',           \
#'1 28187U 04008A   16343.11792845  .00000053  00000-0  00000+0 0  9999' \
#'2 28187   0.0625 357.9032 0005290 246.7311 242.1323  1.00270523 46704']


my_data = np.genfromtxt(name,skip_header=10,dtype=float)
min_sample=0
max_sample=len(my_data[:,0])

min_sample=0
max_sample=6000

p.figure(1)
p.plot(my_data[min_sample:max_sample,0],my_data[min_sample:max_sample,2],'.')
p.savefig('amplitude_AZ')
p.figure(2)
p.plot(my_data[min_sample:max_sample,2],'.')
p.savefig('amplitude')
p.figure(3)
p.plot(my_data[min_sample:max_sample,0],my_data[min_sample:max_sample,1],'.')
p.savefig('az_el')
p.figure(4)
p.plot(my_data[min_sample:max_sample,1],my_data[min_sample:max_sample,2],'.')
p.savefig('amplitude_el')



p.show()
