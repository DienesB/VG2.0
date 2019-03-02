# VG2.0
Introducing leaf phenology induced variability of solar irradiance to numerical modeling.
Please note: the uploaded files are examples and serve demonstrational purposes only. Final codes are going to be publicly available in May 2019.

Input: dwd_weather_spring.txt, dwd_phenology_phase4.txt (dwd_phenology_phase31.txt, dwd_phenology_phase32.txt)
1. leaf_spread.R:             identification of 3 leaf phenology stages (phase4, phase31, phase32).
2. futher literature review:  identification of remaining leaf phenology stages.
Product: lookup_table.txt
3. leaf_density.R:            calculation of transmissivity of solar radiation through the crown of a user-defined genus on a user-defined day of year.
Product: transmissivity value
