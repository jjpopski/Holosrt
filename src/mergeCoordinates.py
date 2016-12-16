import numpy as np
from astropy.time import Time,TimeDelta
import matplotlib.pyplot as p
from Tkinter import Tk
from tkFileDialog import askopenfilename,askdirectory
from astropy.io import fits
from astropy.time import Time
import os
import fnmatch
import sys




def locate(pattern, root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

def scanDir(path,ext='*.fits'):
      ''' scan recursively a directory with subdirectories 

      scanDir(path,ext)
      path = starting point of recursion
      ext  = extension, default fits
    
      '''


      filelist=[]
      rootdir=path
      for i in locate(ext,path):
	  if 'summary' not in i:     
	    filelist.append(i)
      return filelist            

chmap={'Ch0':0,'Ch1':1,'Ch2':2,'Ch3':3,'Ch4':4,'Ch5':5,'Ch6':6}

class Beamspectra:
   def __init__(self,hdulist,ch):
      
      self.hdulist=hdulist
      self.raoff=hdulist[0].header['RightAscension Offset']
      self.decoff= hdulist[0].header['Declination Offset']
      self.vlsr=hdulist[0].header['VLSR']
      self.x_offset=hdulist['FEED TABLE'].data.field('xOffset')[chmap[ch]]
      self.y_offset=hdulist['FEED TABLE'].data.field('yOffset')[chmap[ch]]

      #self.data_elements=hdulist['DATA TABLE'].data.field('ElementNumber')
      self.data_ra2000=hdulist['DATA TABLE'].data.field('raj2000')
      self.data_dec2000=hdulist['DATA TABLE'].data.field('decj2000')
      self.data_parangle=hdulist['DATA TABLE'].data.field('par_angle')
      self.data_channel=hdulist['DATA TABLE'].data.field(ch)
      self.data_time=hdulist['DATA TABLE'].data.field('time')
      self.data_az=hdulist['DATA TABLE'].data.field('az')
      self.data_el=hdulist['DATA TABLE'].data.field('el')
      self.data_derotangle=hdulist['DATA TABLE'].data.field('derot_angle')
     

   def getxyoffset(self):
       return self.x_offset,self.y_offset
   
   def getskyoffset(self):
	   
      return self.x_offset+self.raoff,self.y_offset+self.decoff

   def getskyoffsetarcsec(self):
      
      return (self.x_offset+self.raoff)*206265,(self.y_offset+self.decoff)*206265
 
   def getSample(self):
      return self.data_channel[0]
   
   
   def getSampleAveraged(self):
        sommaon=np.zeros(len(self.data_channel[0]),dtype=type(float))
        for i in self.data_channel:
             sommaon += i
        return sommaon/len(sommaon)
   def getAzEl(self):
        
        return np.degrees(self.data_az),np.degrees(self.data_el)
   
   def getTime(self):
	
	return self.data_time




def extract_azel(name_scan): 

   #fileou=name.split('/')[-1]+'coordinates.txt'
   fileou='temp_azel.txt'
   print 'Extracting az,el from ', name_scan
   files_ns=scanDir(name_scan)
   files=sorted(files_ns)
   times=np.array([],dtype=float)
   azs=np.array([],dtype=float)
   els=np.array([],dtype=float)
   f_coordinates=open(fileou,'w')
   for name in files:
   	    hdulist = fits.open(name)
            sp=Beamspectra(hdulist,'Ch0')
            az,el=sp.getAzEl()
            time=sp.getTime()
            p.plot(time,el) 
            for i,val in enumerate(time):
               f_coordinates.write("%s %7.4f %7.4f\n" % (Time(val,format='mjd').iso,az[i],el[i]))
               
   				
            
   print Time(time,format='mjd').iso
   f_coordinates.close()
 

#my_data = np.genfromtxt('coordinates.txt', delimiter='\t',skip_header=1,dtype=float)


#coo_file=open('20161021-101330-Holography-EUTELSATAZMAPcoordinates.txt')
#data_file=open('holo_20161021_101240')
scan_name = askdirectory(title='Fits Scan directory') # show an "Open" dialog box and return the path to the selected file
name_datafile=askopenfilename(title='Data File')
data_file=open(name_datafile)

extract_azel(scan_name)
coo_file=open('temp_azel.txt')
fileou_name=name_datafile+'_merged'



data=[]
time=[]
az=[]
el=[]

time_data=[]
tuttalinea=[]

for line in coo_file:
	
	split=line.split()
	data.append(split[0])
        timedata='%s %s' % (split[0],split[1])
        time.append(timedata)
        
	az.append(split[2])
	el.append(split[3])
        



times_coo=Time(time,format='iso')
	
for line in data_file:
	if line[0] =='#' or line[0]=='A':
		continue
	
	split=line.strip().split()
	data_time_dati=split[11]+' '+split[12]
	times_data=Time(data_time_dati,format='iso')
	time_data.append(times_data)
        tuttalinea.append(line.strip())
 	



#time_data
#time_coo
i=0;
fileou=open(fileou_name,'w')

aligned=False


#occorre invertire il ciclo for
#scorrerlo sui dati Per ogni dato una coordinata di az el.
#se supera 

	   
	   



max_coo=len(times_coo)
for idx,timestamp_data in enumerate(time_data[:-1]):
     
     delta1=timestamp_data-times_coo[i]
      
  #        if (timestamp_data < times_coo[i]) and aligned==False:

     if (timestamp_data < times_coo[i]) and (abs(delta1.sec)>0.041)  :
             print 'aaa'
	     continue
     
     if aligned == False and (timestamp_data >= times_coo[i]):
	     aligned==True
	     
     while (timestamp_data > times_coo[i]):
 	     i=i+1
             if i==max_coo:
		  break
     
     
     
     if i==max_coo:
		  break
     delta=timestamp_data-times_coo[i]
     if (abs(delta.sec)<0.041):
	     fileou.write("%s %s %s\n" %(az[i],el[i],tuttalinea[idx][30:]))
	     print (az[i],el[i],timestamp_data.iso,times_coo[i].iso,delta.sec)

             continue
     #elif aligned == True and (timestamp_data < times_coo[i]):
	     #aligned == False
	     
     
     #else:
	     #aligned=True
           
    
	     
p.plot(az)
p.show()
 

#for timestamp in times_data:
	
   #for idx,val in enumerate(times_coo):
     #tt=val-timestamp
     #if tt.sec < 0.2:
	     #print val,timestamp
      
	   
	
#tau_list=[ idx  for idx, val in enumerate(time_tau) if val > timestamp]
#       tau=my_data[tau_list[0],2]


#print time


       
       