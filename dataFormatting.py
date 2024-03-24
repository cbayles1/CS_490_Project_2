import os, random

def cropLengths(pos, neg):
    sumLineLen = 0
    # For now, I'm just using the avg length of positive lines to crop both positive and negative, to avoid empty positive outputs.
    # I could use the avg length to split the negative lines up into chunks if needed, but that would skew the data heavily.
    for line in pos: sumLineLen += len(line)
    avgLineLen = int(sumLineLen / len(pos))

    pos1 = [line for line in pos if len(line) >= avgLineLen]
    neg1 = [line for line in neg if len(line) >= avgLineLen]
    for i, line in enumerate(pos1):
        pos1[i] = line[0:avgLineLen]
    for i, line in enumerate(neg1):
        neg1[i] = line[0:avgLineLen]
    return pos1, neg1

def exportAtgcToFile(atgc, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        for nuc in atgc:
            f.write(nuc + "\n")

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

def main(posInDir, posOutDir, negInDir, negOutDir):
    smallerInDir = posInDir
    if len(negInDir) < len(posInDir):
        smallerInDir = negInDir
    for inFilename in os.listdir(smallerInDir):
        if inFilename.startswith(".ipynb_checkpoints"): continue
        
        x = removeHeaderLine(posInDir + inFilename)
        y = removeHeaderLine(negInDir + inFilename)
        x, y = cropLengths(x, y)
        x = [nuc.upper() for nuc in x] # capitalize
        y = [nuc.upper() for nuc in y] # capitalize
        random.shuffle(x)
        random.shuffle(y)
        exportAtgcToFile(x, posOutDir + inFilename)
        exportAtgcToFile(y, negOutDir + inFilename)

if __name__ == "__main__":
    main("./data/atgc/positives/", "./data/positives/", "./data/atgc/negatives/", "./data/negatives/")
    