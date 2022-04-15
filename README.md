# CC_radiomics_project

DATA SET-UP
------------------------
- batch_radiomics.py - script to extract radiomic features
- GTVdilate.py - script to dilate GTV while keeping it within the confines of the CTV-IR
- compute_peritumoral.py - script to compute the peritumoral region from the dilated GTV and the GTV

CORRELATIONS TO VOLUME
------------------------
- drop_volume.py - script to drop radiomic features highly correlated to volume

csv files showing all features and their correlation to original_shape_MeshVolume

- GTV_T2W.csv - T2W images and their respective GTV contours data-set
- Peritumoral_T2W.csv - T2W images and their respective peritumoral region contours data-set
- GTV_Dixon.csv - Dixon images and their respective GTV contours data-set
- Peritumoral_Dixon.csv - Dixon images and their respective peritumoral region contours data-set

ICC(1,1)
------------------------
- ICC_script.R - script to find the ICC values of radiomic features from images acquired at the start and end of a visit

csv files showing all reamining features and their corresponding ICC(1,1) and their repeatability based on the criteria:

def label_repeatability (row):
    if (row['ICC_value'] >= 0.9):
        return 'Excellent'
    if (0.75 <= row['ICC_value'] < 0.9):
        return 'Good'
    if (row['ICC_value'] < 0.75):
        return 'Poor'

- GTV_T2W.csv - T2W images and their respective GTV contours data-set
- Peritumoral_T2W.csv - T2W images and their respective peritumoral region contours data-set
- GTV_Dixon.csv - Dixon images and their respective GTV contours data-set
- Peritumoral_Dixon.csv - Dixon images and their respective peritumoral region contours data-set
