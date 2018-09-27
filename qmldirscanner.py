import argparse
import qmldependencyscanner.qmlscanfile

def getModuleID(content):
    for line in content.splitlines():
        tmpqmlid = qmldependencyscanner.qmlscanfile.parseqmldirmoduleidline(line)
        if tmpqmlid is not None:
                return tmpqmlid
    return None
    

def getResourceID(content):
    result = []
    for line in content.splitlines():
        tmpresourec = qmldependencyscanner.qmlscanfile.parseqmldirresourceline(line)
        if tmpresourec is not None:
            result.append(tmpresourec)
    return result


def getPluginResource(content):
    result = []
    for line in content.splitlines():
        tmppluginrc = qmldependencyscanner.qmlscanfile.parseqmldirpluginline(line)
        if tmppluginrc is not None:
            result.append(tmppluginrc)
    return result


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

     


