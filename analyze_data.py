data = []

import csv
import matplotlib.pyplot as plt  
from math import *    

'''
with open('./test_datasets/babyheights.csv', mode='r') as d:
    reader = csv.reader(d)
    data = [(float(rows[0]),float(rows[1])) for rows in reader]'''


data = [(x, log(x)+100000) for x in range(2,100)]

def get_data(data):
    xs = [i[0] for i in data]
    ys = [i[1] for i in data]
    return xs, ys

def get_differences(data):
    xs = []
    ys = []
    for i in range(1,len(data)):
        xs.append(data[i][0])
        ys.append(1/(data[i][1]-data[i-1][1]))
    return xs,ys
    
def get_multiples(data):
    xs = []
    ys = []
    for i in range(1,len(data)):
        xs.append(data[i][0])
        ys.append(data[i][1]/data[i-1][1])
    return xs,ys
    
def get_exp(data, a=1):
    xs = []
    ys = []
    for i, point in enumerate(data[2:]):
        xs.append(point[0])
        ys.append(a**(point[1]/(a*log(a))))
    return xs,ys

def get_ln(data):
    xs = []
    ys = []
    for i, point in enumerate(data[2:]):
        xs.append(point[0])
        ys.append(log(point[1]))
    return xs,ys

figure, axis = plt.subplots(3, 3)

axis[0,0].plot(*get_data(data))
axis[0,1].plot(*get_differences(data))
axis[0,2].plot(*get_multiples(data))
'''
for a in range(25,35):
    axis[1,0].plot(*get_exp(data, a))'''

axis[1,1].plot(*get_ln(data))
axis[1,2].plot(*get_multiples(list(zip(*get_differences(data)))))



plt.show()