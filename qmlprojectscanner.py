import argparse
from qmltraverser import *

inputfile = sys.argv[1]
importFileList=[]
CLI=argparse.ArgumentParser()
CLI.add_argument("inputProject", type=str,
                    help="Project to analyze")
CLI.add_argument(
                "--imports",  # name on the CLI - drop the `--` for positional/required parameters
                                nargs="*",  # 0 or more values expected => creates a list
                                                type=str#,
                                                                )
args = CLI.parse_args()

if not args.inputProject:
    print("No input project(.pro) specified!")
    raise SystemExit

inputfilefullpath = os.path.realpath(args.inputProject)#inputfile)
rootfolder=os.path.dirname((inputfilefullpath))

if args.imports:
    importFolderList = args.imports
else:
    importFolderList=list()
    importFolderList.append(rootfolder)

with open(inputfile, 'r') as file:
    content = file.read()
    files = getDistFiles(content)
    validFiles = getValidFiles(rootfolder, files)

    moduledependencies = []
    importdependencies = []

    for f in validFiles:
        if f[-4:] == ".qml":
            traverser = CQmlTraverser(rootfolder, f, list())#, importFileList)
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
