import nibabel as nib
import numpy as np
import os
import cv2
import pydicom
from PIL import Image
import sys
import imageio

def InitDicomFile():
    infometa = pydicom.dataset.Dataset()
    infometa.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    infometa.ImplementationVersionName = 'Python ' + sys.version
    infometa.MediaStorageSOPClassUID = 'CT Image Storage'
    infometa.FileMetaInformationVersion = b'\x00\x01'
    return infometa

def usin2(imagesPath,niipath):
    imgPathList = os.listdir(imagesPath)
    niiPathList = os.listdir(niipath)
    for PathIndex in range(len(imgPathList)):
        imgPathFile = imagesPath+imgPathList[PathIndex]
        nii_file2 = niipath+imgPathList[PathIndex]+".nii.gz"
        img2 = nib.load(nii_file2).get_fdata()
        print(type(img2))
        w,h,c = img2.shape
        imglist = os.listdir(imgPathFile)
        np.sort(imglist)
        imglist = np.sort(imglist)
        for i in range(0,c):
            if (i==0):
                mask = img2[:,:,0:i+1]
            else:
                mask = img2[:,:,i-1:i]

            #单通道转３通道
            imgData = np.dstack((mask,mask,mask))
            print(imgData.shape)
            color = [[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255],[255,160,0],[100,0,200]]
            for nums in range(8):
                indexD =np.array(np.where(mask==nums+1))
                # print(indexD.shape[1])
                for i in range(indexD.shape[1]):
                    changeIndex = indexD[:,i]
                    imgData[changeIndex[0],changeIndex[1],0] = color[nums][0]
                    imgData[changeIndex[0],changeIndex[1],1] = color[nums][1]
                    imgData[changeIndex[0],changeIndex[1],2] = color[nums][2]
            # print(imgData)
            mask = imgData
            cX= int(w/2)
            cY=int(h/2)
            print("cX, cY is",cX, cY )
            M = cv2.getRotationMatrix2D((cX, cY), -90, 1.0)
            mask = cv2.warpAffine(mask, M, (w, h))

            saveMaskPath = "./data/image"+str(imgPathList[PathIndex])+"/"
            savePngPath = "./data/label"+str(imgPathList[PathIndex])+"/"
            print(saveMaskPath)
            print(savePngPath)
            if not os.path.exists(saveMaskPath):  
                os.mkdir(saveMaskPath)
            if not os.path.exists(savePngPath):  
                os.mkdir(savePngPath)
            print("read dcm path is",imgPathFile+"/"+imglist[i])
            filename = imgPathFile+"/"+imglist[i]
            name = str(i)
            name=filename[:-4]
            ds = pydicom.read_file("%s" % (filename))
            img = ds.pixel_array
            imageio.imwrite(savePngPath+"/image_"+str(i)+".jpg", img)
            cv2.imwrite(saveMaskPath+"/mask_"+str(i)+".png",mask)


imagesPath = "./data/image"
niipath = "./data/label"
usin2(imagesPath,niipath)    
