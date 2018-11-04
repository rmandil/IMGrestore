#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 19:19:55 2018

@author: verdu
"""

from numpy import abs, fft, zeros,shape,copy,savetxt
from cv2 import imread
import glob
from matplotlib.pyplot import figure,imshow,nipy_spectral,close,tick_params
from random import randint
import scipy.ndimage as img

nipy_spectral()

def makePSF(length,width,theta,array):
    """ Returns a linear point spread function 
    INPUT: length of x and y blurs, blurry image (to copy shape of array)
    OUTPUT: array of same size as input that defines PSF """   
    # initialize gaussian array of same size as input array
    psf = zeros(shape(array))
    rows = len(psf[0]) # store dimensions
    cols = len(psf)
    
    psf[cols//2-width//2:cols//2+width//2,rows//2:rows//2+length] = 1. # make linear psf
    psf = img.rotate(psf, theta, reshape=False) # rotate by theta
   
    # transform to corners because of the weird fft indexing
    topleft = copy(psf[0:cols//2,0:rows//2])
    topright = copy(psf[0:cols//2,rows//2:rows])
    bottleft = copy(psf[cols//2:cols,0:rows//2])
    bottright = copy(psf[cols//2:cols,rows//2:rows])
    
    psf[0:cols//2,0:rows//2],psf[0:cols//2,rows//2:rows],psf[cols//2:cols,
            0:rows//2],psf[cols//2:cols,rows//2:rows] = bottright,bottleft,topright,topleft
    
    return psf

def convolve(image, psf):
    K = len(psf[0])
    L = len(psf)
    image_fft = fft.fft2(image) # fourier transform image
    psf_fft = fft.fft2(psf) # fourier transform point spread function 
    convolved_fft = image_fft*psf_fft*K*L
    convolved = abs(fft.ifft2(convolved_fft))
    return convolved # return deconvolved image

images= []
for filename in glob.glob('*.jpg'): #assuming jpg
    images.append(imread(filename,0))
    
num = 0    
for image in images:
    # save original image
    savetxt('im{0}_original.txt'.format(num),image)
    for i in range(1):
        # randum number generate for length width and theta
        length = randint(1,200)
        width = randint(1,100)
        theta = randint(0,359)
        # convolve image
        psf = makePSF(length,width,theta,image)
        convolved = convolve(image,psf)
        savetxt('im{0}_{1}_{2}_{3}.txt'.format(num,length,width,theta),convolved)
    num += 1
print(' All Done! ')
