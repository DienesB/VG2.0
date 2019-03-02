#Author: Balazs Dienes
#Contact: dienes.balazs88@gmail.com

#Processing DWD leaf phenology data to establish a lookup table for calculating transmissivity (see "lookup_table.txt").
#Leaf phenology phase 4: start of leaf spread.

#Please note: this code serves demonstrative purposes only.

#Read table
AllGenus <- read.table("dwd_phenology_phase4.txt", sep = "\t", na.strings = "NA")
sort(unique(AllGenus$Lat_name), decreasing = FALSE)

#Descriptive statistics
DescriptiveStats <- cbind(
  tapply(AllGenus$Jultag, AllGenus$Lat_name, length),
  tapply(AllGenus$Jultag, AllGenus$Lat_name, mean),
  tapply(AllGenus$Jultag, AllGenus$Lat_name, sd),
  tapply(AllGenus$Jultag, AllGenus$Lat_name, median))
colnames(DescriptiveStats) <-  c("Number of elements","Mean", "Standard Deviation", "Median")
DescriptiveStats <- t(DescriptiveStats)
write.table(DescriptiveStats, "descriptive_stats_phase4.txt", sep = "\t")

###1. ANOVA###
#Is there a statistically significant difference between tree genera considering the start of leaf spread?

#ANOVA requirement1: Normal distribution
hist(AllGenus$Jultag, main = "Histrogram of unfolding leaves", xlab = "Leaves unfold start")
shapiro.test(AllGenus$Jultag) #p-value = 0.236: normally distributed

#ANOVA requirement 2: Variance homogeneity
install.packages("car")
library(car)
leveneTest(AllGenus$Jultag,AllGenus$Lat_name) #0.9172: homogene

#ANOVA
AnovaAllGenus <- aov(AllGenus$Jultag~AllGenus$Lat_name)
summary(AnovaAllGenus) #<2e-16
AnovaAllGenus2 <- lm(AllGenus$Jultag~AllGenus$Lat_name)
anova(AnovaAllGenus2) #<2.2e-16: yes, there is a statictically significant difference

#Post-Hoc-Test
TukeyHSD(AnovaAllGenus)
boxplot(AllGenus$Jultag~AllGenus$Lat_name)

#Letter codes
install.packages("agricolae")
library(agricolae)
LetterCode <-HSD.test(AnovaAllGenus, "AllGenus$Lat_name", group=TRUE)
LetterCode

#AllGenus$Jultag groups
#Quercus         117.3084      a
#Tilia           116.8182      a
#Fraxinus        115.7746      a
#Aesculus        105.6228      b
#Betula          102.6250      b

#Median start of leaf spread of early leafing genera (i.e. Aesculus and Betula)
median(AllGenus$Jultag[AllGenus$Lat_name=="Aesculus" | AllGenus$Lat_name=="Betula"])
#Day oy year: 105

#Median start of leaf spread of late leafing genera (i.e. Fraxinus, Quercus, and Tilia)
median(AllGenus$Jultag[AllGenus$Lat_name=="Fraxinus" | AllGenus$Lat_name=="Quercus" | AllGenus$Lat_name=="Tilia"])
#Day of year: 117

###2. Climate scenarios###
#Read table
weatherSpring <- read.table("dwd_weather_spring.txt", sep = "\t", na.strings = "NA", header = TRUE)

#Establishing cold and warm spring scenarions by class intervals function
install.packages("classInt")
library(classInt)
classIntervals(weatherSpring$meanT, 2, style = "kmeans")
#group1: 7.136667 to 9.537778; no. of elements:20
#group2: 9.537778 to 11.88444; no. of elements: 21
plot(classIntervals(weatherSpring$meanT, 2, style = "kmeans"), pal=c("wheat1", "red3"))
#Threshold: ~9.53 degrees Celsius

#List of T values below 9.53
cold <- weatherSpring$meanT[weatherSpring$meanT < 9.53]
min(cold)
max(cold)
length(cold)

#List of T values above 9.53
warm <- weatherSpring$meanT[weatherSpring$meanT > 9.53]
warm
min(warm)
max(warm)
length(warm)

###3. Correlation between temperature and start of leaf spread
#Merge T and phenology data
GenusWeatherMerge <- merge(AllGenus, weatherSpring, by = "Referenzjahr", all.x = TRUE)

#Test correlation 1:
plot(GenusWeatherMerge$meanT,GenusWeatherMerge$Jultag, xlab = "Spring mean temperature (°C)", ylab = "DOY", main = "Correlation between DOY and temperature: - 0.41")
cor(GenusWeatherMerge$meanT,GenusWeatherMerge$Jultag) #-0.4110097
abline(v = 9.53, col="red")
text(10, 142, "k-means: 9.53°C", col = "red") 

#Test correlation 2:
#On the previous plot, multiple Jultag values were presented for each year.
#To avoid this, I calculate the mean Jultag value for each temperature value.
TemperatureJultagMean <- aggregate(GenusWeatherMerge$Jultag, list(GenusWeatherMerge$meanT), mean)
TemperatureJultagMean
#Jultag tends to decrease as the temperature increases
plot(TemperatureJultagMean$Group.1,TemperatureJultagMean$x, main = "Correlation between mean DOY and temperature: - 0.73", xlab = "Spring mean temperature (°C)", ylab = "DOY")
abline(h=mean(GenusWeatherMerge$Jultag))
abline(v = 9.53, col="red")
text(10, 122, "k-means: 9.53", col = "red") 
cor(TemperatureJultagMean$Group.1,TemperatureJultagMean$x) #-0.7254343

