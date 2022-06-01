import matplotlib.pyplot as plt
import csv
citation = "Oosterbaan, R.J.. (2019). CROP TOLERANCE TO SOIL SALINITY, STATISTICAL ANALYSIS OF DATA MEASURED IN FARM LANDS."
data = []
with open('babyheights.csv', mode='r') as d:
    reader = csv.reader(d)
    data = [(float(rows[0]),float(rows[1])) for rows in reader]

x = [pair[0] for pair in data]
y = [pair[1] for pair in data]

plt.scatter(x,y, marker="o")
import math
def f(a):
    #0.337X+11.1\ln\left(X+1.9\right)+43
    return 0.337*a+11.1*math.log(a+1.9)+43

x2 = []
y2 = []

mx = max(x)
mn = min(x)

for x in range(0,1000):
    x = (x/1000)*(mx-mn) + mn
    x2.append(x)
    y2.append(f(x))

#0.1568459619399607 X - 306.00613944659269
    
plt.plot(x2,y2,color="red",linestyle="--")
plt.ylabel("50th percentile height")
plt.xlabel("months alive")
#plt.title(citation)
plt.show()


