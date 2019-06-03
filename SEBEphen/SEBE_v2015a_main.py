
# This is the main file for the SEBE model, python version (Made for Python 2.x)
# Author of SEBE: Fredrik Lindberg, fredrikl@gvc.gu.se

# SEBE has been modified by Balazs Dienes to include leaf phenology
# Author of SEBEphen: Balazs Dienes
# contact: dienes.balazs88@gmail.com

import Solweig_v2015_metdata_noload as metload
import SEBE_v2015_calc as so
from Utilities.misc import *
from osgeo import gdal, osr
from SEBEfiles.sunmapcreator_2015a import sunmapcreator_2015a
import matplotlib.pylab as plt
from Utilities.misc import saveraster

#Import transmissivity calculation:
import Stratified_irradiance as strata
import Vegtype_counter as vegcounter
import Veg_objects as vegobjects
import inputCDSM_creator as cdsmcreator

# Input settings
mainfolder = ".../"
metfilepath = mainfolder + '... .txt'
outfolder = mainfolder + '.../'
inputDSM = '... .tif'
inputWallAspect = '... .tif'
inputWallHeight = '... .tif'
usevegdem = 1
onlyglobal = 1
canopyToTrunkRatio = 0.3
UTC = 1
alt = 150.0
voxelheight = 1.
albedo = 0.15
calc_month = 0  # This does not work yet
output = {'energymonth': 0, 'energyyear': 1, 'suitmap': 0}

# load surface grids
dataSetDSM = gdal.Open(mainfolder + inputDSM)
dsm = dataSetDSM.ReadAsArray().astype(np.float)

# find latlon etc.
old_cs = osr.SpatialReference()
dsm_ref = dataSetDSM.GetProjection()
old_cs.ImportFromWkt(dsm_ref)


wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""

new_cs = osr.SpatialReference()
new_cs.ImportFromWkt(wgs84_wkt)

transform = osr.CoordinateTransformation(old_cs, new_cs)

width1 = dataSetDSM.RasterXSize
height1 = dataSetDSM.RasterYSize
gt = dataSetDSM.GetGeoTransform()
minx = gt[0]
miny = gt[3] + width1 * gt[4] + height1 * gt[5]
lonlat = transform.TransformPoint(minx, miny)
geotransform = dataSetDSM.GetGeoTransform()
scale = 1 / geotransform[1]
lon = lonlat[0]
lat = lonlat[1]
rows = dsm.shape[0]
cols = dsm.shape[1]

dataSet = gdal.Open(mainfolder + inputWallHeight)
wallheight = dataSet.ReadAsArray().astype(np.float)
dataSet = gdal.Open(mainfolder + inputWallAspect)
wallaspect = dataSet.ReadAsArray().astype(np.float)

slope, aspect = get_ders(dsm, scale)

# Processing of metdata
metin = np.loadtxt(metfilepath, skiprows=1, delimiter=' ')

