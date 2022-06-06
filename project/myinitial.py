import os
import re
import cchardet as chardet
import pandas as pd
import myglobal


def getKeyHeaderId(tokens):
    keyHeaderId = ""
    tokensLength = len(tokens)
    if tokensLength > 0:
        match = re.match(myglobal.REG_EXP, tokens[0], re.I)
        if match:
            keyHeaderId = match.groups()[0]
    return keyHeaderId


def getInputDataInfo(inputDataFilePath, inputDataFile, file_encoding):
    cnt = 0
    inputDataInfo = {}
    try:
        fp = open(inputDataFilePath, encoding=file_encoding)
        for line in fp:
            if cnt == 2:
                break
            tokens = line.split(",")
            if cnt == 0:  # first line
                keyHeaderId = getKeyHeaderId(tokens)
                if not keyHeaderId:
                    exit("There is some problem(line1) in {} file.".format(inputDataFile))
                inputDataInfo = {
                    myglobal.KEY_INPUTDATA_FILENAME: inputDataFile,
                    myglobal.KEY_INPUTDATA_HEADERID: keyHeaderId,
                    myglobal.KEY_INPUTDATA_HEADERSIZE: len(tokens)
                }
            else:  # second line
                if len(tokens) == inputDataInfo[myglobal.KEY_INPUTDATA_HEADERSIZE]:
                    inputDataInfo[myglobal.KEY_INPUTDATA_HEADERNAMES] = tokens
                else:
                    exit("There is some problem(line2) in {} file.".format(inputDataFile))
            cnt += 1
    finally:
        fp.close()
    myglobal.g_inputdata_infos.append(inputDataInfo)


def detectFileEncoding(inputDataFilePath):
    with open(inputDataFilePath, "rb") as f:
        msg = f.read()
        result = chardet.detect(msg)
        if result["encoding"] == "SHIFT_JIS" or result["encoding"] == "ISO-8859-1":
            return "CP932"
        return result["encoding"]

def getAllInputDataInfo(inputDataPath):
    allInputDataFiles = [f for f in os.listdir(inputDataPath) if f.endswith('.csv')]
    for inputDataFile in allInputDataFiles:
        file_encoding = detectFileEncoding(inputDataPath + '/' + inputDataFile)
        getInputDataInfo(inputDataPath + '/' + inputDataFile, inputDataFile, file_encoding)


def find_inputdata(filename):
    result = None
    for inputdata_info in myglobal.g_inputdata_infos:
        if inputdata_info[myglobal.KEY_INPUTDATA_FILENAME] == filename:
            result = inputdata_info
            break
    return result


def isValidReferFromOrTo(filename, headeridinfo, headername):
    inputdata_info = find_inputdata(filename)
    if inputdata_info is None:
        return False
    match = re.match(myglobal.REG_EXP, headeridinfo, re.I)
    if match:
        items = match.groups()
        headerid = items[0]
        headerindex = int(items[1])
        if headerid == inputdata_info[myglobal.KEY_INPUTDATA_HEADERID] and headerindex <= inputdata_info[
            myglobal.KEY_INPUTDATA_HEADERSIZE]:
            if inputdata_info[myglobal.KEY_INPUTDATA_HEADERNAMES][headerindex - 1] == headername:
                return True
    return False


def isValidReferRow(row):
    if len(row) != 6:
        return False
    if (isValidReferFromOrTo(row[0], row[1], row[2]) == False):
        return False
    return isValidReferFromOrTo(row[3], row[4], row[5])


def getReferenceInfo(referFilePath):
    xl = pd.ExcelFile(referFilePath)
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name, header=None)
        df = df.reset_index()
        for index, row in df.iterrows():
            listRow = row.tolist();
            listRow.pop(0)
            listRow = [item for item in listRow if str(item) != 'nan']
            if isValidReferRow(listRow) == False:
                continue
            refer_info = {
                myglobal.KEY_REFER_FROM_FILENAME: row[0],
                myglobal.KEY_REFER_FROM_HEADERID: row[1],
                myglobal.KEY_REFER_FROM_HEADERNAME: row[2],
                myglobal.KEY_REFER_TO_FILENAME: row[3],
                myglobal.KEY_REFER_TO_HEADERID: row[4],
                myglobal.KEY_REFER_TO_HEADERNAME: row[5]
            }
            myglobal.g_refer_infos.append(refer_info)


def isValidGroupRow(row):
    for item in row:
        if find_inputdata(item) is None:
            return False
    return True

def getGroupInfo(groupFilePath):
    xl = pd.ExcelFile(groupFilePath)
    df = xl.parse(xl.sheet_names[0], header=None)
    df = df.reset_index()
    if df.shape[0] != 2:
        exit("The group table file should have only 2 rows.")
    for index, row in df.iterrows():
        listRow = row.tolist();
        listRow.pop(0)
        listRow = [item for item in listRow if str(item) != 'nan']
        if isValidGroupRow(listRow) == False:
            continue
        if index == 0:
            myglobal.g_group_infos[myglobal.KEY_GROUP_FROM_FILENAMES] = listRow
        else:
            myglobal.g_group_infos[myglobal.KEY_GROUP_TO_FILENAMES] = listRow

def loadAllData(allFiles):
    listNecessary = [myglobal.REFER_FILE_NAME, myglobal.GROUP_FILE_NAME, myglobal.INPUT_DATA_FOLDER_NAME]
    for item in listNecessary:
        if item not in allFiles:
            exit("{} folder should contain {}.".format(myglobal.DATA_PATH, item))

    getAllInputDataInfo(myglobal.DATA_PATH + '/' + myglobal.INPUT_DATA_FOLDER_NAME)
    getReferenceInfo(myglobal.DATA_PATH + '/' + myglobal.REFER_FILE_NAME)
    getGroupInfo(myglobal.DATA_PATH + '/' + myglobal.GROUP_FILE_NAME)
