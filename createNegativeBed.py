import os, sys, csv

inFileName = sys.argv[1]
inFileDir = sys.argv[2]
outFileDir = sys.argv[3]
inFilePath = inFileDir + inFileName
outFilePath = outFileDir + inFileName

positiveRanges = []
negativeRanges = []

with open(inFilePath, "r") as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        positiveRanges.append([row[0], row[1], row[2]])

for i, row in enumerate(positiveRanges):
    if i + 1 < len(positiveRanges):
        negativeRanges.append([row[0], row[2], positiveRanges[i + 1][1]])

if not os.path.isdir(outFileDir): os.mkdir(outFileDir)
with open(outFilePath, "w") as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(negativeRanges)