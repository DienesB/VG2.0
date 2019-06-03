# Author: Balazs Dienes
# Contact: dienes.balazs88@gmail.com


# Considering the location of tree canopies for transmissivity value calculation

#Import libraries
from osgeo import gdal
import numpy as np

#Read wall raster as NumPy array
filepath = r"mainfolder/transmissivity_weighting_test/aspect.tif"
buildingRaster = gdal.Open(filepath)
buildingArray = np.array(buildingRaster.GetRasterBand(1).ReadAsArray())

#New NumPy array with the location (row, col) and value of wall pixels
wallArray = np.array([]).reshape(0,3)
for rowBuilding in range(0,len(buildingArray)):
    for colBuilding in range(0,len(buildingArray[0])):
        if buildingArray.item(rowBuilding, colBuilding) > 0.0:
            wallArray = np.append(wallArray, [[rowBuilding, colBuilding, buildingArray.item(rowBuilding, colBuilding)]], axis=0)
print 'row', '  col', ' value'
for i in range(len(wallArray)):
    print wallArray[i]

#Read vegetation raster as NumPy array
filepathVeg = r"mainfolder/transmissivity_weighting_test/tree_genus_test.tif"
vegetationRaster = gdal.Open(filepathVeg)
vegetationArray = np.array(vegetationRaster.GetRasterBand(1).ReadAsArray())

#New NumPy array with the location (row, col) and value of vegetation pixels
canopyArray = np.array([]).reshape(0,3)
for rowVeg in range(0,len(vegetationArray)):
    for colVeg in range(0,len(vegetationArray[0])):
        if vegetationArray.item(rowVeg, colVeg) != -128:
            canopyArray = np.append(canopyArray, [[rowVeg, colVeg, vegetationArray.item(rowVeg, colVeg)]], axis=0)
print 'row', '  col', ' value'
for j in range(len(canopyArray)):
    print canopyArray[j]

print 'number of items in wall array: ', len(wallArray)
print 'number of items in canopy array: ', len(canopyArray)

######################################################################################################################
###Identification of vegetation pixels that are located in eastern, southern, or western direction from wall pixels###
######################################################################################################################

#Set buffer in pixel size
buffer = 20

#Filter trees based on their location
morningArray = np.array([]).reshape(0,5)
noonArray = np.array([]).reshape(0,5)
eveningArray = np.array([]).reshape(0,5)
for xMorning in range(0,len(wallArray)):
    for yMorning in range(0,len(canopyArray)):
        if ((wallArray[xMorning][0] == canopyArray[yMorning][0]) and (wallArray[xMorning][1] < canopyArray[yMorning][1] <= (wallArray[xMorning][1] + buffer))):
            morningArray = np.append(morningArray, [[wallArray[xMorning][0], wallArray[xMorning][1], canopyArray[yMorning][0], canopyArray[yMorning][1], canopyArray[yMorning][2]]], axis=0)
        elif ((wallArray[xMorning][0] < canopyArray[yMorning][0] <= (wallArray[xMorning][0] + buffer)) and (wallArray[xMorning][1] == canopyArray[yMorning][1])):
            noonArray = np.append(noonArray, [[wallArray[xMorning][0], wallArray[xMorning][1], canopyArray[yMorning][0], canopyArray[yMorning][1], canopyArray[yMorning][2]]], axis=0)
        elif ((wallArray[xMorning][0] == canopyArray[yMorning][0]) and ((wallArray[xMorning][1] - buffer) <= canopyArray[yMorning][1] < wallArray[xMorning][1])):
            eveningArray = np.append(eveningArray, [[wallArray[xMorning][0], wallArray[xMorning][1], canopyArray[yMorning][0], canopyArray[yMorning][1], canopyArray[yMorning][2]]], axis=0)
print 'morning: ', len(morningArray), '\n', morningArray
print 'noon: ', len(noonArray), '\n', noonArray
print 'evening:', len(eveningArray), '\n', eveningArray

#Remove duplicate vegetation pixels from arrays
#Morning
morningVegetation = [tuple(row) for row in morningArray[:,2:5]]
uniqueMorningVegetation = np.unique(morningVegetation, axis=0)
print 'unique morning vegetation pixels:\n',uniqueMorningVegetation
#Noon
noonVegetation = [tuple(row) for row in noonArray[:,2:5]]
uniqueNoonVegetation = np.unique(noonVegetation, axis=0)
print 'unique noon vegetation pixels:\n',uniqueNoonVegetation
#Evening
eveningVegetation = [tuple(row) for row in eveningArray[:,2:5]]
uniqueEveningVegetation = np.unique(eveningVegetation, axis=0)
print 'unique evening vegetation pixels:\n',uniqueEveningVegetation

fullVegetation = np.concatenate((uniqueMorningVegetation[:,2],uniqueNoonVegetation[:,2],uniqueEveningVegetation[:,2]))
print 'morning + noon + evening vegetation pixels: ', fullVegetation

fullUniqueVegetation = np.unique(fullVegetation)
print'uniques morning + noon + evening vegetation pixels: ', fullUniqueVegetation
