# Author: Balazs Dienes
# Contact: dienes.balazs88@gmail.com

# Incorporating mean spring temperature for the calculation of leaf density and transmissivity.
# Three scenarios are possible: "warm spring", "cold spring", and "no spring temperature".

#Import libraries
import numpy as np

def scenario():

    print '\nscenario method is running...'

    # Read lookup table as a numpy array.
    # The lookup table was prepared as a result of literature review.
    # The lookup table contains the days on which tree genera frequent in Berlin enter new phenological phases.
    # The lookup table also includes the winter and summer transmissivity of tree genera frequent in Berlin.

    mainfolder = "C:/Users/Balazs Dienes/PycharmProjects/SEBEphen/mainfolder/"
    lookupfolder = mainfolder + 'input_phenology/'

    springScenarios = True
    springTemperature = 11.27  # threshold:9.53

    if (springScenarios == True):
        if (springTemperature >= 9.53):
            lookuptable = np.genfromtxt(lookupfolder + 'lookup_table_warm_scenario.txt', skip_header=1,
                                        usecols=(1, 2, 3, 4, 5, 6, 7, 8),
                                        delimiter="\t", missing_values="NA")
            print "Warm spring scenario is applied as the temperature is: ", springTemperature, "C.\n"
        else:
            lookuptable = np.genfromtxt(lookupfolder + 'lookup_table_cold_scenario.txt', skip_header=1,
                                        usecols=(1, 2, 3, 4, 5, 6, 7, 8),
                                        delimiter="\t", missing_values="NA")
            print "Cold spring scenario is applied as the temperature is: ", springTemperature, "C.\n"
    else:
        lookuptable = np.genfromtxt(lookupfolder + 'lookup_table_no_scenario.txt', skip_header=1,
                                    usecols=(1, 2, 3, 4, 5, 6, 7, 8),
                                    delimiter="\t", missing_values="NA")
        print "Spring temperature is unknown, no climate scenario is applied.\n"

    return lookuptable
