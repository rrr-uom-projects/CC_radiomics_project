#
# script subtract the GTV from the dilated volume to form a new mask
# the new mask is confind to the CTV-IR
#

import numpy as np
from scipy.ndimage.morphology import (generate_binary_structure, binary_erosion, binary_dilation)
import SimpleITK as sitk 


def subtand(imgName, gtvMaskName, dilMaskName, ctvMaskName, difMaskName):
    img = sitk.ReadImage(imgName)
    ctvMsk = sitk.ReadImage(ctvMaskName)
    dilMsk = sitk.ReadImage(dilMaskName)
    gtvMsk = sitk.ReadImage(gtvMaskName)

    #Ensure new mask origin, spacing and direction is equal to that of the image for radiomics analysis.
    origin = img.GetOrigin()
    spacing = img.GetSpacing()
    direction = img.GetDirection()
    print(origin, spacing, direction)

    gtvMsk.SetOrigin(origin)
    gtvMsk.SetSpacing(spacing)
    gtvMsk.SetDirection(direction)
    sitk.WriteImage(gtvMsk, gtvMaskName, True)

    dilMsk.SetOrigin(origin)
    dilMsk.SetSpacing(spacing)
    dilMsk.SetDirection(direction)
    sitk.WriteImage(dilMsk, dilMaskName, True)

    ctvMsk.SetOrigin(origin)
    ctvMsk.SetSpacing(spacing)
    ctvMsk.SetDirection(direction)
    sitk.WriteImage(ctvMsk, ctvMaskName, True)

    # resample images to the same shape
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(img)
    res_ctv = resampler.Execute(ctvMsk)
    res_gtv = resampler.Execute(gtvMsk)
    res_dil = resampler.Execute(dilMsk)

    imga = sitk.GetArrayFromImage(img)
    ctvMska = sitk.GetArrayFromImage(res_ctv)
    dilMska = sitk.GetArrayFromImage(res_dil)
    gtvMska = sitk.GetArrayFromImage(res_gtv)
    
    diffmask = []
    # some masks have different number of slices that gives an error
    if imga.shape[0] != ctvMska.shape[0]:
        print('errorimg')
        return    
    if imga.shape[0] != dilMska.shape[0]:
        print('errorimg')
        return
    if imga.shape[0] != gtvMska.shape[0]:
        print('errorgtv')
        return
    
    for i in range(dilMska.shape[0]):
        # subtract masks
        diffmask.append((ctvMska[i] & dilMska[i]) - gtvMska[i])

    sitk.WriteImage(sitk.GetImageFromArray(diffmask), "%s" % difMaskName, True)
    
    diffMsk = sitk.ReadImage(difMaskName)
    diffMsk.SetOrigin(origin)
    diffMsk.SetSpacing(spacing)
    diffMsk.SetDirection(direction)
    sitk.WriteImage(diffMsk, difMaskName, True)
    diffMska = sitk.GetArrayFromImage(diffMsk)

    print(imgName, imga.shape, dilMska.shape, gtvMska.shape, ctvMska.shape, diffMska.shape)



def main():
    subtand(path_to image_file,
			path_to_gtv_file,
			path_to_dilated_gtv_file,
			path_to_CTV-IR_file,
			path_to_resulting_mask_after_GTV_is_subtracted_from_the_dilated_mask)

if __name__ == '__main__':
    main()

