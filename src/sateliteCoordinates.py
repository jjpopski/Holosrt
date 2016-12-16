import ephem
import time

from math import degrees,radians
import datetime


class SatPosition:
   
    def __init__(self,observer,tle):
       self.observer=observer
       self.satellite=ephem.readtle(tle[0],tle[1],tle[2])
       
    def getPosition(self):
       self.observer.date=ephem.now()+10*ephem.minute
       
       self.satellite.compute(self.observer)
       return self.satellite.az,self.satellite.alt

def main():
    observer=ephem.Observer()
    observer.lat="39:29:34.94"
    observer.long= "09:14:42" 
    observer.elevation=700.
    config_file=open('config.txt')
    config_parameters=config_file.readlines()
    line1=config_parameters[0]
    line2=config_parameters[1]
    line3=config_parameters[2]
    print line2
    offset_az=float(config_parameters[3])  # since 1710
    offset_el=float(config_parameters[4]) # since 1710
         
    
    tle=(line1,line2,line3)
    positioner=SatPosition(observer,tle)
    try:
        while(True):
          sat_az,sat_el= positioner.getPosition()
          print "Actual SRT satellite",degrees(float(sat_az)),degrees(float(sat_el))
          pointingaz=float(sat_az)
          pointingel=float(sat_el)
          print "SRT satellite coordinates %fd %fd,%f,%f" % (degrees(pointingaz)-offset_az,degrees(pointingel)-offset_el,offset_az,offset_el)
          
          
          
           
          for t in range(10,-1,-1):
             minutes = t / 60
             seconds = t % 60
             print "%d:%2d" % (minutes,seconds) # Python v2 only
             time.sleep(1.0) 
    except KeyboardInterrupt:
        print "End Program"
    return 0
          
print __name__
if __name__=="__main__":
    main()
  

