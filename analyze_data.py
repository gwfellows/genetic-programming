data = []

import csv
import matplotlib.pyplot as plt  
from math import *    


with open('pop_size.csv', mode='r') as d:
    reader = csv.reader(d)
    data = [(float(rows[0]),float(rows[1])) for rows in reader]

def get_data(data):
    xs = [i[0] for i in data]
    ys = [i[1] for i in data]
    return xs, ys

def get_differences(data):
    xs = []
    ys = []
    for i, point in enumerate(data[1:]):
        xs.append(point[0])
        ys.append((point[1]-data[i-1][1])/(point[0]-data[i-1][0]))
    return xs,ys
    
def get_multiples(data):
    xs = []
    ys = []
    for i, point in enumerate(data[1:]):
        xs.append(point[0])
        ys.append((point[1]/data[i-1][1])/(point[0]-data[i-1][0]))
    return xs,ys
    
def get_exp(data, a=1):
    xs = []
    ys = []
    for i, point in enumerate(data[1:]):
        xs.append(point[0])
        ys.append(a**(point[1]/(a*log(a))))
    return xs,ys

figure, axis = plt.subplots(3, 3)

axis[0,0].plot(*get_data(data))
axis[0,1].plot(*get_differences(data))
axis[0,2].plot(*get_multiples(data))
'''
for a in range(25,35):
    axis[1,0].plot(*get_exp(data, a))'''
#axis[1,1].plot(*get_multiples(list(zip(*get_exp(data)))))



plt.show()