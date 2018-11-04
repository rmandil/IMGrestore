#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 19:19:55 2018

@author: verdu
"""

from numpy import abs, fft
from scipy.misc import imread
from matplotlib.pyplot import figure,imshow,savefig,nipy_spectral
import argparse 
from random import randint

parser = argparse.ArgumentParser(description='convolve images')
parser.add_argument('start', help='first image number, ex. 000100')
parser.add_argument('end', help='last image number, ex. 010000')
args = parser.parse_args()

start = int(args.start)
end = int(args.end) + 1
leng = len(args.start)

nipy_spectral()

def makePSF(length,width,theta,array):
    """ Returns a linear point spread function 
    INPUT: length of x and y blurs, blurry image (to copy shape of array)
    OUTPUT: array of same size as input that defines PSF """   
    # initialize gaussian array of same size as input array
    psf = np.zeros(np.shape(array))
    rows = len(psf[0]) # store dimensions
    cols = len(psf)
    
    psf[cols//2-width//2:cols//2+width//2,rows//2:rows//2+length] = 1. # make linear psf
    psf = img.rotate(psf, theta, reshape=False) # rotate by theta
   
    # transform to corners because of the weird fft indexing
    topleft = np.copy(psf[0:cols//2,0:rows//2])
    topright = np.copy(psf[0:cols//2,rows//2:rows])
    bottleft = np.copy(psf[cols//2:cols,0:rows//2])
    bottright = np.copy(psf[cols//2:cols,rows//2:rows])
    
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

images = [imread('{0}.jpg'.format(str('{0}'.format('%0{0}d'.format(leng) % (i,))), mode='L') for i in range(start,end))]
for image in images:
    num = 0
    # save original image
    figure()
    imshow(image)
    savefig('im{0}_original'.format(num))
    for i in range(10):
        # randum number generate for length width and theta
        length = randint(1,200)
        width = randint(1,100)
        theta = randint(0,359)
        # convolve image
        psf = makePSF(a,b,image)
        convolved = convolve(image,psf)
        figure()
        imshow(convolved)
        savefig('im{0}_{1}_{2}_{3}'.format(num,length,width,theta))
    num += 1
    
print(' All Done! ')
