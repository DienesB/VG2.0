# Author: Balazs Dienes
# contact: dienes.balazs88@gmail.com

# This file sets all CDSM values to 0 if they do not represent the vegtype with which SEBE is running in this round.

import sys
import numpy as np
from osgeo import gdal
np.set_printoptions(threshold=sys.maxsize)

def CDSMCreator(genusid):
    print '\ninputCDSM_creator.CDSMCreator running...'
    mainfolder = "C:/Users/Balazs Dienes/PycharmProjects/SEBEphen/mainfolder/"

    # input CDSM to numpy array
    inputCDSM = r"mainfolder/input_CDSM/a1_cdsm.tif"
    inputRaster = gdal.Open(inputCDSM)
    CDSMArray = np.array(inputRaster.GetRasterBand(1).ReadAsArray()).astype(np.float)

    # input vegtype to numpy array
    inputVegtype = r"mainfolder/input_veg_type/a4_bet_frax.tif"
    vegtypeRaster = gdal.Open(inputVegtype)
    vegtypeArray = np.array(vegtypeRaster.GetRasterBand(1).ReadAsArray())

    # wanted vegtype value
    currgenus = genusid
    print 'current genus ID (passing argument): ', currgenus

    # if vegtype is not the wanted value, set CDSM to 0
    vegtypeArray[vegtypeArray != currgenus] = 0
    vegtypeArray[vegtypeArray == currgenus] = 1

    vegtypespecificCDSMArray = CDSMArray * vegtypeArray
    print 'length of vegtype-specific CDSM array', len(vegtypespecificCDSMArray[vegtypespecificCDSMArray!=0])
    return vegtypespecificCDSMArray
