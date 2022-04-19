import matplotlib.pyplot as plt
import csv

x=[]
y=[]

with open('populationsizetest.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        x.append(float(row[0]))
        y.append(float(row[1]))

plt.scatter(x,y, marker='o')

plt.xlabel('Population Size')
plt.ylabel('Individuals Proccessed to Reach Completion (Avg. of 100)')

x=[]
y=[]

for i in range(50,295,1):
    x.append(i)
    y.append(11290.4-98.529*i+0.525703*i*i-0.000853652*i*i*i)

plt.plot(x,y, color='black')

plt.axvline(x=144.739,color='red', linestyle='--', label='optimal population size of around 145')
plt.legend()

plt.savefig('results.png')

plt.show()