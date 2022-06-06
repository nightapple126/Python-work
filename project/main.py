import os
import myglobal
import myinitial
import myprocess


if __name__ == '__main__':
    if os.path.isdir(myglobal.DATA_PATH) == False:
        exit("{} directory doesn't exist.".format(myglobal.DATA_PATH))
    allFiles = os.listdir(myglobal.DATA_PATH)
    myinitial.loadAllData(allFiles)
    myprocess.createCSVForDrawio()
    print("Converted successfully! Find the result.csv in Result folder.")
