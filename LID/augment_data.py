from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
import csv
import os

def getListOfFiles(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.wav' in file:
                files.append(os.path.join(r, file))
    return files

# Liste fuer die Features
MFCCEnglish = []
MFCCGerman = []

# Hier alle Daten aus dem englischen Ordner schnappen
path = '/home/panda/Desktop/solution_ws/Tensorflow/Sample_Data/English'
files = getListOfFiles(path)
englisch_tag = np.array([0])

for file in files:
    (rate,sig) = wav.read(file)
    print(rate)
    mfcc_feat = mfcc(sig, rate, numcep=26) #mfcc_feat -> numpy.ndarray
    mfcc_feat = mfcc_feat.sum(axis=0)
    mfcc_feat = mfcc_feat.tolist()
    mfcc_feat.append(0)
    MFCCEnglish.append(mfcc_feat) #MFCCGerman -> List

np.savetxt("MFCCEnglish.csv", MFCCEnglish, delimiter=",", fmt='%s')

# Hier alle Daten aus dem deutschen Ordner schnappen
path = '/home/panda/Desktop/solution_ws/Tensorflow/Sample_Data/German'
files = getListOfFiles(path)
german_tag = np.array([1])

for file in files:
    (rate,sig) = wav.read(file)
    mfcc_feat = mfcc(sig, rate, numcep=26) #mfcc_feat -> numpy.ndarray
    mfcc_feat = mfcc_feat.sum(axis=0)
    mfcc_feat = mfcc_feat.tolist()
    mfcc_feat.append(1)
    MFCCGerman.append(mfcc_feat) #MFCCGerman -> List

np.savetxt("MFCCGerman.csv", MFCCGerman, delimiter=",", fmt='%s')

