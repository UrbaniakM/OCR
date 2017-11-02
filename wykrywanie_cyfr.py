'''AUTHORS
Mateusz Urbaniak
Kajetan Zimniak'''

import matplotlib.pyplot as plt
import numpy as np
from skimage import data, io, measure, color, feature, filters, exposure, img_as_ubyte, morphology, transform

def polygon_area(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def recognition_sign(coords1,coords0):
    #plt.plot(coords1,coords0)
    #plt.show()
    #todo
    print("")
    
def process_image(image_input, k):
    #subPlt = plt.subplot(25,4,k+1)
    subPlt = plt.subplot(1,2,k+1)
    plt.axis('off')
    image = color.rgb2gray(image_input)
    percentileP, percentileK = np.percentile(image,(2,98))
    image = exposure.rescale_intensity(image,in_range=(percentileP,percentileK))
    edges = measure.find_contours(image, level=0.3, fully_connected='low', positive_orientation='high')
    subPlt.set_aspect('equal')
    minCoord = [] #potrzebne do wycinania krawedzi
    maxCoord = [] #potrzebne do wycinania krawedzi
    temp = True #potrzebne do wycinania krawedzi
    for n, coords in enumerate(edges):
        sizeOfPolygon = polygon_area(coords[:,1],coords[:,0])
        if (sizeOfPolygon > 50) and (coords[0,1] == coords[-1,1]) and (coords[0,0] == coords[-1,0]):
            print(np.min(coords[:,1]))
            print(np.max(coords[:,1]))

            plt.plot(coords[:, 1], coords[:, 0], linewidth=1)
            plt.plot(np.mean(coords[:,1]),np.mean(coords[:,0]), 'wo', markersize=3)
        #Sprawdzanie czy to nie jest czesc juz gotowej cyfry
        minCoord.append(min(coords[:,1]))
        maxCoord.append(max(coords[:,1]))
        for a,minValue in enumerate(minCoord):
            if maxCoord[a] > min(coords[:,1]) and min(coords[:,1]) > minCoord[a]:
                temp = False 
        if temp == True:
            recognition_sign(coords[:,1],coords[:,0])
        
    subPlt.set_aspect('equal')
    io.imshow(image)

if __name__ == '__main__':
    plt.figure(figsize=(50,100))
    images = io.ImageCollection('images/*.jpg')

    for n,image in enumerate(images):
        process_image(image,n)
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig('edges.pdf')   
