import numpy as np
import matplotlib.pyplot as p
#from astropy.time import Time
from Tkinter import Tk
from tkFileDialog import askopenfilename
from math import log10
from astropy.time import Time,TimeDelta
import sys
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp


#def satpos(tle,time):

    #observer=ephem.Observer()
    #observer.lat="39:29:34.94"
    #observer.long= "09:14:42" 
    #observer.elevation=700.
    #satellite=ephem.readtle(tle[0],tle[1],tle[2])
    

def usage(arg):
   print "python " +arg[0] +"mergedfile"


def gaus(x, a, x0, sigma,c0):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+c0





def main(arg):

     config_file=open('config.txt')
     config_parameters=config_file.readlines()
      
     offset_az=float(config_parameters[3])  # since 1710
     offset_el=float(config_parameters[4]) # since 1710
     name = arg[1] # show an "Open" dialog box and return the path to the selected file
     print name
     
     #times_data=Time(data_time_dati,format='iso')
     #tle=['EUTELSAT 7A',           \
     #'1 28187U 04008A   16343.11792845  .00000053  00000-0  00000+0 0  9999' \
     #'2 28187   0.0625 357.9032 0005290 246.7311 242.1323  1.00270523 46704']
     
     
     my_data = np.genfromtxt(name,skip_header=10,dtype=float)
     min_sample=0
     max_sample=len(my_data[:,0])
     
     el_scan_id_min=30
     el_scan_id_max=max_sample/2-30
     
     az_scan_id_min=max_sample/2+10
     az_scan_id_max=max_sample-10
     
     print 'elevation',max_sample,el_scan_id_min,el_scan_id_max
     print 'az',max_sample,az_scan_id_min,az_scan_id_max
     
     azimuth_scan_az=my_data[az_scan_id_min:az_scan_id_max,0]
     minaz=min(azimuth_scan_az)
     maxaz=max(azimuth_scan_az)
     averaz=(minaz+maxaz)/2.
     azimuth_scan_amplitude=my_data[az_scan_id_min:az_scan_id_max,2]
     azimuth_commanded=np.mean(my_data[el_scan_id_min:el_scan_id_max,0])
     
     elevation_scan_az=my_data[el_scan_id_min:el_scan_id_max,1]
     averel=(max(elevation_scan_az)+min(elevation_scan_az))/2.
     
     
     
     elevation_scan_amplitude=my_data[el_scan_id_min:el_scan_id_max,2]
     elevation_commanded=np.mean(my_data[az_scan_id_min:az_scan_id_max,1])   
     
     print averel
     popt_az,pcov = curve_fit(gaus,azimuth_scan_az,azimuth_scan_amplitude,p0=[500000,averaz,.2,10.],bounds=(0, [1e6, 360., 1.,1e3]))
     popt_el,pcov = curve_fit(gaus,elevation_scan_az,elevation_scan_amplitude,p0=[500000,averel,.2,30.],maxfev=6000,bounds=(0, [1e6, 360., 1.,1e3]))
     print popt_el
     print popt_az
     p.plot(elevation_scan_az,elevation_scan_amplitude)
     p.show(block=False)
     fit_offset_az= azimuth_commanded-popt_az[1]
     fit_offset_el= elevation_commanded-popt_el[1]
     #min_sample=0
     #max_sample=6000
     print 'AZ peak:',popt_az[1], azimuth_commanded-popt_az[1] 
     print 'El peak:',popt_el[1], elevation_commanded-popt_el[1],elevation_commanded
     print ("OLD Offset Parameters AZ:",offset_az)    
     print ("OLD Offset Parameters EL:",offset_el) 
     print ("New Offset Parameters AZ:",offset_az+fit_offset_az)    
     print ("New Offset Parameters EL:",offset_el+fit_offset_el) 
     
     p.figure(1)
     p.plot(my_data[az_scan_id_min:az_scan_id_max,0],my_data[az_scan_id_min:az_scan_id_max,2],'.')
     p.plot(azimuth_scan_az,gaus(azimuth_scan_az,*popt_az),'-',label='fit')
     p.savefig('amplitude_AZ')
     p.figure(2)
     p.plot(my_data[min_sample:max_sample,2],'.')
     p.savefig('amplitude')
     p.figure(3)
     p.plot(my_data[min_sample:max_sample,0],my_data[min_sample:max_sample,1],'.')
     p.savefig('az_el')
     p.figure(4)
     p.plot(my_data[min_sample:max_sample,1],my_data[min_sample:max_sample,2],'.')
     p.plot(elevation_scan_az,gaus(elevation_scan_az,*popt_el),'-',label='fit')
     
     p.savefig('amplitude_el')
     p.draw()
     
     
     p.show(block=False)
     exit_plot=raw_input('Press return to exit! ')
     

if __name__ == "__main__": 
    if len(sys.argv) > 1:  	
       main(sys.argv)
    else:
       usage(sys.argv)

