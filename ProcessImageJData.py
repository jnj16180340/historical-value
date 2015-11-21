# this could be implemented anyhow

# modules installed in system
##################################################
# does importing modules everywhere use extra memory?
#import cv # opencv bindings; installed in package manager
import sys # system specific crap, LIKE sys.argv etc.
import os # system interfaces
import string
import numpy
#import Image
##################################################

##################################################
# modules from this project
#from HelperFunctions import *
#from WormCountConfigs import *
#from ImageJFormat import *
# this depends on Configs
#from ChunkImages import *
#this depends on OpenCV and lotsa other crap like that
#from CVGui import *
#from CVGuiClasses import *
##################################################

##################################################
if __name__ == '__main__':
# run from platephotos directory  
  ####### configuration
  #ants = Format() # it's form-ic, get it?

  ####### I/O init

  ####### config 
  spot_radius = 575 #pixels. could do one radius for each spot, re:origin is small
  cutoff = [17,80] # pixel^2, worm size
  summaryfile = open(os.path.join(os.getcwd(),'summary'),'w')
  
  ####### helper functions
  dist = lambda a,b: numpy.sqrt(numpy.dot(numpy.array(a)-numpy.array(b),numpy.array(a)-numpy.array(b)))
  flatten = lambda l: [item for sublist in l for item in sublist]
  #inspot = lambda coords,radius:  
  
  # this is perfectly legible
  # set of unique strings before the -*** in filenames
  #filles = list(set([ x.split('-')[0] for x in os.listdir(os.getcwd())]))
  uniquedirs = []
  uniquefiles = []
  uniquetimepoints = []
  for root, dirs, files in os.walk(os.getcwd(), topdown=True):
      for name in dirs:
	  if name == 'platephotos': 
	    uniquedirs.append(os.path.join(root,name))
	    uniquefiles.append(list(set([ x.split('-')[0] for x in os.listdir(os.path.join(root,name))])))
  # messy... this is just the 'identifying' part of the path that gives the timepoint
  #uniquetimepoints = [k.split(os.path.commonprefix(uniquex))[1] for k in uniquex]
  filles = flatten([[os.path.join(uniquedirs[m],uniquefiles[m][l]) for l in range(len(uniquedirs))] for m in range(len(uniquedirs))])
  # fUCK
  #summary line part one
  #[(os.path.basename(os.path.dirname(os.path.dirname(k))),os.path.basename(os.path.dirname(k)) ) for k in flatten(filles)]
   
  for fille in filles:
    summary_what = (os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(fille)))),os.path.basename(os.path.dirname(os.path.dirname(fille))) )
    counts = [0,0,0] # summary: origin, vehicle, butanone
    total = 0
    print 'workin` on '+fille
    outputfile = open(fille+'-distances.tsv','w')
    inputfile = open(fille+'-particles.txt','r')
    spotsfile = open(fille+'-crop.spots','r')
    
    # 5 columns in total
    # as numpy arrays
    objects = numpy.genfromtxt(inputfile,skiprows=1, usecols=(0,1,3,4,13)) # number,area,x,y,circularity
    spots = numpy.genfromtxt(spotsfile,skiprows=0)
    output = numpy.empty((objects.shape[0],objects.shape[1]+3+3+1)) # add columns for distance to each spot PLUS 3x atspot PLUS 1x showhide
    # numpy.savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n')
    #numpy.array([[1,2,4],[2,3,3]]).shape
    #print objects.shape[0]
    #print spots
    #print objects
    for row in range(objects.shape[0]):
      #print row
      distances = numpy.hstack([dist(objects[row,[2,3]],spots[0,:]),dist(objects[row,[2,3]],spots[1,:]),dist(objects[row,[2,3]],spots[2,:])])
      atspots = 1*(distances<spot_radius)
      #print objects[row,1]
      #print cutoff[1]
      showhide = ((objects[row,1]>cutoff[0]) and (objects[row,1]<cutoff[1])) # is is masked?
      #print distances
      #print atspots
      #print 1*showhide
      #print numpy.hstack([objects[row,:],distances,atspots,[1*showhide]])
      output[row,:] = numpy.hstack([objects[row,:],distances,atspots,[1*showhide]])
      
      if showhide:
	counts[0] += atspots[0]
	counts[1] += atspots[1]
	counts[2] += atspots[2]
	total +=1
    print counts
    summaryfile.write(summary_what[0]+' '+summary_what[1]+' '+str(counts[0])+' '+str(counts[1])+' '+str(counts[2])+' '+str(total)+'\n')
    ###################
    # post-loop
    numpy.savetxt(outputfile, output,fmt='%-5f')
    spotsfile.close()
    inputfile.close()
    outputfile.close()
  # end of script cleanuo
  summaryfile.close()