
import matplotlib.pyplot as plt
import os
import numpy as np

def myrename(path):
    file_list=os.listdir(path)
    i=0
    for fi in file_list:
        old_name=os.path.join(path,fi)
        new_name=os.path.join(path,fi[0:4]+".dcm")
        os.rename(old_name,new_name)
        i+=1
        # #读取pydicom
        # import pydicom
        # import matplotlib.pyplot as plt
        # #读取单张dicom文件
        # df_origin = pydicom.dcmread(new_name)
        # df_label = pydicom.dcmread(new_name)
        # plt.figure(figsize=(12, 6))
        # #获取图像部分
        # img_origin = df_origin.pixel_array
        # img_label = df_label.pixel_array
        # plt.subplot(121),plt.imshow(img_origin,'gray'), plt.title('origin')
        # plt.subplot(122),plt.imshow(img_label,'gray'),plt.title('label')
        # plt.show()
 
if __name__=="__main__":
    path = "./data/image/"
    pathlist = os.listdir(path)
    for i in pathlist:
        print(path+i+"/")
        myrename(path+i+"/")
