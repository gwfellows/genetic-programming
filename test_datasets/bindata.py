import csv
import statistics

data = []
with open('crop_yields_vs_soil_salinity_processed.txt', mode='r') as d:
    reader = csv.reader(d)
    data = [(float(rows[0]),float(rows[1])) for rows in reader]

segs = 20

for i in range(segs):
    start = 2.647479954+(i/segs)*(22.83505155-2.647479954)
    mid = 2.647479954+(i/segs + 1/(segs*2))*(22.83505155-2.647479954)
    end = 2.647479954+(i/segs + 1/(segs*2))*(22.83505155-2.647479954)
    
    print(mid,",", statistics.mean([row[1] for row in data if (start*0.9<=row[0]<=end*1.1)]))

    