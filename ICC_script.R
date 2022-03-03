library(dplyr)
library(irr)
library(ggplot2)
library(tidyverse)

# data set-up
# columns in "dx" have features with suffix "start" or "end" based on the images they were extracted from
dx <- data.frame(read.csv(path_to_csv_file_with_features_from_images_acquired_at_the_start_and_end_of_a_visit))

# lists of feature names
# columns in "f_list" have features without the suffix for comparison to be drawn from a list with the actual feature names 
f_list <- data.frame(read.csv(path_to_csv_file_with"C:\\Users\\mutho\\OneDrive\\Documents\\src\\sample_ds\\dx7b_vol_rem.csv"))

# remove columns with names not corresponding to feature names
dxfeatureList = c(names(f_list %>% select(!c(PatientID, visit, time))))

icc_val <- vector()
icc_val_lbound <- vector()
icc_val_ubound <- vector()
feature <- vector()
p_val <- vector()
# create empty dataframe and append 2 columns
y <- data.frame()
y$ICC_value <- 0
y$p_value <- 0

for (i in 1:length(dxfeatureList)) {
  dxfeatureList[i]
  df_temp <- dx %>% dplyr:: select(starts_with(paste(dxfeatureList[i],"_",sep="",collapse = NULL)))
  ICC <- icc(df_temp,model="oneway",type="agreement",unit="single",0,conf.level=0.95)
  icc_val[i] <- ICC
  icc_val_lbound[i] <- ICC$lbound
  icc_val_ubound[i] <- ICC$ubound
  p_val <- ICC['p.value']
  feature <- dxfeatureList[i]
  ICC_v <- abs(as.numeric(ICC['value']))
  print(ICC_v)
  y <- rbind.data.frame(y, feature)
  y$ICC_value[i] <- ICC_v
  y$p_value[i] <- p_val
}
colnames(y)
colnames(y)[1] <- "Features"
y <- apply(y,2,as.character)

# radiomic features and their respecitve ICC values
write.csv(y, path_to_csv_file_with_radiomic_features_and_their_respective_ICC_values", row.names = FALSE)
