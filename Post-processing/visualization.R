#Import libraries
library(raster)
library(rgdal)
library(dplyr)
library(rasterVis)

#Read tables
temp <- list.files(pattern="*.txt", full.names = TRUE)
temp
structuredTables <- lapply(temp, function(x){
  DF <- read.table(x, header = FALSE, skip = "1", col.names = paste0("v",seq_len(12)))
  colnames(DF) <- c("row", "col", paste0("m",seq_len(10)))
  #Filter southern wall
  DF <- dplyr::filter(DF, row==21 & (col >= 11 & col <=20 ))
  #Rotate tables counter-clockwise: this way irradiance values increase vertically (bottom to top)
  foo <- apply(t(DF),2,rev)
  mymatrix <- foo[1:10,]
  #Create tifs
  myraster <- raster(mymatrix, xmn=0, xmx=10, ymn=0, ymx=10)
  return(myraster)
  })

#Write rasters with automatic naming
rasterNames <- setNames(structuredTables, c(
  'B09h','B10h','B11h','B12h','B13h','B14h','B15h','B16h','B17h','B18h','B19h',
  'P09h','P10h','P11h','P12h','P13h','P14h','P15h','P16h','P17h','P18h','P19h',
  'QF09h','QF10h','QF11h','QF12h','QF13h','QF14h','QF15h','QF16h','QF17h','QF18h','QF19h',
  'X09h','X10h','X11h','X12h','X13h','X14h','X15h','X16h','X17h','X18h','X19h'))
rasterNames
mapply(writeRaster, rasterNames, names(rasterNames), 'GTiff', overwrite = TRUE)


#Plot raster time series

#Stack tifs
myraster_all_files <- list.files(full.names = TRUE, pattern = ".tif$")
myraster_all_files
myraster_stack <- stack(myraster_all_files)

crs(myraster_stack)
extent(myraster_stack)
yres(myraster_stack)
xres(myraster_stack)
names(myraster_stack)

#Common plot
cols <- colorRampPalette(rev(brewer.pal(11,"RdBu")))
rasterNames <- paste0(" ",seq_len(44))
levelplot(myraster_stack,
          #main = "Irradiance values on the southern wall",
          legend=list(top=list(fun=grid::textGrob("kWh /"~m^{2}, y=0.25, x=1.015))),
          col.regions = cols,
          names.attr=rasterNames,
          layout = c(11,4),
          xlab = c("9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"),
          ylab = c("No vegetation", "Fraxinus", "Pinus", "Betula"),
          scales = list(draw=FALSE))      #removes scales (i.e. width and height)
