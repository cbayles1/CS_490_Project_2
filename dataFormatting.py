import os, random

def removeHeaderLine(inFile):
    arr = []
    with open(inFile, 'r') as f:
        while True:
            headerLine = f.readline()
            nucleotide = f.readline()
            
            if not nucleotide: break #EOF
            nucleotide = nucleotide.strip()
            arr.append(nucleotide)
    return arr

def getAvgPosLength(positives):
    sumLineLen = 0
    sumFileLen = 0
    for x in positives:
        sumFileLen += len(x)
        for line in x:
            sumLineLen += len(line)
    return int(sumLineLen / sumFileLen)

def cropLengths(x, avgLineLen):
    x1 = [line for line in x if len(line) >= avgLineLen]
    for i, line in enumerate(x1):
        x1[i] = line[0:avgLineLen]
    return x1

def exportAtgcToFile(atgc, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        for nuc in atgc:
            f.write(nuc + "\n")

def main(posInDir, posOutDir, negInDir, negOutDir):
    positives = []
    negatives = []
    
    for inFilename in os.listdir(posInDir):
        if inFilename.startswith(".ipynb_checkpoints"): continue
        positives.append(removeHeaderLine(posInDir + inFilename))
        negatives.append(removeHeaderLine(negInDir + inFilename))

    avgLineLen = getAvgPosLength(positives)
    
    for i, x in enumerate(positives):
        y = negatives[i]
        x = cropLengths(x, avgLineLen)
        y = cropLengths(y, avgLineLen)
        x = [nuc.upper() for nuc in x] # capitalize
        y = [nuc.upper() for nuc in y] # capitalize
        random.shuffle(x)
        random.shuffle(y)
        exportAtgcToFile(x, posOutDir + str(i + 1) + ".txt")
        exportAtgcToFile(y, negOutDir + str(i + 1) + ".txt")

if __name__ == "__main__":
    main("./data/atgc/positives/", "./data/positives/", "./data/atgc/negatives/", "./data/negatives/")
    