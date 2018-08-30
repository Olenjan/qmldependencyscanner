import argparse
from qmltraverser import *
import json

importFileList=[]
CLI=argparse.ArgumentParser()
CLI.add_argument("inputmetadata", type=str,
                    help="CB Application metadata to analyze")
CLI.add_argument("--imports",
                    help="",
                    nargs="*",
                    type=str
                                                                )
args = CLI.parse_args()

if not args.inputmetadata:
    print("No input metadata(.json) specified!")
    raise SystemExit

inputfile=args.inputmetadata
metadatafilefullpath = os.path.realpath(inputfile)
rootfolder=os.path.dirname((metadatafilefullpath))
if args.imports:
    importFolderList = args.imports
else:
    importFolderList=list()
    importFolderList.append(rootfolder)

#print("Metadata form file: %s" % metadatafilefullpath)
#print("Import folders: %s" % importFolderList)
#print("")

with open(inputfile, 'r') as file:
    metadata=json.load(file)
    
    validFiles=[]

    if "viewFile" in metadata and \
        "name" in metadata and \
        "viewFile" in metadata:
        id = metadata["id"]
        name = metadata["name"]
        viewFile = metadata["viewFile"]
        print("CB Application '%s(%s)'" % (name, id))
        if viewFile[0] == '/':
            validFiles.append(viewFile)
        else:
            validFiles.append(rootfolder + "/" + viewFile )

    #print("QML files to scan: %s" % validFiles)

    moduledependencies = []
    importdependencies = []

    for f in validFiles:
        if f[-4:] == ".qml":
            traverser = CQmlTraverser(rootfolder, f, list())
            traverser.traverse()

            for m in traverser.ModuleDependencies:
                if m not in moduledependencies:
                    moduledependencies.append(m)
            for i in traverser.ImportDependencies:
                if i not in importdependencies:
                    importdependencies.append(i)

    print("---------------------------------------------------")
    print("----------------------Imports----------------------")

    imports = checkLocalImports(importFolderList, importdependencies)
    print("{: <20} {: <20} {: >3}".format(*["name", "version", "y|n"]))
    for i in imports:
        if i["exists"] == False:
            print("{: <20} {: <20} {: >1}".format(*[i["import"]["name"], i["import"]["version"], 'n']))
        else:
            print("{: <20} {: <20} {: >1}".format(*[i["import"]["name"],  i["import"]["version"], 'y']))

    print("---------------------------------------------------")
    print("----------------------Modules----------------------")
    for m in moduledependencies:
        print(m)
    print("---------------------------------------------------")
    print("---------------------------------------------------")
