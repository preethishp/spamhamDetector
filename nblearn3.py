import os
import argparse
import fnmatch
import pickle
import re

#TODO: Modification: Eliminate stuff other than alphabets. Eliminate special characters, numbers, etc.
def changeDir(path):
    '''This function changes the directory'''
    os.chdir(path)

def pathJoin(dirNamePath, listCon):
    returnList = []
    for item in listCon:
        returnList.append(os.path.join(dirNamePath, item))
    return returnList

def findAllSpamFiles(path):
    listDir = []
    for dirNamePath, dtory, fileNames in os.walk(path):
        for name in dtory:
            if name == 'spam':
                os.chdir(os.path.join(dirNamePath, name))

                listDir.extend(pathJoin(os.path.join(dirNamePath, name), os.listdir(os.getcwd())))
                #print(len(listDir))
                #listDir = os.path.join(dirNamePath,os.listdir((os.getcwd())))
    #print(len(listDir))
    return listDir




def findAllHamFiles(path):
    listDir = []
    for dirNamePath, dtory, fileNames in os.walk(path):
        for name in dtory:
            if name == 'ham':
                os.chdir(os.path.join(dirNamePath, name))
                listDir.extend(pathJoin(os.path.join(dirNamePath, name), os.listdir(os.getcwd())))
                #print(len(listDir))
    #print(len(listDir))
    return listDir

def checkspl(item):
    patternSpl = re.compile(r'\W+')
    if patternSpl.search(item) is None:
        return False
    else:
        return True

def addToDict(wordList, dictContainer):
    patternStem = re.compile("ing")
    patternStemPlural = re.compile(r"\w+")
    stopWords = ['the', 'a', 'he', 'she','all','about','him','her','them','their','they','are','be','an','also','and','any','as','ask','back','but','however','Subject','subject','both','did','had','has','himself','have','herself','if','in','then','else','for','into','is','let','mr','mrs','mr.','mrs.']
    for item in wordList:
        if item.isdigit():
            continue
        if checkspl(item):
            continue
        if item in stopWords:
            continue
        strOutput = patternStem.split(item)
        if len(strOutput) == 2:
            if len(strOutput[0]) > 1:
                item = strOutput[0]
        if item in dictContainer:
            dictContainer[item] += 1
        else:
            dictContainer[item] = 1


def normalizeCount(modDict, checkDict):
    for keyString in checkDict:
        if keyString not in modDict:
            modDict[keyString] = 0
    return modDict


def tokenizeWordsFromList(filepath):
    dictContainer = {}
    dictList = []
    noOfWordsInClass = 0
    for item in filepath:
        with open(item, 'r', encoding="latin1") as fileHandle:
            wordList = fileHandle.read().split()
            noOfWordsInClass += len(wordList)
            # print(wordList)
            addToDict(wordList, dictContainer)
    dictList.append(noOfWordsInClass)
    dictList.append(dictContainer)


    return dictList


def calculateWordProb(inputDict, vocabSize, noOfWordsInClass):
    outputDashDict = {}
    totNumOfWordsClass = noOfWordsInClass
    for key in inputDict.keys():
        countKeyWordl = inputDict[key]
        #print(countKeyWordl, key, totNumOfWordsClass, vocabSize)
        probOfWordClass = (countKeyWordl + 1) / (totNumOfWordsClass + vocabSize)
        outputDashDict[key] = probOfWordClass

    return outputDashDict


def writeModelToFile(spamOutputDict, hamOutputDict, vocabSize, probOfSpam, storePath):
    os.chdir(storePath)
    listPass = [vocabSize, probOfSpam, spamOutputDict, hamOutputDict]
    with open('nbmodel.txt', mode='wb') as fileHandle:

        pickle.dump(listPass, fileHandle)
    return True


if __name__ == '__main__':
    storePath = os.getcwd()
    parserObj = argparse.ArgumentParser()
    parserObj.add_argument("path_to_folders", help="Specify the path")
    firstArg = parserObj.parse_args()
    direcPath = firstArg.path_to_folders

    changeDir(direcPath)

    spamFiles = findAllSpamFiles(direcPath)
    #print(len(spamFiles))

    hamFiles = findAllHamFiles(direcPath)
    #print(len(hamFiles))

    totNumber = len(spamFiles) + len(hamFiles)
    probOfSpam = len(spamFiles) / totNumber

    noOfWordsInSpam = 0
    noOfWordsInHam = 0
    spamDictList = tokenizeWordsFromList(spamFiles)
    hamDictList = tokenizeWordsFromList(hamFiles)
    spamDict = spamDictList[1]
    hamDict = hamDictList[1]
    noOfWordsInSpam = spamDictList[0]
    noOfWordsInHam = hamDictList[0]
    spamDict = normalizeCount(spamDict, hamDict)
    hamDict = normalizeCount(hamDict, spamDict)
    vocabSize = len(spamDict)
    #print(len(spamDict), len(hamDict))
    #print(noOfWordsInSpam, noOfWordsInHam)

    spamOutputDict = calculateWordProb(spamDict, vocabSize, noOfWordsInSpam)

    hamOutputDict = calculateWordProb(hamDict, vocabSize, noOfWordsInHam)

    #print(spamOutputDict)
    #print(hamOutputDict)

    if (not writeModelToFile(spamOutputDict, hamOutputDict, vocabSize, probOfSpam, storePath)):
        print('Model was not exported to nbmodel.txt')

    #with open('nbmodel.txt', mode='r',encoding='latin1') as fileHandle:
        #print(fileHandle.read())


