import os, csv, random

def loadDir(dataset, dir, label):
    for filename in os.listdir(dir):
        if filename.startswith(".ipynb_checkpoints"): continue
        with open(dir + filename, 'r') as f:
            while True:
                seq = f.readline()
                dataset.append([label, seq.strip()])
                if not seq:
                    break

def exportDataset(dataset, outPath):
    with open(outPath, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(dataset)

def splitDataset(dataset, trainingPercent):
    splitPoint = int(len(dataset) * trainingPercent)
    training = dataset[:splitPoint]
    testing = dataset[splitPoint:]
    return training, testing

if __name__ == "__main__":
    POSITIVE_DIR = "./data/positives/"
    NEGATIVE_DIR = "./data/negatives/"
    POSITIVE_LABEL = 0
    NEGATIVE_LABEL = 1
    OUT_TRAINING_FILEPATH = "./data/training_dataset.tsv"
    OUT_TESTING_FILEPATH = "./data/testing_dataset.tsv"
    
    dataset = []
    loadDir(dataset, POSITIVE_DIR, POSITIVE_LABEL)
    loadDir(dataset, NEGATIVE_DIR, NEGATIVE_LABEL)
    random.shuffle(dataset)
    training, testing = splitDataset(dataset, 0.7)
    exportDataset(training, OUT_TRAINING_FILEPATH)
    exportDataset(testing, OUT_TESTING_FILEPATH)
