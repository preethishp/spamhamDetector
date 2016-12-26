import os
import argparse
import fnmatch
import math
import pickle
import re


def changeDir(path):
    os.chdir(path)

def findAllFiles(path):
    allFiles = [os.path.join(pathDir, filename)
                 for pathDir, namedir, tfiles in os.walk(path)
                 for filename in fnmatch.filter(tfiles, '*.txt')]
    return allFiles



def openModel(storePath):
    os.chdir(storePath)
    listPass = []
    with open('nbmodel.txt','rb') as fileHandle:
        listPass = pickle.loads(fileHandle.read(), encoding='latin1')
    return listPass

def extractKeyWords(fileParam):
    wordList = []
    with open(fileParam, 'r', encoding='latin1') as fileHandle:
        wordList = fileHandle.read().split()
        return wordList

def stemWord(keyWord):
    patternStem = re.compile("ing")
    strOutput = patternStem.split(keyWord)
    if len(strOutput) == 2:
        if len(strOutput[0]) > 1:
            return strOutput[0]
    else:
        return keyWord

def calcProbOfDocGivenClass(fileKeyWordList, modelParams):
    probOfDocGivenClass = []
    probOfDocGivenSpam = 0
    probOfDocGivenHam = 0
    spamProbDict = modelParams[2]
    hamProbDict = modelParams[3]
    for keyWord in fileKeyWordList:
        keyWord = stemWord(keyWord)
        if keyWord in spamProbDict:
            probOfDocGivenSpam += math.log(spamProbDict[keyWord])
        if keyWord in hamProbDict:
            probOfDocGivenHam += math.log(hamProbDict[keyWord])
    probOfDocGivenClass.append(probOfDocGivenSpam)
    probOfDocGivenClass.append(probOfDocGivenHam)

    return probOfDocGivenClass


def calcClassGivenDoc(probOfClass, probOfDocGivenClass):
    return (math.log(probOfClass)  + probOfDocGivenClass)


def classifyDocument(singleFile, modelParams):
    resultString = ['spam','ham']
    fileKeyWordList = []
    fileKeyWordList = extractKeyWords(singleFile)
    #print(singleFile)
    # #print(fileKeyWordList)
    probOfDocGivenClass = calcProbOfDocGivenClass(fileKeyWordList, modelParams)
    probOfSpam = modelParams[1]
    probOfHam = 1 - probOfSpam

    probSpamGivenDoc = calcClassGivenDoc(probOfSpam, probOfDocGivenClass[0])
    probHamGivenDoc = calcClassGivenDoc(probOfHam, probOfDocGivenClass[1])


    if(probSpamGivenDoc > probHamGivenDoc):
        return resultString[0]
    elif(probSpamGivenDoc < probHamGivenDoc):
        return resultString[1]














if __name__ == '__main__':
    storePath = os.getcwd()
    parserObj = argparse.ArgumentParser()
    parserObj.add_argument("path_to_folders", help="Specify the path")
    firstArg = parserObj.parse_args()
    direcPath = firstArg.path_to_folders
    changeDir(direcPath)
    allFiles = findAllFiles(direcPath)
    #print(len(allFiles))
    # #dictContainer = tokenizeWordsFromList(allFiles)
    #figure out whether the word frequencies needs to be calculated. I am moving on to finish another task of 			converting json from nblearn into a dict
    modelParams = []
    modelParams = openModel(storePath)

    #print(len(modelParams))
    resultList = []
    os.chdir(storePath)
    rememberSpam = 0
    rememberHam = 0
    with open('nboutput.txt',mode='w',encoding='latin1') as fileHandle:
        for singleFile in allFiles:
            strValue = classifyDocument(singleFile, modelParams)
            if(strValue == 'spam'):
                rememberSpam += 1
                fileHandle.write(strValue + ' ')
            elif(strValue=='ham'):
                rememberHam += 1
                fileHandle.write(strValue + ' ')


            fileHandle.write(singleFile + '\n')
            #fileHandle.write(classifyDocument(singleFile, modelParams) + '\n')

    #print(rememberSpam, rememberHam)