#Create subsets based on spring temperature
GenusWeatherMerge0205Warm <- GenusWeatherMerge[GenusWeatherMerge$meanT > 9.53,]
GenusWeatherMerge0205Cold <- GenusWeatherMerge[GenusWeatherMerge$meanT < 9.53,]
max(GenusWeatherMerge0205Cold$meanT) #9.51: good, it is below the threshold
mean(GenusWeatherMerge0205Cold$meanT) #8.71
min(GenusWeatherMerge0205Warm$meanT) #9.64: good, it is over the threshold
mean(GenusWeatherMerge0205Warm$meanT) #10.53


###ANOVA for cold and for warm springs###
#Is there a difference between colder and warmer springs regarding start of leaf spread?

###ANOVa for cold springs###

#ANOVA requirement1: Normal distribution
hist(GenusWeatherMerge0205Cold$Jultag, main = "Histrogram of unfolding leaves in cold springs", xlab = "Leaves unfold start")
shapiro.test(GenusWeatherMerge0205Cold$Jultag) #p-value = 0.3164: normally distributed

#ANOVA requirement 2: Variance homogeneity
install.packages("car")
library(car)
leveneTest(GenusWeatherMerge0205Cold$Jultag,GenusWeatherMerge0205Cold$Lat_name) #0.5476: homogene

#ANOVA
AnovaAllGenusCold <- aov(GenusWeatherMerge0205Cold$Jultag~GenusWeatherMerge0205Cold$Lat_name)
summary(AnovaAllGenusCold) #1.48e-12
AnovaAllGenusCold2 <- lm(GenusWeatherMerge0205Cold$Jultag~GenusWeatherMerge0205Cold$Lat_name)
anova(AnovaAllGenusCold2) #1.484e-12

#Post-Hoc-Test
TukeyHSD(AnovaAllGenusCold)
boxplot(GenusWeatherMerge0205Cold$Jultag~GenusWeatherMerge0205Cold$Lat_name, ylab = "DOY", xlab = "Genera", main = "DOY of leaf spread on cold springs")

#Letter codes
install.packages("agricolae")
library(agricolae)
LetterCode <-HSD.test(AnovaAllGenusCold, "GenusWeatherMerge0205Cold$Lat_name", group=TRUE)
LetterCode

#GenusWeatherMerge0205Cold$Jultag groups
#Quercus   123.6667      a
#Tilia     122.1429      a
#Fraxinus  117.9565      a
#Aesculus  111.3617      b
#Betula    108.8750      b

#Median start of leaf spread of early leafing genera on cold springs (i.e. Aesculus and Betula)
median(GenusWeatherMerge0205Cold$Jultag[GenusWeatherMerge0205Cold$Lat_name=="Aesculus" | GenusWeatherMerge0205Cold$Lat_name=="Betula"])
#Day of year: 111

#Median start of leaf spread of late leafing genera on cold springs (i.e. Fraxinus, Quercus, and Tilia)
median(GenusWeatherMerge0205Cold$Jultag[GenusWeatherMerge0205Cold$Lat_name=="Fraxinus" | GenusWeatherMerge0205Cold$Lat_name=="Quercus" | GenusWeatherMerge0205Cold$Lat_name=="Tilia"])
#Day of year: 122

###ANOVA for warm springs###

#ANOVA requirement1: Normal distribution
hist(GenusWeatherMerge0205Warm$Jultag, main = "Histrogram of unfolding leaves in cold springs", xlab = "Leaves unfold start")
shapiro.test(GenusWeatherMerge0205Warm$Jultag) #p-value = 0.2644: normally distributed

#ANOVA requirement 2: Variance homogeneity
install.packages("car")
library(car)
leveneTest(GenusWeatherMerge0205Warm$Jultag,GenusWeatherMerge0205Warm$Lat_name) #0.5999: homogene

#ANOVA
AnovaAllGenusWarm <- aov(GenusWeatherMerge0205Warm$Jultag~GenusWeatherMerge0205Warm$Lat_name)
summary(AnovaAllGenusWarm) #<2e-16
AnovaAllGenusWarm2 <- lm(GenusWeatherMerge0205Warm$Jultag~GenusWeatherMerge0205Warm$Lat_name)
anova(AnovaAllGenusWarm2) #<2.2e-16

#Post-Hoc-Test
TukeyHSD(AnovaAllGenusWarm)
boxplot(GenusWeatherMerge0205Warm$Jultag~GenusWeatherMerge0205Warm$Lat_name, ylab = "DOY", xlab = "Genera", main = "DOY of leaf spread on warm springs")

#Letter codes
install.packages("agricolae")
library(agricolae)
LetterCode <-HSD.test(AnovaAllGenusWarm, "GenusWeatherMerge0205Warm$Lat_name", group=TRUE)
LetterCode

#GenusWeatherMerge0205Warm$Jultag groups
#Fraxinus                         114.7292      a
#Quercus                          112.6935      a
#Tilia                            107.5000     ab
#Aesculus                         101.5970      b
#Betula                            99.5000      b

#Median start of leaf spread of early leafing genera on warm springs(i.e. Aesculus and Betula)
median(GenusWeatherMerge0205Warm$Jultag[GenusWeatherMerge0205Warm$Lat_name=="Aesculus" | GenusWeatherMerge0205Warm$Lat_name=="Betula"])
#Day of year: 101

#Median start of leaf spread of medium leafing genera on warm springs (i.e Tilia)
median(GenusWeatherMerge0205Warm$Jultag[GenusWeatherMerge0205Warm$Lat_name=="Tilia"])
#Day of year: 107.5

#Median start of leaf spread of late leafing genera on warm springs (i.e Fraxinus and Quercus)
median(GenusWeatherMerge0205Warm$Jultag[GenusWeatherMerge0205Warm$Lat_name=="Fraxinus" | GenusWeatherMerge0205Warm$Lat_name=="Quercus"])
#Day of year: 115
