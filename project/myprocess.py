import re
import myglobal
import myinitial

def getNewId():
    newId = "id_" + str(myglobal.g_id)
    myglobal.g_id += 1
    return newId


def preprocess():
    index = 0
    for item in myglobal.g_inputdata_infos:
        item[myglobal.KEY_INPUTDATA_TOP] = myglobal.CSV_TABLE_TOP
        item[myglobal.KEY_INPUTDATA_WIDTH] = myglobal.CSV_TABLE_WIDTH
        item[myglobal.KEY_INPUTDATA_HEIGHT] = myglobal.CSV_TABLE_ROWHEIGHT * (item[myglobal.KEY_INPUTDATA_HEADERSIZE] + 2) + 10

        listIds = []
        for x in range(item[myglobal.KEY_INPUTDATA_HEADERSIZE]):
            listIds.append(getNewId())
        item[myglobal.KEY_INPUTDATA_CSVIDS] = listIds
        myglobal.g_inputdata_infos[index] = item

        index += 1


def outputLine(fp, strLine):
    fp.write(strLine)
    fp.write("\n")

def isInReferTo(inputdata_info, x):
    toHeaderId = inputdata_info[myglobal.KEY_INPUTDATA_HEADERID] + str(x + 1)
    for refer_info in myglobal.g_refer_infos:
        if refer_info[myglobal.KEY_REFER_TO_HEADERID] == toHeaderId:
            return True
    return False

def getReferencedCSVIds(inputdata_info, x):
    result = []
    fromHeaderId = inputdata_info[myglobal.KEY_INPUTDATA_HEADERID] + str(x + 1)
    for refer_info in myglobal.g_refer_infos:
        if refer_info[myglobal.KEY_REFER_FROM_HEADERID] != fromHeaderId:
            continue
        to_filename = refer_info[myglobal.KEY_REFER_TO_FILENAME]
        to_headerid = refer_info[myglobal.KEY_REFER_TO_HEADERID]
        match = re.match(myglobal.REG_EXP, to_headerid, re.I)
        if match:
            items = match.groups()
            headerindex = int(items[1])
            target_inputdata_info = myinitial.find_inputdata(to_filename)
            refer_csvid = target_inputdata_info[myglobal.KEY_INPUTDATA_CSVIDS][headerindex - 1]
            result.append(refer_csvid)
    return result

def outputGroup(fp, groupId, filenames):
    tableLeft = myglobal.CSV_TABLE_LEFT
    for filename in filenames:
        inputdata_info = myinitial.find_inputdata(filename)
        headernames = inputdata_info[myglobal.KEY_INPUTDATA_HEADERNAMES]
        tableId = getNewId()
        strLine = "{},{},{},{},{},{},{},\"shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;align=center;resizeLast=1;fillColor=#dae8fc;gradientColor=#7ea6e0;fontStyle=1;\","\
            .format(tableId, inputdata_info[myglobal.KEY_INPUTDATA_FILENAME], groupId,
                    inputdata_info[myglobal.KEY_INPUTDATA_TOP], tableLeft,
                    inputdata_info[myglobal.KEY_INPUTDATA_WIDTH], inputdata_info[myglobal.KEY_INPUTDATA_HEIGHT])
        outputLine(fp, strLine)

        # table header
        theaderId = getNewId()
        strLine = "{},,{},,,,{},\"shape=tableRow;startSize=0;collapsible=0;top=0;bottom=0;\","\
            .format(theaderId, tableId, myglobal.CSV_TABLE_ROWHEIGHT)
        outputLine(fp, strLine)
        strLine = "{},ID,{},,,{},{},style1,"\
            .format(theaderId + "_1", theaderId, myglobal.CSV_TABLE_ID_WIDTH, myglobal.CSV_TABLE_ROWHEIGHT)
        outputLine(fp, strLine)
        strLine = "{},Header Name,{},,,{},{},style2," \
            .format(theaderId + "_2", theaderId, myglobal.CSV_TABLE_WIDTH - myglobal.CSV_TABLE_ID_WIDTH, myglobal.CSV_TABLE_ROWHEIGHT)
        outputLine(fp, strLine)
        # table header end

        # table content
        for x in range(inputdata_info[myglobal.KEY_INPUTDATA_HEADERSIZE]):
            style1 = "style3"
            style2 = "style4"
            csvId = inputdata_info[myglobal.KEY_INPUTDATA_CSVIDS][x]
            refer_csvids = getReferencedCSVIds(inputdata_info, x)
            if len(refer_csvids) == 0:
                strLine = "{},,{},,,,{},\"shape=tableRow;startSize=0;collapsible=0;top=0;bottom=0;\"," \
                    .format(csvId, tableId, myglobal.CSV_TABLE_ROWHEIGHT)
            else:
                strLine = "{},,{},,,,{},\"shape=tableRow;startSize=0;collapsible=0;top=0;bottom=0;\",\"{}\"" \
                    .format(csvId, tableId, myglobal.CSV_TABLE_ROWHEIGHT, ",".join(refer_csvids))
                style1 = "style5"
                style2 = "style6"
            outputLine(fp, strLine)
            if isInReferTo(inputdata_info, x):
                style1 = "style5"
                style2 = "style6"
            strLine = "{},{},{},,,{},{},{},"\
                .format(csvId + "_1", inputdata_info[myglobal.KEY_INPUTDATA_HEADERID] + str(x + 1), csvId,
                        myglobal.CSV_TABLE_ID_WIDTH, myglobal.CSV_TABLE_ROWHEIGHT, style1)
            outputLine(fp, strLine)
            strLine = "{},{},{},,,{},{},{},"\
                .format(csvId + "_2", headernames[x], csvId,
                        myglobal.CSV_TABLE_WIDTH - myglobal.CSV_TABLE_ID_WIDTH, myglobal.CSV_TABLE_ROWHEIGHT, style2)
            outputLine(fp, strLine)
        # table content end

        tableLeft += inputdata_info[myglobal.KEY_INPUTDATA_WIDTH] + myglobal.CSV_TABLE_GAP