for line in metin:
    met = np.zeros((1, 24)) + line

    location = {'longitude': lon, 'latitude': lat, 'altitude': alt}
    YYYY, altitude, azimuth, zen, jday, leafon, dectime, altmax = metload.Solweig_2015a_metdata_noload(met, location, UTC)
    radmatI, radmatD, radmatR = sunmapcreator_2015a(met, altitude, azimuth, onlyglobal, output, jday, albedo, location, zen)

    print 'YYYY, altitude, azimuth, zen, jday, leafon, dectime, altmax', YYYY, altitude, azimuth, zen, jday, leafon, dectime, altmax
    #print 'radmatI, radmatD, radmatR', radmatI, radmatD, radmatR

    # Create objects for existing vegtypes:
    plant1 = vegobjects.vegobjects()
    plant2 = vegobjects.vegobjects()
    plant3 = vegobjects.vegobjects()
    plant4 = vegobjects.vegobjects()
    plant5 = vegobjects.vegobjects()
    plant6 = vegobjects.vegobjects()
    plant7 = vegobjects.vegobjects()
    plant8 = vegobjects.vegobjects()
    noplantwallmatrix = 0

    if usevegdem == 1:

        # Read all unique vegtypes:
        uniquevegtype = vegcounter.vegcounter()
        print 'unique vegtypes in main: ', uniquevegtype

        # ACER:
        if np.any(uniquevegtype == 1):
            plant1.name = "Acer"
            # Create CDSM for Acer:
            plant1.vegtypeCDSM = cdsmcreator.CDSMCreator(1)
            vegdsm = plant1.vegtypeCDSM
            vegdsm2 = vegdsm * canopyToTrunkRatio
            # Calculate transmissivity for Acer:
            plant1.transmiss = strata.transmissivity(line[1], 1)
            psi = plant1.transmiss
            print 'Psi of object 1: ', psi
            # Run SEBE for Acer:
            plant1.wallmatrix = so.SEBE_2015a_calc(dsm, scale, slope, aspect, voxelheight, cols, rows, vegdsm, vegdsm2,
                                 wallheight, wallaspect, albedo, psi, radmatI, radmatD, radmatR, usevegdem, calc_month)
            wallrow = plant1.wallmatrix[1]
            wallcol = plant1.wallmatrix[2]
            plant1.wallmatrix = plant1.wallmatrix[0]

        # BETULA:
        if np.any(uniquevegtype == 2):
            plant2.name = "Betula"
            # Create CDSM for Betula:
            plant2.vegtypeCDSM = cdsmcreator.CDSMCreator(2)
            vegdsm = plant2.vegtypeCDSM
            vegdsm2 = vegdsm * canopyToTrunkRatio
            # Calculate transmissivity for Betula:
            plant2.transmiss = strata.transmissivity(line[1], 2)
            psi = plant2.transmiss
            print 'Psi of object 2: ', psi
            # Run SEBE for Betula:
            plant2.wallmatrix = so.SEBE_2015a_calc(dsm, scale, slope, aspect, voxelheight, cols, rows, vegdsm, vegdsm2,
                                 wallheight, wallaspect, albedo, psi, radmatI, radmatD, radmatR, usevegdem, calc_month)
            wallrow = plant2.wallmatrix[1]
            wallcol = plant2.wallmatrix[2]
            plant2.wallmatrix = plant2.wallmatrix[0]

        # FRAXINUS:
        if np.any(uniquevegtype == 3):
            plant3.name = "Fraxinus"
            # Create CDSM for Fraxinus:
            plant3.vegtypeCDSM = cdsmcreator.CDSMCreator(3)
            vegdsm = plant3.vegtypeCDSM
            vegdsm2 = vegdsm * canopyToTrunkRatio
            # Calculate transmissivity for Fraxinus:
            plant3.transmiss = strata.transmissivity(line[1], 3)
            psi = plant3.transmiss
            print 'Psi of object 3: ', psi
            # Run SEBE for Fraxinus:
            plant3.wallmatrix = so.SEBE_2015a_calc(dsm, scale, slope, aspect, voxelheight, cols, rows, vegdsm, vegdsm2,
                                 wallheight, wallaspect, albedo, psi, radmatI, radmatD, radmatR, usevegdem, calc_month)
            wallrow = plant3.wallmatrix[1]
            wallcol = plant3.wallmatrix[2]
            plant3.wallmatrix = plant3.wallmatrix[0]

        # PLATANUS:
        if np.any(uniquevegtype == 4):
            plant4.name = "Platanus"
            # Create CDSM for Platanus:
            plant4.vegtypeCDSM = cdsmcreator.CDSMCreator(4)
            vegdsm = plant4.vegtypeCDSM
            vegdsm2 = vegdsm * canopyToTrunkRatio
            # Calculate transmissivity for Platanus:
            plant4.transmiss = strata.transmissivity(line[1], 4)
            psi = plant4.transmiss
            print 'Psi of object 4: ', psi
            # Run SEBE for Platanus:
            plant4.wallmatrix = so.SEBE_2015a_calc(dsm, scale, slope, aspect, voxelheight, cols, rows, vegdsm, vegdsm2,
                                 wallheight, wallaspect, albedo, psi, radmatI, radmatD, radmatR, usevegdem, calc_month)
            wallrow = plant4.wallmatrix[1]
            wallcol = plant4.wallmatrix[2]
            plant4.wallmatrix = plant4.wallmatrix[0]

        # QUERCUS:
        if np.any(uniquevegtype == 5):
            plant5.name = "Quercus"
            # Create CDSM for Quercus:
            plant5.vegtypeCDSM = cdsmcreator.CDSMCreator(5)
            vegdsm = plant5.vegtypeCDSM
            vegdsm2 = vegdsm * canopyToTrunkRatio
            # Calculate transmissivity for Quercus:
            plant5.transmiss = strata.transmissivity(line[1], 5)
            psi = plant5.transmiss
            print 'Psi of object 5: ', psi
            # Run SEBE for Quercus:
            plant5.wallmatrix = so.SEBE_2015a_calc(dsm, scale, slope, aspect, voxelheight, cols, rows, vegdsm, vegdsm2,
                                 wallheight, wallaspect, albedo, psi, radmatI, radmatD, radmatR, usevegdem, calc_month)
            wallrow = plant5.wallmatrix[1]
            wallcol = plant5.wallmatrix[2]
            plant5.wallmatrix = plant5.wallmatrix[0]

        # TILIA:
        if np.any(uniquevegtype == 6):
            plant6.name = "Tilia"
            # Create CDSM for Tilia:
            plant6.vegtypeCDSM = cdsmcreator.CDSMCreator(6)
            vegdsm = plant6.vegtypeCDSM
            vegdsm2 = vegdsm * canopyToTrunkRatio
            # Calculate transmissivity for Tilia:
            plant6.transmiss = strata.transmissivity(line[1], 6)
            psi = plant6.transmiss
            print 'Psi of object 6: ', psi
            # Run SEBE for Tilia:
            plant6.wallmatrix = so.SEBE_2015a_calc(dsm, scale, slope, aspect, voxelheight, cols, rows, vegdsm, vegdsm2,
                                 wallheight, wallaspect, albedo, psi, radmatI, radmatD, radmatR, usevegdem, calc_month)
            wallrow = plant6.wallmatrix[1]
            wallcol = plant6.wallmatrix[2]
            plant6.wallmatrix = plant6.wallmatrix[0]

        # AESCULUS:
        if np.any(uniquevegtype == 7):
            plant7.name = "Aesculus"
            # Create CDSM for Aesculus:
            plant7.vegtypeCDSM = cdsmcreator.CDSMCreator(7)
            vegdsm = plant7.vegtypeCDSM
            vegdsm2 = vegdsm * canopyToTrunkRatio
            # Calculate transmissivity for Aesculus:
            plant7.transmiss = strata.transmissivity(line[1], 7)
            psi = plant7.transmiss
            print 'Psi of object 7: ', psi
            # Run SEBE for Fraxinus:
            plant7.wallmatrix = so.SEBE_2015a_calc(dsm, scale, slope, aspect, voxelheight, cols, rows, vegdsm, vegdsm2,
                                 wallheight, wallaspect, albedo, psi, radmatI, radmatD, radmatR, usevegdem, calc_month)
            wallrow = plant7.wallmatrix[1]
            wallcol = plant7.wallmatrix[2]
            plant7.wallmatrix = plant7.wallmatrix[0]

        # PINUS:
        if np.any(uniquevegtype == 8):
            plant8.name = "Pinus"
            # Create CDSM for Pinus:
            plant8.vegtypeCDSM = cdsmcreator.CDSMCreator(8)
            vegdsm = plant8.vegtypeCDSM
            vegdsm2 = vegdsm * canopyToTrunkRatio
            # Calculate transmissivity for Pinus:
            # Pinus transmissivity is constant throughout the year, no need for linear regression in this case:
            plant8.transmiss = 0.051 #i.e. 5.1%, see Konarska et al. 2013
            psi = plant8.transmiss
            print 'Psi of object 8: ', psi
            # Run SEBE for Pinus:
            plant8.wallmatrix = so.SEBE_2015a_calc(dsm, scale, slope, aspect, voxelheight, cols, rows, vegdsm, vegdsm2,
                                 wallheight, wallaspect, albedo, psi, radmatI, radmatD, radmatR, usevegdem, calc_month)
            wallrow = plant8.wallmatrix[1]
            wallcol = plant8.wallmatrix[2]
            plant8.wallmatrix = plant8.wallmatrix[0]

    else:
        print 'No vegetation raster applied in this run'
        vegdsm = np.zeros([rows, cols])
        vegdsm2 = np.zeros([rows, cols])
        psi = 0.03
        noplantwallmatrix = so.SEBE_2015a_calc(dsm, scale, slope, aspect, voxelheight, cols, rows, vegdsm, vegdsm2,
                                 wallheight, wallaspect, albedo, psi, radmatI, radmatD, radmatR, usevegdem, calc_month)
        wallrow = noplantwallmatrix[1]
        wallcol = noplantwallmatrix[2]
        noplantwallmatrix = noplantwallmatrix[0]

    print '\nMain running...'
    print 'Length of non-zero inputCDSM: ', len(vegdsm[vegdsm!=0])
    print 'Psi value applied in this run: ', psi, '\n'

    # At this stage there are two possibilities:
    # we either do use vegeration raster or do not.
    # If vegetation raster is not used, i.e the noplatwallmatrix variable was overwritten by SEBE, we are finished:
    if noplantwallmatrix != 0:
        minmatrix = np.asarray(noplantwallmatrix)

    else:
        # In case we use vegetation raster, a wallmatrix can be either overwritten by the return value from SEBE
        # (for trees that are in the AOI) or still remain as 0s (for trees not in the AOI)
        # 0 wallmatrices will be replaced to NaN matrices so that they do not take part in the combination process later.

        # Firstly, the length of non-zero wallmatrices is to be identified:
        if plant1.wallmatrix != 0:
            wallaxis1 = len(plant1.wallmatrix)  # 145
            wallaxis2 = len(plant1.wallmatrix[0])
            wallaxis3 = len(plant1.wallmatrix[0][0])
        elif plant2.wallmatrix != 0:
            wallaxis1 = len(plant2.wallmatrix)  # 145
            wallaxis2 = len(plant2.wallmatrix[0])
            wallaxis3 = len(plant2.wallmatrix[0][0])
        elif plant3.wallmatrix != 0:
            wallaxis1 = len(plant3.wallmatrix)  # 145
            wallaxis2 = len(plant3.wallmatrix[0])
            wallaxis3 = len(plant3.wallmatrix[0][0])
        elif plant4.wallmatrix != 0:
            wallaxis1 = len(plant4.wallmatrix)  # 145
            wallaxis2 = len(plant4.wallmatrix[0])
            wallaxis3 = len(plant4.wallmatrix[0][0])
        elif plant5.wallmatrix != 0:
            wallaxis1 = len(plant5.wallmatrix)  # 145
            wallaxis2 = len(plant5.wallmatrix[0])
            wallaxis3 = len(plant5.wallmatrix[0][0])
        elif plant6.wallmatrix != 0:
            wallaxis1 = len(plant6.wallmatrix)  # 145
            wallaxis2 = len(plant6.wallmatrix[0])
            wallaxis3 = len(plant6.wallmatrix[0][0])
        elif plant7.wallmatrix != 0:
            wallaxis1 = len(plant7.wallmatrix)  # 145
            wallaxis2 = len(plant7.wallmatrix[0])
            wallaxis3 = len(plant7.wallmatrix[0][0])
        elif plant8.wallmatrix != 0:
            wallaxis1 = len(plant8.wallmatrix)  # 145
            wallaxis2 = len(plant8.wallmatrix[0])
            wallaxis3 = len(plant8.wallmatrix[0][0])

        # Create a new matrix with the same size as non-zero wallmatrices and fill it up with NaNs:
        emptymatrix = np.empty([wallaxis1, wallaxis2, wallaxis3])
        nanmatrix = np.full_like(emptymatrix, np.nan)

        # Zero wallmatrices are replaced by the NaN matrix:
        if plant1.wallmatrix == 0:
            plant1.wallmatrix = nanmatrix
        if plant2.wallmatrix == 0:
            plant2.wallmatrix = nanmatrix
        if plant3.wallmatrix == 0:
            plant3.wallmatrix = nanmatrix
        if plant4.wallmatrix == 0:
            plant4.wallmatrix = nanmatrix
        if plant5.wallmatrix == 0:
            plant5.wallmatrix = nanmatrix
        if plant6.wallmatrix == 0:
            plant6.wallmatrix = nanmatrix
        if plant7.wallmatrix == 0:
            plant7.wallmatrix = nanmatrix
        if plant8.wallmatrix == 0:
            plant8.wallmatrix = nanmatrix

        # At this stage we still have a list of matrices with 145 elements
        # First the matrix list of different species is to be combined (to "minmatrix")
        # At each voxel, the MINIMUM of irradiance is considered for each skypatch (NaN values are ignored)
        # Source: https://docs.scipy.org/doc/numpy/reference/generated/numpy.fmin.html#numpy.fmin
        minmatrix = np.fmin.reduce([plant1.wallmatrix, plant2.wallmatrix, plant3.wallmatrix, plant4.wallmatrix,
                                plant5.wallmatrix, plant6.wallmatrix, plant7.wallmatrix, plant8.wallmatrix])

    print 'minmatrix', len(minmatrix)
    print 'minmatrix', len(minmatrix[0])
    print 'minmatrix', len(minmatrix[0][1])

    # After combining irradianc values per skypatches, they can be accumulated.
    # Unlike the original code, in this case Energyyearwall is not copied per runs of a for loop (145*)
        # Energyyearwall = Energyyearwall + np.copy(wallmatrix)

    # but a list with 145 elements is summed up
    Energyyearwall = minmatrix.sum(axis=0)

    # Including radiation from ground on walls as well as removing pixels higher than walls
    print np.copy(Energyyearwall).shape
    wallmatrixbol = (Energyyearwall > 0).astype(float)
    Energyyearwall = (Energyyearwall + (np.sum(radmatR[:, 2]) * albedo)/2) * wallmatrixbol
    Energyyearwall /= 1000
    Energyyearwall = np.transpose(np.vstack((wallrow + 1, wallcol + 1, np.transpose(Energyyearwall))))    # adding 1 to wallrow and wallcol so that the tests pass

    # Save the result
    filenamewall = outfolder + '/' + str(line[0]) + '-' + str(line[1]) + '-' + str(line[2]) + '.txt'
    header = '%row col irradiance'
    numformat = '%4d %4d ' + '%6.2f ' * (Energyyearwall.shape[1] - 2)
    np.savetxt(filenamewall, Energyyearwall, fmt=numformat, header=header, comments='')
