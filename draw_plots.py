import matplotlib.pyplot as plt
import csv

x=[]
y=[]

with open('crossover_ratio.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        x.append(float(row[0]))
        y.append(float(row[1]))

plt.scatter(x,y, marker='o')
plt.xlabel('Crossover Rate')
plt.ylabel('Time to Reach Fitness Target (s)')
plt.yscale('log')
plt.legend()

plt.savefig('crossover_ratio.png')

plt.show()

x=[]
y=[]

with open('pop_size.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        x.append(float(row[0]))
        y.append(float(row[1]))

plt.scatter(x,y, marker='o')
plt.xlabel('Population Size')
plt.ylabel('Time to Reach Fitness Target (s)')
plt.legend()

plt.savefig('population_size.png')

plt.show()

x=[]
y=[]

with open('init_max_depth.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        x.append(float(row[0]))
        y.append(float(row[1]))

plt.scatter(x,y, marker='o')
plt.yscale('log')
plt.xlabel('Initial Max Depth')
plt.ylabel('Time to Reach Fitness Target (s)')
plt.legend()

plt.savefig('init_max_depth.png')

plt.show()