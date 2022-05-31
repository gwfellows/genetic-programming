import matplotlib.pyplot as plt
import csv
citation = "Oosterbaan, R.J.. (2019). CROP TOLERANCE TO SOIL SALINITY, STATISTICAL ANALYSIS OF DATA MEASURED IN FARM LANDS."
data = []
with open('crop_yields_vs_soil_salinity.csv', mode='r') as d:
    reader = csv.reader(d)
    data = [(float(rows[0]),float(rows[1])) for rows in reader]

x = [pair[0] for pair in data]
y = [pair[1] for pair in data]

plt.scatter(x,y, marker="o")
import math
def f(a):
    return math.log(0.0319*a+0.0216) * (2.926e-5*a**4 + 0.000139*a**3+8.12e-5*a**2) + 3.81

x2 = []
y2 = []

mx = max(x)
mn = min(x)

for x in range(0,1000):
    x = (x/1000)*(mx-mn) + mn
    x2.append(x)
    y2.append(f(x))

    
plt.plot(x2,y2,color="red",linestyle="--")
plt.ylabel("yield of barley (t/ha)")
plt.xlabel("soil salinity in ECe (dS/m)")
#plt.title(citation)
plt.show()


