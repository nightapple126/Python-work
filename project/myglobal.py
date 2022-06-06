# define all constants
DATA_PATH = './Data'
REFER_FILE_NAME = 'ReferenceTable.xlsx'
GROUP_FILE_NAME = 'GroupTable.xlsx'
INPUT_DATA_FOLDER_NAME = 'InputTable'
RESULT_CSV_FILE_NAME = './Result/result.csv'

KEY_INPUTDATA_FILENAME = "ki_filename"
KEY_INPUTDATA_HEADERID = "ki_headerid"
KEY_INPUTDATA_HEADERSIZE = "ki_headersize"
KEY_INPUTDATA_HEADERNAMES = "ki_headernames"
# to output
KEY_INPUTDATA_CSVIDS = "ki_csvids"
KEY_INPUTDATA_TOP = "ki_top"
KEY_INPUTDATA_WIDTH = "ki_width"
KEY_INPUTDATA_HEIGHT = "ki_height"
# to output end

KEY_REFER_FROM_FILENAME = "kr_from_filename"
KEY_REFER_FROM_HEADERID = "kr_from_headerid"
KEY_REFER_FROM_HEADERNAME = "kr_from_headername"
KEY_REFER_TO_FILENAME = "kr_to_filename"
KEY_REFER_TO_HEADERID = "kr_to_headerid"
KEY_REFER_TO_HEADERNAME = "kr_to_headername"

KEY_GROUP_FROM_FILENAMES = "kg_from_filenames"
KEY_GROUP_TO_FILENAMES = "kg_to_filenames"

REG_EXP = r"([a-z]+)([0-9]+)"

CSV_GROUP_TOP = 30
CSV_GROUP_LEFT = 30
CSV_TABLE_WIDTH = 240
CSV_TABLE_TOP = 50
CSV_TABLE_BOTTOM = 20
CSV_TABLE_LEFT = 30
CSV_TABLE_GAP = 50
CSV_TABLE_ROWHEIGHT = 30
CSV_TABLE_ID_WIDTH = 50
# define all constants end

# global variables
g_inputdata_infos = []
g_refer_infos = []
g_group_infos = {}

g_csv_header = """# identity: id
# parent: parent
# label: %name%
# styles: {"style1": "shape=partialRectangle;fontStyle=1;right=0;", "style2": "shape=partialRectangle;align=left;spacingLeft=6;fontStyle=5;", "style3": "shape=partialRectangle;top=0;bottom=0;right=0;", "style4": "shape=partialRectangle;align=left;spacingLeft=6;top=0;bottom=0;", "style5": "shape=partialRectangle;top=0;bottom=0;right=0;fontColor=red;", "style6": "shape=partialRectangle;align=left;spacingLeft=6;top=0;bottom=0;fontColor=red;"}
# stylename: shapes
# style: %shapes%
# parentstyle: %shapes%
# connect: {"from": "ref", "to": "id", "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"}
# top: top
# left: left
# width: @width
# height: @height
# ignore: parent, top, left, width, height, ref
id,name,parent,top,left,width,height,shapes,ref\n"""

g_id = 1

# global variables end
