from numpy import abs, fft, zeros,shape,copy,loadtxt
#from cv2 import imread
import glob
import matplotlib.pyplot as plt
import scipy.ndimage as img
import argparse 

parser = argparse.ArgumentParser(description='deconvolve images')
parser.add_argument('image', help='image number, ex. 0')
parser.add_argument('length', help='last image number, ex. 100')
parser.add_argument('width', help='last image number, ex. 20')
parser.add_argument('theta', help='last image number, ex. 50')                 
args = parser.parse_args()
                    
plt.nipy_spectral()

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


def deconvolve(Input, psf, epsilon):
  """ Returns the deconvolved (un-blurred) photograph""" 
  InputFFT = fft.fft2(Input) # fourier transform blurry image
  psfFFT = fft.fft2(psf)+epsilon # fourier transform point spread function
  deconvolved = abs(fft.ifft2(InputFFT/psfFFT)) # inverse fourier transform deconvolved image
  return deconvolved
                    
a=int(args.image)
b=int(args.length)
c=int(args.width)
d=int(args.theta)

convolved=loadtxt('im{0}_{1}_{2}_{3}.txt'.format(a,b,c,d))
image=loadtxt('im{0}_original.txt'.format(a))
psf = makePSF(b,c,d,convolved)
deconvolved = deconvolve(convolved,psf,0.001)

fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(1,3,1)

# Plot the deconvolved image
ax1.imshow(deconvolved)
ax1.set_title('Deconvolved Image')
ax1.set_ylabel('Y Pixels')
ax1.set_xlabel('X Pixels')

# Plot the convolved image
ax2 = fig.add_subplot(1,3,2)
ax2.imshow(convolved)
ax2.set_title('Convolved Image')
ax2.set_xlabel('X Pixels')
plt.tight_layout()

# Plot the original image

ax3 = fig.add_subplot(1,3,3)
ax3.imshow(image)
ax3.set_title('Original Image')
ax3.set_xlabel('X Pixels')
plt.tight_layout()
plt.show()
