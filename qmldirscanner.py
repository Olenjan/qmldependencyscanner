import argparse
import qmlscanfile

def getModuleID(content):
    for line in content.splitlines():
        tmpqmlid = qmlscanfile.parseqmldirmoduleidline(line)
        if tmpqmlid is not None:
                return tmpqmlid
    return None
    

def getResourceID(content):
    for line in content.splitlines():
        print("getting resource from line: %s" % line)
        tmpresourec = qmlscanfile.parseqmldirresourceline(line)
        if tmpresourec is not None:
            return tmpresourec
    return None


importFileList=[]
CLI=argparse.ArgumentParser()
CLI.add_argument("qmldir", type=str,
                    help="qmldir to analyze")
CLI.add_argument("--imports",
                    help="List of QML import folders used for matching imports",
                    nargs="*",
                    type=str)

args = CLI.parse_args()
inputfile=args.qmldir

with open(inputfile, 'r') as file:
    content = file.read()
    moduleName = ""
    moduleID = getModuleID(content)
    resourceIDs = getResourceID(content)

    print(moduleID)
    print(resourceIDs)

     


