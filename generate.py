import os
import csv
import json
from statistics import mean, median

walkpath = "_data/"
lwalkpath = len(walkpath)

stats = {}
odata = {}

def process_files(root, dirname, filename, stats):
	f, e = os.path.splitext(filename)
	if e == '.csv' and f != "overall":
		path = os.path.join(root, filename)
		promo = f.replace('s', '#')
		
		with open(path, "r") as file:
			next(file) # Skip header row.
			
			data = [None]
			n = 1 # Dynamic length of data.
			for line in file:
				parts = line.split(',')
				lparts = len(parts)
				
				for i in range(n, lparts): # Increase size of data, as needed.
					data.append([])
					n += 1
				
				for i in range(1, lparts): # Skip login column.
					if parts[i] != "":
						try: data[i].append(float(parts[i]))
						except: pass
		
		final = data[n - 1]
		
		count = len(final)
		avg = round(mean(final), 2)
		med = round(median(final), 2)
		mini = min(final)
		maxi = max(final)
		
		if dirname not in stats:
			stats[dirname] = [["Promotion", "Count", "Average", "Median", "Minimum", "Maximum"]]
		
		stats[dirname].append([promo, count, avg, med, mini, maxi])
		
		if promo not in odata:
			odata[promo] = [[], [], [], [], []]
		
		odata[promo][0].append(count)
		odata[promo][1].append(avg)
		odata[promo][2].append(med)
		odata[promo][3].append(mini)
		odata[promo][4].append(maxi)

for root, dirs, files in os.walk(walkpath):
	print((root, dirs, files))
	dirname = root[lwalkpath:]
	if dirname != "":
		for filename in files:
			process_files(root, dirname, filename, stats)


stats[""] = [["Promotion", "Number of Homework", "Average Count", "Global Average", "Average Median", "Average Minimum", "Average Maximum"]]

for promo in sorted(odata):
	final = odata[promo]
	
	count = len(final[0])
	avgcount = round(mean(final[0]), 2)
	avgavg = round(mean(final[1]), 2)
	avgmed = round(mean(final[2]), 2)
	avgmini = round(mean(final[3]), 2)
	avgmaxi = round(mean(final[4]), 2)
	
	stats[""].append([promo, count, avgcount, avgavg, avgmed, avgmini, avgmaxi])

print(stats)

hwlist = []
for homework in sorted(stats):
	if homework:
		hwlist.append(homework)
	
	npath = os.path.join(walkpath, homework, 'overall.csv')
	with open(npath, 'w', newline='') as file:
		wr = csv.writer(file)
		for row in stats[homework]:
			wr.writerow(row)

hpath = os.path.join(walkpath, 'homeworklist.json')
with open(hpath, 'w', newline='') as file:
	json.dump(hwlist, file)
