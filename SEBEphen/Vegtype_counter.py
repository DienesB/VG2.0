# Author: Balazs Dienes
# Contact: dienes.balazs88@gmail.com

# This file separates an input vegtype raster to multiple vegtypes so that SEBE can separately run for each of them.

# Import libraries:
import sys
import numpy as np
from osgeo import gdal
np.set_printoptions(threshold=sys.maxsize)

def vegcounter():
    print '\nVegtype_counter.vegcounter running...'
    
    # Read vegetation_type raster:
    mainfolder = "..."
    filepathVegtype = r"..."
    vegtypeRaster = gdal.Open(filepathVegtype)
    vegtypeArray = np.array(vegtypeRaster.GetRasterBand(1).ReadAsArray())
    print 'length of vegtype array: ', len(vegtypeArray), '*', len(vegtypeArray[0]), '=', len(vegtypeArray) * len(vegtypeArray[0])

    # Remove NoData values:
    vegtypefilterArray = vegtypeArray[vegtypeArray > 0]
    print 'length of vegtype array without NoData values: ', len(vegtypefilterArray)

    # The number of vegetation layers must be equal to the number of UNIQUE values of vegetation types.
    vegtypeuniqueArray = np.unique(vegtypefilterArray)
    print 'unique values in vegtype array: ', vegtypeuniqueArray
    
    # As a result we got an array with unique vegetation type values.
    return vegtypeuniqueArray