def outputToCSV(fp):
    # From database
    fromFilenames = myglobal.g_group_infos[myglobal.KEY_GROUP_FROM_FILENAMES];
    count = len(fromFilenames)
    groupTop = myglobal.CSV_GROUP_TOP
    groupLeft = myglobal.CSV_GROUP_LEFT
    groupWidth = count * myglobal.CSV_TABLE_WIDTH + (count - 1) * myglobal.CSV_TABLE_GAP + 2 * myglobal.CSV_TABLE_LEFT
    groupHeight = 0
    for filename in fromFilenames:
        inputdata_info = myinitial.find_inputdata(filename)
        if groupHeight < inputdata_info[myglobal.KEY_INPUTDATA_HEIGHT]:
            groupHeight = inputdata_info[myglobal.KEY_INPUTDATA_HEIGHT]
    groupHeight += myglobal.CSV_TABLE_TOP + myglobal.CSV_TABLE_BOTTOM
    groupId = getNewId()

    strLine = "{},From Database,,{},{},{},{},\"swimlane;dashed=1;fillColor=#fff2cc;strokeColor=#d6b656;gradientColor=#ffd966;\","\
        .format(groupId, groupTop, groupLeft, groupWidth, groupHeight);
    outputLine(fp, strLine)

    outputGroup(fp, groupId, fromFilenames)
    # From database end

    # Calculation
    calcFilenames = myglobal.g_group_infos[myglobal.KEY_GROUP_TO_FILENAMES];
    count = len(calcFilenames)
    groupTop = myglobal.CSV_GROUP_TOP
    groupLeft += groupWidth + myglobal.CSV_TABLE_GAP
    groupWidth = count * myglobal.CSV_TABLE_WIDTH + (count - 1) * myglobal.CSV_TABLE_GAP + 2 * myglobal.CSV_TABLE_LEFT
    groupHeight = 0
    for filename in calcFilenames:
        inputdata_info = myinitial.find_inputdata(filename)
        if groupHeight < inputdata_info[myglobal.KEY_INPUTDATA_HEIGHT]:
            groupHeight = inputdata_info[myglobal.KEY_INPUTDATA_HEIGHT]
    groupHeight += myglobal.CSV_TABLE_TOP + myglobal.CSV_TABLE_BOTTOM
    groupId = getNewId()

    strLine = "{},Calculation,,{},{},{},{},\"swimlane;dashed=1;fillColor=#fff2cc;strokeColor=#d6b656;gradientColor=#ffd966;\"," \
        .format(groupId, groupTop, groupLeft, groupWidth, groupHeight);
    outputLine(fp, strLine)

    outputGroup(fp, groupId, calcFilenames)
    # Calculation


def createCSVForDrawio():
    preprocess()
    try:
        fp = open(myglobal.RESULT_CSV_FILE_NAME, "wt", encoding='utf-8')
        outputLine(fp, myglobal.g_csv_header)
        outputToCSV(fp)
    finally:
        fp.close()
