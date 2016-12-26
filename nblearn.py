import os
import argparse
import pickle

def changeDir(path):
    '''This function changes the directory'''
    os.chdir(path)


#def findAllSpamFiles(path):
 #   spamFiles = [os.path.join(pathDir, filename)
  #               for pathDir, namedir, tfiles in os.walk(path)
   #              for filename in fnmatch.filter(tfiles, '*spam.txt')]

    #return spamFiles
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


def addToDict(wordList, dictContainer):
    for item in wordList:
        if item in dictContainer:
            dictContainer[item] += 1
        else:
            dictContainer[item] = 1


def normalizeCount(modDict, checkDict):
    for keyString in checkDict:
        if keyString not in modDict:
            modDict[keyString] = 0
    return modDict

def addToDictOpp(wordList, dictContainer):
    for item in wordList:
        if item not in dictContainer:
            dictContainer[item] = 0


def tokenizeWordsFromList(spampath, hampath):
    spamdictContainer = {}
    hamdictContainer = {}
    dictList = []
    noOfWordsInSpam = 0
    noOfWordsInHam = 0
    for item in spampath:
        with open(item, 'r', encoding="latin1") as fileHandle:
            wordList = fileHandle.read().split()
            noOfWordsInSpam += len(wordList)
            # print(wordList)
            addToDict(wordList, spamdictContainer)
            addToDictOpp(wordList, hamdictContainer)
    for item in hampath:
        with open(item, 'r', encoding="latin1") as fileHandle:
            wordList = fileHandle.read().split()
            noOfWordsInHam += len(wordList)
            # print(wordList)
            addToDictOpp(wordList, spamdictContainer)
            addToDict(wordList, hamdictContainer)


    dictList.append(noOfWordsInSpam)
    dictList.append(spamdictContainer)
    dictList.append(noOfWordsInHam)
    dictList.append(hamdictContainer)


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
    classDictList = tokenizeWordsFromList(spamFiles, hamFiles)
    #hamDictList = tokenizeWordsFromList(hamFiles)
    spamDict = classDictList[1]
    hamDict = classDictList[3]
    noOfWordsInSpam = classDictList[0]
    noOfWordsInHam = classDictList[2]
    #spamDict = normalizeCount(spamDict, hamDict)
    #hamDict = normalizeCount(hamDict, spamDict)
    #print(len(spamDictList[1]),len(hamDictList[1]))
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


