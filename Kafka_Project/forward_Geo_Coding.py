import sys
from builtins import list

from opencage.geocoder import OpenCageGeocode
import csv
mylist = []
key = '7585c234e35746da802a418ac633988e'
geocoder = OpenCageGeocode(key)
addressfile = 'addresses.txt'
try:
  with open(addressfile,'r') as f:
    for line in f:
      address = line.strip()
      result = geocoder.geocode(address, no_annotations='1')
      if result and len(result):
        latitude = result[0]['geometry']['lat']
        longitude = result[0]['geometry']['lng']
        data = str(latitude) + ','+ str(longitude) + ','+ address + "\n"
        mylist.append(data)
        file1 = open("geodetails.csv","w")
        file1.writelines(mylist)
        file1.close()
      else:
        sys.stderr.write("not found: %s\n" % address)  
except IOError:
  print('Error: File %s does not appear to exist.' % addressfile)
except RateLimitExceededError as ex:
  print(ex)


