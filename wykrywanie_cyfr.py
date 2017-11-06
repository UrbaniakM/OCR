'''AUTHORS
Mateusz Urbaniak
Kajetan Zimniak'''

import matplotlib.pyplot as plt
import numpy as np
from skimage import data, io, measure, color, feature, filters, exposure, img_as_ubyte, morphology, transform
from math import ceil

def polygon_area(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def recognize_if_sign(adjusted_image, k):
    subPlt = plt.subplot(5,2,k+1)
    plt.axis('off')
    subPlt.set_aspect('equal')
    io.imshow(adjusted_image)
    
def process_image(image_input, k):
    
    #subPlt = plt.subplot(1,2,k+1)
    #
    image = color.rgb2gray(image_input)
    percentileP, percentileK = np.percentile(image,(2,98))
    image = exposure.rescale_intensity(image,in_range=(percentileP,percentileK))
    #TODO - noise removing
    edges = measure.find_contours(image, level=0.3, fully_connected='low', positive_orientation='high')
    array_min_max = []
    for n, coords in enumerate(edges):
        sizeOfPolygon = polygon_area(coords[:,1],coords[:,0])
        if (sizeOfPolygon > 50) and (coords[0,1] == coords[-1,1]) and (coords[0,0] == coords[-1,0]):
            xMin, xMax = (np.min(coords[:,1]),np.max(coords[:,1]))
            yMin, yMax = (np.min(coords[:,0]),np.max(coords[:,0]))
            not_inside = True
            for instance in array_min_max:
               if (xMin > instance[0]) and (xMax < instance[1]) and (yMin > instance[2]) and (yMax < instance[3]):
                   not_inside = False
            if not_inside == True:
                array_min_max.append([int(xMin), ceil(xMax), int(yMin), ceil(yMax)]) #min - round down, max - round up
    for n,instance in enumerate(array_min_max):
        adjusted_image = image[instance[2]:instance[3],instance[0]:instance[1]] #cropping - image[ymin:ymax,xmin:xmax]
        # RESIZE? RESCALE? etc.
        recognize_if_sign(adjusted_image, n)

if __name__ == '__main__':
    plt.figure(figsize=(50,100))
    images = io.ImageCollection('images/*.jpg')

    for n,image in enumerate(images):
        process_image(image,n)
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig('edges.pdf')   
