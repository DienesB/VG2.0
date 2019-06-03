# Author: Balazs Dienes
# Contact: dienes.balazs88@gmail.com

# This file calculates transmissivity of solar radiation through the canopy of urban trees.
# Genera included: Acer, Aesculus, Betula, Fraxinus, Platanus, Quercus, Tilia

# Import libraries:
import sys
import numpy as np

np.set_printoptions(threshold=sys.maxsize)
import Spring_scenarios as scenario

def transmissivity(Jultag, Genus):
  print '\ntransmissivity method is running...'
  print 'Jultag: ', Jultag
  lookuptable = scenario.scenario()
  print lookuptable

  # The Day of Year is already known, tree genera occuring in the AOI is also known from the passing arguments.

  # Leaf density of a certain Genus on a certain Jultag is a pre-condition to calculate transmissivity.
  # Leaf density can be calculated by using the Equation of a Line.
  # LeafDensity = Slope * Jultag + Intersection

  # There is a total of 12 segments in the transmissivity curve. Each segment has a specific slope and length for each genera.
  # To identify the endpoints of the segments to which the current Jultag refers (which in necessary for the linear equation),
  # First the column in which the examined tree genera is located must be defined:

  #ACER
  if Genus == 1:
    Column = 1
    print 'Acer - as passing argument - is on fire!'

  #BETULA
  elif Genus == 2:
    Column = 3
    print 'Betula - as passing argument - is on fire!'

  #FRAXINUS
  elif Genus == 3:
    Column = 4
    print 'Fraxinus - as passing argument - is on fire!'

  #PLATANUS
  elif Genus == 4:
    Column = 5
    print 'Platanus - as passing argument - is on fire!'

  #QUERCUS
  elif Genus == 5:
    Column = 6
    print 'Quercus - as passing argument - is on fire!'

  #TILIA
  elif Genus == 6:
    Column = 7
    print 'Tilia - as passing argument - is on fire!'

  #AESCULUS
  elif Genus == 7:
   Column = 2
   print 'Aesculus - as passing argument - is on fire!'

  else:
    print("Caution: Unknown Genus")
    # Other genera are handled as if they were Tilia
    Column = 7

  # Identify the used column in the numpy array:
  BreakpointVector = lookuptable[0:10,Column]

  # Define breakpoints:
  if Jultag in BreakpointVector:
    Breakpoint1 = Jultag
    Breakpoint2 = Jultag
  elif Jultag == 366:
    Breakpoint1 = 365
    Breakpoint2 = 365
  else:
    Breakpoint1 = max(BreakpointVector[BreakpointVector < Jultag])
    Breakpoint2 = min(BreakpointVector[BreakpointVector > Jultag])

  BreakpointVector
  Breakpoint1
  Breakpoint2

  # Equation of the line defined by the two endpoints:
  # An "X" vector (the x values of the two breakpoints) and a "Y" vector (the y values of the two breakpoints) are necessary for the linear model.

  # Location of rows (records) in which the "X" values (i.e. Breakpoint1 and Breakpoint2) are located:
  RecordOfBreakpoint1 = np.where(BreakpointVector == Breakpoint1)
  RecordOfBreakpoint2 = np.where(BreakpointVector == Breakpoint2)
  RecordOfBreakpoint1
  RecordOfBreakpoint2
  # "Y" values (YAxisBreakpoint1, YAxisBreakpoint2) that are located in the above indentified rows (records):
  YAxisBreakpoint1 = lookuptable[RecordOfBreakpoint1,0]
  YAxisBreakpoint2 = lookuptable[RecordOfBreakpoint2,0]
  YAxisBreakpoint1
  YAxisBreakpoint2

  # "X" vector:
  XAxisVector = np.array([Breakpoint1, Breakpoint2])
  XAxisVector

  # "Y" vector:
  YAxisVector = np.array([np.ndarray.item(YAxisBreakpoint1), np.ndarray.item(YAxisBreakpoint2)])
  YAxisVector

  # The linear model itself:
  from sklearn.linear_model import LinearRegression
  reg = LinearRegression()
  # scikit learn uses 2D arrays and thus XAXisVector must be reshaped to 1 column and as many records as its length (in my case: 2)
  reg = reg.fit(XAxisVector.reshape(len(XAxisVector), 1), YAxisVector)

  # Extract slope and intersect values:
  Slope = reg.coef_
  Intersection = reg.intercept_
  Slope
  Intersection

  # Define Leaf Density:
  LeafDensity = Slope * Jultag + Intersection
  LeafDensity

  # Identify the theoretical minimum and maximum transmissivity value of a certain tree genus:

  print 'Jultag: ', Jultag
  print 'Current genus: ', Genus
  TransmissivityMinimum = lookuptable[10,Column]
  TransmissivityMaximum = lookuptable[11,Column]
  print 'Minimum transmissivity of current genus: ', TransmissivityMinimum
  print 'Maximum transmissivity of current genus: ', TransmissivityMaximum

  # Transmissivity is inversely proportional to Leaf Density and thus:
  Transmissivity = TransmissivityMaximum - ((LeafDensity/100)*(TransmissivityMaximum - TransmissivityMinimum))
  print 'Current transmissivity of current genus: ', Transmissivity, '\n'

  return Transmissivity[0]/100
