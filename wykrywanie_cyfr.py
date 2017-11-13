import matplotlib.pyplot as plt
import numpy as np
from skimage import data, io, measure, color, feature, filters, exposure, img_as_ubyte, morphology, transform, draw
from math import ceil
from skimage.feature import match_template

def polygon_area(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def recognize_if_sign(adjusted_image, k, templates):
    result = -1
    for x in range(10):        
            if match_template(adjusted_image, templates[x]) > 0.65:
                result = x
                break
    return result

def draw_rectangle(image,x_min, y_min, x_max, y_max):
    rr,cc = draw.polygon_perimeter([x_min, x_max, x_max, x_min], [y_min, y_min, y_max, y_max], shape=None, clip=False)
    image[rr,cc] = (0,255,255)
    return image

    
def process_image(image_input, k, templates_array, numOfPictures):
    subPlt = plt.subplot(numOfPictures,1,k+1)
    plt.axis('off')
    subPlt.set_aspect('equal')

    image = color.rgb2gray(image_input)
    percentileP, percentileK = np.percentile(image,(2,98))
    #image = exposure.rescale_intensity(image,in_range=(percentileP,percentileK))
    image = morphology.closing(image)
    image = morphology.opening(image)
    #image = morphology.dilation(image)
    #image = morphology.erosion(image)
    edges = measure.find_contours(image, level=0.3, fully_connected='low', positive_orientation='high')
    array_min_max = []
    for n, coords in enumerate(edges):
        sizeOfPolygon = polygon_area(coords[:,1],coords[:,0]) #niepotrzebne
        if (coords[0,1] == coords[-1,1]) and (coords[0,0] == coords[-1,0]):
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
        adjusted_image = transform.resize(adjusted_image, (12, 8),mode='reflect')         
        res = recognize_if_sign(adjusted_image, n, templates_array)
        if res != -1:
           print(res)
           image_input = draw_rectangle(image_input,instance[2],instance[0],instance[3],instance[1])
           io.imshow(templates_array[res])
    io.imshow(image_input)

if __name__ == '__main__':
    plt.figure(figsize=(50,100))
    images = io.ImageCollection('images/*.jpg') #'obrazy do testow/*.jpg'   'images/*.jpg'
    templates_input = io.ImageCollection('data_sets/*.jpg')
    templates = []
    for template in templates_input:
       	template = transform.resize(template, (12, 8),mode='reflect')
        templates.append(color.rgb2gray(template))
    for n,image in enumerate(images):
        process_image(image,n, templates, len(images))
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig('edges.pdf')   
