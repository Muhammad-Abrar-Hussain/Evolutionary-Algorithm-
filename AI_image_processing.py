#import libraries
from random import random
from tokenize import group
import cv2 as cv
from cv2 import imshow
from cv2 import threshold
import numpy as np
import operator
import statistics

#read group images by opencv,change its color type & show group photo
group_image =cv.imread('groupgray.jpg')
group_image_gray = cv.cvtColor(group_image, cv.COLOR_BGR2GRAY)
# cv.imshow('gray', group_image_gray)

#read boothi image by opencv,change its color type & show group photo
boothi = cv.imread('boothigray.jpg')
boothi_gray = cv.cvtColor(boothi, cv.COLOR_BGR2GRAY)
#cv.imshow('boothi_image', boothi_gray )

#find number of rows & colums in boothi_gray & group_image_gray
groupimage_xy = np.shape(group_image_gray)
boothi_xy  = np.shape(boothi_gray)
   
def population_initialization(rows, columns, population_size):
    current_generation = []
    individual = 0
    while len(current_generation) <= population_size:
        random_point = np.random.randint(rows), np.random.randint(columns)
        
        if(random_point[0] + boothi_xy[0] < groupimage_xy[0]) and (random_point[1] + boothi_xy[1] < groupimage_xy[1]):
           current_generation.append(random_point)
        else:
            individual = individual
    #print(current_generation)        
    return(current_generation)

def fitness_evalutation(current_generation, group_image, boothi_image):
    co_relation_values = []
    for point in current_generation:  
        image_crop = group_image[point[0]:point[0]+boothi_image[0], point[1]:point[1]+boothi_image[1]]
       
        upper = np.mean((image_crop - image_crop.mean())*(boothi_gray - boothi_gray.mean()))
        lower  = image_crop.std()*boothi_gray.std()
        if (lower == 0):
            return 0
        else:
            corr = upper/lower
            co_relation_values.append(corr)
    return  co_relation_values

def selection(current_generation,fitness_value):
    corelation_index  = {}
    corelation_keys= []
    corelation_values = []
    selected_generation = []
    index= 0
    for value in fitness_value:
        corelation_index.update({current_generation[index]: value})
        index += 1     
    #sort dictonary(corelation_index) on the base of value
    sort_corelation_index = dict( sorted(corelation_index.items(), key=operator.itemgetter(1),reverse=True))
    items = sort_corelation_index.items()
    for item in items:
        corelation_keys.append(item[0]), corelation_values.append(item[1])   
    values  = 0
    while values < 30:
        selected_generation.append(corelation_keys[values])
        values += 1
    return selected_generation
   
def new_generation(current_generation, group_imagerow, group_imagecolum):

    xy_binary = []
    random_cut_left = []
    random_cut_right = []
    new_generation_binary = []
    new_generation_decm = []
    for values in current_generation:
    #convert decimal into binary
        binary_x = bin(values[0])
        binary_y = bin(values[1])
    #remove "0b" from the start of binary using slicing
        binary_xpoint = binary_x[2:]
        binary_ypoint = binary_y[2:]
    #To maintain maximum  length of binary 512 & 1024 = 2**9 & 2**10 respectively, use .zfill function:
        x_binary = str(binary_xpoint).zfill(9)
        y_binary = str(binary_ypoint).zfill(10)
    #concatenate binary of xy.
        join_xy = x_binary + y_binary
        xy_binary.append(join_xy)
    #generate random number between '0' and '19' because over combine xy bit length is '19'
    random = np.random.randint(1,19)
    #cut the xy combine binary xy random number & store lelf & right cut into 
    # random_cut_left & random_cut_right respectively:
    for binary in xy_binary:
        random_cut_left.append(binary[:random]) 
        random_cut_right.append(binary[random:]) 
        
    #generate new population by the combination of p1 &p2 parent i.e xy... 
    # &  store values into new generation list:
    for val in range(0, len(random_cut_left), 2):
      left_p1 = random_cut_left[val]
      right_p1 = random_cut_right[val]
      left_p2 = random_cut_left[val+1]
      right_p2 = random_cut_right[val+1]
      new_generation_binary.append((left_p1 + right_p2))
      new_generation_binary.append((left_p2 + right_p1))
    #cut the xy combine binary xy random number & store lelf & right cut into 
    # random_cut_left & random_cut_right respectively:
    for index in new_generation_binary:
        xy_int = int((index[:9]),2), int((index[9:]),2)
        new_generation_decm.append(xy_int)

    print(new_generation_decm)
    return new_generation_decm
    
    
    
         
def main():
    
    current_generation = population_initialization(groupimage_xy[0], groupimage_xy[1], 100)
    fitness_value = fitness_evalutation(current_generation ,group_image_gray,boothi_xy)
    selected_generation = selection(current_generation, fitness_value)
    current_generation = new_generation(selected_generation, groupimage_xy[0], groupimage_xy[1])
    for i in range(1000):
        
        if max(fitness_value) >= 0.9:
            print(fitness_value)
            print(current_generation)
            print(max(fitness_value))
            xy = current_generation[fitness_value.index(max(fitness_value))]
            p = cv.rectangle(group_image_gray, (xy),(xy[0]+35,xy[1]+29),(255,0,0), thickness=1)
            cv.imshow('p',p)
            break
        else:
            fitness_value = fitness_evalutation(current_generation ,group_image_gray,boothi_xy)
            selected_generation = selection(current_generation, fitness_value)
            current_generation = new_generation(selected_generation, groupimage_xy[0], groupimage_xy[1])
    print(i)   
            
main()

cv.waitKey(0)

