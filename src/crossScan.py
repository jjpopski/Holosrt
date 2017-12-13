import ephem
from math import degrees
import sys

class SatPosition:
   
    def __init__(self,observer,tle):
       self.observer=observer
       self.satellite=ephem.readtle(tle[0],tle[1],tle[2])
       
    def getPosition(self):
       self.observer.date=ephem.now()+10*ephem.minute
       
       self.satellite.compute(self.observer)
       return self.satellite.az,self.satellite.alt
          #offset_az=0.3020183890000112-0.0177  # since 1710
          #offset_el=0.028374441899998715-0.0316 # since 1710

def usage():
   print "python satelliteMapSchedule scheduleName scanning_direction size"
   
  

def main(arg):
   size=float(arg[2])

   sat_name="EUTELSAT_7A"
   
   config_file=open('config.txt')
   config_parameters=config_file.readlines()
   line1=config_parameters[0]
   line2=config_parameters[1]
   line3=config_parameters[2]
   offset_az=-float(config_parameters[3])  # since 1710
   offset_el=-float(config_parameters[4]) # since 1710
   
   
   
   #offset_az=-(0.3042560000000094)
   #offset_el=-(0.02037299999999931-0.011299999999999998)
   
   #filename="map_65x64_161216_1555"
   filename=arg[1]
   direction=arg[2]
   
   filescd = open(filename+".scd","w")
   filelis = open(filename+".lis","w")
   filenamelis=filename+'.lis'
   filescd.write("PROJECT:\tHolography\n")
   filescd.write("OBSERVER:\tSP_GS\n")
   filescd.write("SCANLIST:\t%s\n" % filenamelis)
   filescd.write("BACKENDLIST:\teutelsat_azmap.bck\n")
   filescd.write("PROCEDURELIST:\teutelsat_azmap.cfg\n")
   filescd.write("MODE:\tSEQ\n")
   filescd.write("SCANTAG:\t1\n")
   filescd.write("INITPROC:\tNULL\n\n")
   filescd.write("SC:\t1\tEUTELSATAZMAP\tTP:MANAGEMENT/FitsZilla\n")
   
   #line1='EUTELSAT 7A'             
   #line2='1 28187U 04008A   16340.05224449  .00000056  00000-0  00000+0 0  9992'
   #line3='2 28187   0.0633 352.2572 0005282 249.6501 218.2032  1.00272184 46676'
   
   w3a=ephem.readtle(line1,line2,line3)
   
   print line1
   print line2
   print line3
   print offset_az
   print offset_el
   
   
   observer=ephem.Observer()
   observer.lat="39:29:34.94"
   observer.long= "09:14:42" 
   observer.elevation=700.
   observer.date=ephem.now()+5*ephem.minute
   print observer.date
   
   beam=0.02323
   time=60.0
   
   
   sidereal_time=observer.sidereal_time()
   w3a.compute(observer) # compute position for observer
   sat_el= degrees(float(w3a.alt))+offset_el
   sat_az= degrees(float(w3a.az))+offset_az
   j=1;
   
   #size=1.4336  #degrees  
   filescd.write("1_%d\t%5.3f\t%d\tPROC_NULL\tPROC_NULL\tTP:MANAGEMENT/FitsZilla\n" % (j,time,j))
   filelis.write("%d\tOTF\tEUTELSATMAP\t%7.4fd\t%7.4fd\t%6.3fd\t0.000d\tHOR\tHOR\tLAT\tCEN\tINC\t%6.3f\t-HOROFFS\t0.0000d\t%8.4fd\t-RVEL\t0.000000\tBARY\tOP\n" %(j,sat_az,sat_el,size,time,0.0))
   j=j+1
   filescd.write("1_%d\t%5.3f\t%d\tPROC_NULL\tPROC_NULL\tTP:MANAGEMENT/FitsZilla\n" % (j,time,j))
   filelis.write("%d\tOTF\tEUTELSATMAP\t%7.4fd\t%7.4fd\t0.000d\t%6.3fd\tHOR\tHOR\tLON\tCEN\tINC\t%6.3f\t-HOROFFS\t%8.4fd\t0.0000d\t-RVEL\t0.000000\tBARY\tOP\n" %(j,sat_az,sat_el,size,time,0.0))

def usage():
   print "python crossScan.py  size"


if __name__ == "__main__": 
    if len(sys.argv) > 2:  	
       main(sys.argv)
    else:
       usage()
