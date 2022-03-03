#
# script erodes gtv to form a new mask
#

import numpy as np
from scipy.ndimage.morphology import (generate_binary_structure, binary_erosion, binary_dilation)
import SimpleITK as sitk 


def erodilate(imageFile, GTVmaskFile, dilatedGTVmaskFile):
    image = sitk.ReadImage(imageName)
    orMaski = sitk.ReadImage(maskName)
    
    #Ensure new mask origin, spacing and direction is equal to that of the image for radiomics analysis.
    origin = image.GetOrigin()
    spacing = image.GetSpacing()
    direction = image.GetDirection()
    print(origin, spacing, direction)

    orMaski.SetOrigin(origin)
    orMaski.SetSpacing(spacing)
    orMaski.SetDirection(direction)
    
    # resample images to the same shape
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(image)
    orMask = resampler.Execute(orMaski)
    
    newMaskArray = sitk.GetArrayFromImage(orMask)
    dilateMaskArray = newMaskArray.copy()
    dilateMaskArray == 1
    
    structExample = generate_binary_structure(3, 3)
    dilateMaskArray = binary_dilation(dilateMaskArray, structExample, iterations = 10) #edit number of iterations to make sure all gaps in mask are being filled
    dilMaskArray = binary_erosion(dilateMaskArray, structExample, iterations = 8)
    newMaskArray[:,:,:] = 0
    newMaskArray[np.where(dilMaskArray == True)] = 1
    dilatedMask = sitk.GetImageFromArray(newMaskArray)
    print("dilated mask created.")
    
    dilatedMask.SetOrigin(origin)
    dilatedMask.SetSpacing(spacing)
    dilatedMask.SetDirection(direction)
    
    sitk.WriteImage(dilatedMask, "%s" % dilMaskName, True)


def main():
    erodilate(path_to_image_file,
            path_to_gtv_file,
            path_to_created_dilated_mask_file )

if __name__ == '__main__':
    main()
