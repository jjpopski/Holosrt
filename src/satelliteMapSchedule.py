import ephem
from math import degrees
import sys
import argparse
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
   print ("python satelliteMapSchedule scheduleName scanning_direction size")
   
  

def main(arg):
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument("name",help="Schedule Name",type=str)
   parser.add_argument("scanlength",nargs='?',default=0.74*2,help="scan length",type=float)
   parser.add_argument("-d","--direction",type = lambda s : s.lower(),choices=['el','az'],default='az',help='Scanning direction')
   parser.add_argument("-c","--config", help="config file",default='config.txt')

   args = parser.parse_args()
   direction=args.direction
   size_init=args.scanlength
   
   
   config_file=open(args.config)
   config_parameters=config_file.readlines()
   line1=config_parameters[0]
   line2=config_parameters[1]
   line3=config_parameters[2]
   offset_az=-float(config_parameters[3])  # since 1710
   offset_el=-float(config_parameters[4]) # since 1710
   filename=str(args.name)
   sat_name=line1

   
   
   
   #offset_az=-(0.3042560000000094)
   #offset_el=-(0.02037299999999931-0.011299999999999998)
   
   #filename="map_65x64_161216_1555"
   
   filescd = open(filename+".scd","w")

   filenamelis=filename+'.lis'
   filenamebck=filename+'.bck'
   filenamecfg=filename+'.cfg'

   filelis = open(filenamelis,"w")
   filecfg = open(filenamecfg,"w")
   filebck = open(filenamebck,"w")

   
   
   
   
   filescd.write("PROJECT:\tHolography\n")
   filescd.write("OBSERVER:\tSP_GS\n")
   filescd.write("SCANLIST:\t%s\n" % filenamelis)
   filescd.write("BACKENDLIST:\t%s\n" %filenamebck )
   filescd.write("PROCEDURELIST:\t%s\n" %filenamecfg)
   filescd.write("MODE:\tSEQ\n")
   filescd.write("SCANTAG:\t1\n")
   filescd.write("INITPROC:\tNULL\n\n")
   filescd.write("SC:\t1\t%s%sMAP\tTP:MANAGEMENT/FitsZilla\n" %(sat_name,direction.upper()))
   
   filecfg.write("PROC_INIT{\n")
   filecfg.write("\tnop\n")
   filecfg.write("}\n")
   filecfg.write("PROC_NULL{\n")
   filecfg.write("}\n")
   filecfg.write("PROC_TSYS{\n")
   filecfg.write("\twait=2.000000\n")
   filecfg.write("\ttsys\n")
   filecfg.write("\twait=1\n")
   filecfg.write("}\n")
   
   filebck.write("TP:BACKENDS/TotalPower{\n")
   filebck.write("\tsetSection=0,*,300.000000,*,*,0.000100,*\n")
   filebck.write("\tsetSection=1,*,300.000000,*,*,0.000100,*\n")
   filebck.write("\tintegration=40\n")
   filebck.write("\tenable=1;1;0;0;0;0;0;0;0;0;0;0;0;0\n")
   filebck.write("}\n")
   
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
   
   
   sidereal_time=observer.sidereal_time()
   w3a.compute(observer) # compute position for observer
   sat_el= degrees(float(w3a.alt))+offset_el
   sat_az= degrees(float(w3a.az))+offset_az
   
   #size=1.4336  #degrees  
   
   
  # size_init=0.74*2 #degrees 33beam  
   
   step=0.0179

   size=size_init
   print size
   
   
   
   
   speed = beam  # beam per second 
   
    # offset to add to the scan for acceleration and brake
   
   n_scan=int(size/step)+1
   
   
   offset=0
   scan= (size-1)*step+offset
   time=size/speed
    # a fraction of beam
   
   bottom= -(int(n_scan/2)-1)*step # better to be in degrees TBD
   
   	
   #bottom= sat_el - (size /2) * step 
   tcalib=10
   
   	
   timestep=5# seconds
   j=0
   lst_actual=observer.sidereal_time()
   j=j+1
   filescd.write("1_%d\t%6.2f\t%d\tPROC_NULL\tPROC_NULL\tTP:MANAGEMENT/FitsZilla\n" %(j,tcalib,j))
   filelis.write("%d\tSIDEREAL\t%sMAP\tHOR\t%6.3fd\t%6.3fd\n" %(j,sat_name,sat_az,sat_el))
   observer.date += (tcalib +timestep) *ephem.second
   
   lst_actual=observer.sidereal_time()
   j=j+1
   filescd.write("1_%d\t%6.2f\t%d\tPROC_NULL\tPROC_NULL\tTP:MANAGEMENT/FitsZilla\n" %(j,tcalib,j))
   filelis.write("%d\tSIDEREAL\t%s\tHOR\t%6.3fd\t%6.3fd\n" %(j,sat_name,sat_az,sat_el))
   observer.date += (tcalib +timestep) *ephem.second
   
   #-HOROFFS	0.0000d	0.0000d	-RVEL	0.000000	BARY	OP
   	
   for i in range(int(n_scan)):
        sidereal_time=observer.sidereal_time()
        w3a.compute(observer) # compute position for observer
        sat_el= degrees(float(w3a.alt))+offset_el
        sat_az= degrees(float(w3a.az))+offset_az
        
        offset_el_i=bottom+i * step
        j=j+1
        lst_actual=observer.sidereal_time()
        if direction=='az':
            
           filescd.write("1_%d\t%5.3f\t%d\tPROC_NULL\tPROC_NULL\tTP:MANAGEMENT/FitsZilla\n" % (j,time,j))
           filelis.write("%d\tOTF\t%sMAP\t%7.4fd\t%7.4fd\t%6.3fd\t0.000d\tHOR\tHOR\tLAT\tCEN\tINC\t%6.3f\t-HOROFFS\t0.0000d\t%8.4fd\t-RVEL\t0.000000\tBARY\tOP\n" %(j,sat_name,sat_az,sat_el,size,time,offset_el_i))
           print(size)
        else:
           filescd.write("1_%d\t%5.3f\t%d\tPROC_NULL\tPROC_NULL\tTP:MANAGEMENT/FitsZilla\n" % (j,time,j))
           filelis.write("%d\tOTF\t%sMAP\t%7.4fd\t%7.4fd\t0.000d\t%6.3fd\tHOR\tHOR\tLON\tCEN\tINC\t%6.3f\t-HOROFFS\t%8.4fd\t0.0000d\t-RVEL\t0.000000\tBARY\tOP\n" %(j,sat_name,sat_az,sat_el,size,time,offset_el_i))
           print(size)
           
            
        observer.date += (time +timestep) *ephem.second
   
        j=j+1
        lst_actual=observer.sidereal_time()
        filescd.write("1_%d\t%6.2f\t%d\tPROC_NULL\tPROC_NULL\tTP:MANAGEMENT/FitsZilla\n" %(j,tcalib,j))
        filelis.write("%d\tSIDEREAL\t%sMAP\tHOR\t%7.4fd\t%7.4fd\n" %(j,sat_name,sat_az,sat_el))
   #        observer.date += (tcalib +timestep) *ephem.second
        observer.date += (tcalib +timestep) *ephem.second
   
   filescd.close()
   filelis.close()	
   print observer.date

if __name__ == "__main__": 
    main(sys.argv)


    
    