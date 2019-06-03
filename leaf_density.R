#Author: Balazs Dienes
#Contact: dienes.balazs88@gmail.com

#This code defines the transmissivity of solar radiation through the crown of urban trees.
#The calculation is based on a linear model, calculating values between known dates of entering leaf phenological phases.

#Please note:
#The applied leaf phenology table is based on:
#1.) the leaf phenology database of the Deutscher Wetterdienst. Follow the link below for details:
#https://www.dwd.de/DE/klimaumwelt/klimaueberwachung/phaenologie/daten_deutschland/daten_deutschland_node.html
#2.) various academic research papers e.g. Tigges et al.(2013), Polgar and Primack (2011), and Halverson et al. (1986).
#Transmissivity values are based on the ground measurement of Konarska et al. (2013) and Canton et al. (1993).

#Read table:
Jultag2 <- read.table("lookup_table.txt", na.strings = NA, header = TRUE, row.names = 1)
Jultag2

#Define DOY, e.g 150
Jultag <- 150
Jultag

#Define genus, e.g. Tilia
Genus <- "Tilia"
Genus

if (Genus == "Acer") {
  Column <- 2
} else if (Genus == "Aesculus") {
  Column <- 3
} else if (Genus == "Betula") {
  Column <- 4
} else if (Genus == "Fraxinus") {
  Column <- 5
} else if (Genus == "Platanus") {
  Column <- 6
} else if (Genus == "Quercus") {
  Column <- 7
} else if (Genus == "Tilia") {
  Column <- 8
} else {
  print("ERROR: Invalid Genus")
}
print(Column)


#Indentifying leaf density of the user-defined genus on the user-defined DOY is a pre-condition of calculating transmissivity.
#Leaf density can be calculated by using the equation of a line.
#There is a total of 12 segments in the transmissivity curve. Each segment has a specific slope and length for each genus.

#1. Identification of breakpoints for the linear equation:
#1.1 Select column corresponding to the examined genus
BreakpointVector <- Jultag2[,Column]
BreakpointVector

#1.2 Define breakpoints
if (Jultag %in% BreakpointVector) {
  Breakpoint1 = Jultag
  Breakpoint2 = Jultag
} else {
  Breakpoint1 <- max(BreakpointVector[BreakpointVector < Jultag])
  Breakpoint2 <- min(BreakpointVector[BreakpointVector > Jultag])
}

#2. Equation of the line defined by the two breakpoints:
#2.1 Select corresponding values from the column representing leaf density:
RecordOfBreakpoint1 <- which(BreakpointVector == Breakpoint1)
RecordOfBreakpoint2 <- which(BreakpointVector == Breakpoint2)
YAxisBreakpoint1 <- Jultag2[RecordOfBreakpoint1,1]
YAxisBreakpoint2 <- Jultag2[RecordOfBreakpoint2,1]
YAxisBreakpoint1
YAxisBreakpoint2

#2.2 For the linear model, a vector for the "X" values and a vector for the "Y" values are necessary
XAxisVector <- c(Breakpoint1, Breakpoint2)
YAxisVector <- c(YAxisBreakpoint1, YAxisBreakpoint2)

#2.3 Linear model:
LinearModel <- lm(YAxisVector~XAxisVector)

#2.4 Extracting slope and intersect values:
summary(LinearModel)
Slope <- summary(LinearModel)$coefficients[2,1]
Intersection <- summary(LinearModel)$coefficients[1,1]
Slope
Intersection

#3. Calculate transmissivity:
#3.1 Indentify leaf density (y = ax + b)
LeafDensity = Slope * Jultag + Intersection
LeafDensity

#3.2 Transmissivity of the user-defined genus on the user-defined DOY
#Min and max transmissivity of the user-defined genus
TransmissivityMinimum = Jultag2[11,Column]
TransmissivityMaximum = Jultag2[12,Column]
#Leaf density and transmissivity are inversely proportional
Transmissivity = TransmissivityMaximum - ((LeafDensity/100)*(TransmissivityMaximum - TransmissivityMinimum))
Transmissivity #% of direct shortwave solar radiation is transmitted through the crown of the selected genus on the selected day
