import os
import sys
import ast
import re
import qmlscanfile
import argparse

def getDistFiles(content):
    distfileslines=[]
    for line in re.split('((?<!\\\\)\\n)', content):
        if 'DISTFILES' in line:
            prunedline = line.replace(' ', '').replace('\n', '').replace('\r', '')
            if prunedline[9:10] == '=':  # distfiles is overridden
                distfileslines = []
                distfileslines.append(prunedline[10:])
            elif prunedline[9:11] == '+=':
                distfileslines.append(prunedline[11:])
            else:
                print("Unknown 'DISTFILES' operator '%s'" % prunedline[9:11])
    result=[]
    for dl in distfileslines:
        result.extend(filter(None, dl.split('\\')))
    return list(set(result))

def getValidFiles(rootfolder: str, files: list) -> list:
    """
    returns list of paths that are files
    """
    result = []
    for currentfile in files:
        fullcurrentpath = rootfolder + "/" + currentfile
        if os.path.isfile(fullcurrentpath):
            result.append(fullcurrentpath)
        else:
           print("File '%s' not found." % fullcurrentpath)
    return result

def getLocalModuleFilepaths(rootfolder, modules):
    modulePaths = []
    for m in modules:
        path = ""
        desiredfile=m.lower() + ".qml"
        for file in os.listdir(rootfolder):
            if file.lower() == desiredfile:
                modulePaths.append({"name": m, "path": rootfolder + "/" + file})
                break
    return modulePaths

def checkLocalImports(importfolders, imports):
    """
    Dumb solution, check folder too many times, precollect list of existing modules
    """
    result=[]
    for i in imports:
        importdirname=i["name"].replace('.', '/')
        found = False
        for folder in importfolders:
            fulldirpath=os.path.join(folder, importdirname)
            if os.path.isdir(fulldirpath):
                result.append({"import": i, "exists": True})
                found = True
                break
        if found == False:
            result.append({"import": i, "exists": False})
    return result

    

class CQmlTraverser():
    def __init__(self, rootfolder, traversablefile, previouslyTraversed = list()):#, importfolders=list()):
        if traversablefile[-4:].lower() != ".qml":
            raise Exception("CQmlTraverser input file not '.qml'")
        self.traversablefile = traversablefile
        self.ImportDependencies = list()
        self.ModuleDependencies = list()
        self.previouslytraversedfiles=previouslyTraversed
        self.traversedfiles = list()
        #self.importfolders=importfolders
        self.rootfolder = rootfolder

    def traverse(self):
        #rint("Traversing %s" % self.traversablefile)
        with open(self.traversablefile, 'r') as file:
            data = file.read()
            qmlImports = qmlscanfile.getImports(data) 
            qmlModules = qmlscanfile.getModules(data)
            #print("Imports(%s): %s" % (len(qmlImports), qmlImports))
            #print("Modules(%s): %s" % (len(qmlModules), qmlModules))
            for m in qmlModules:
                if m not in self.ModuleDependencies:
                    self.ModuleDependencies.append(m)
            for i in qmlImports:
                if i not in self.ImportDependencies:
                    self.ImportDependencies.append(i)

        self.traversedfiles.append(self.traversablefile)     


        modulePaths = getLocalModuleFilepaths(self.rootfolder, self.ModuleDependencies)
        #print("LocalModulepaths: %s" % getLocalModuleFilepaths(rootfolder, self.ModuleDependencies))
        for m in modulePaths:
            if m["path"] not in self.traversedfiles and m["path"] not in self.previouslytraversedfiles:
                moduleTraverser = CQmlTraverser(self.rootfolder, m["path"], self.traversedfiles)#, self.importfolders)
                moduleTraverser.traverse()
                self.traversedfiles.extend(moduleTraverser.traversedfiles)
                for m in moduleTraverser.ModuleDependencies:
                    if m not in self.ModuleDependencies:
                        self.ModuleDependencies.append(m)
                for i in moduleTraverser.ImportDependencies:
                    if i not in self.ImportDependencies:
                        self.ImportDependencies.append(i)


"""
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
#[rootfolder , "/mnt/c/Qt/5.11.1/msvc2017_64/qml/"]
if args.imports:
    importFolderList = args.imports
else:
    importFolderList=list()
importFolderList.append(rootfolder)

print("Scanning: %s" % inputfilefullpath)
print("Import folders: %s" % importFolderList)
print("")

with open(inputfile, 'r') as file:
    content = file.read()
    files = getDistFiles(content)
    validFiles = getValidFiles(rootfolder, files)

    projectmoduledependencies = []
    projectimportdependencies = []

    for f in validFiles:
        if f[-4:] == ".qml":
            traverser = CQmlTraverser(rootfolder, f, list())#, importFileList)
            traverser.traverse()

            for m in traverser.ModuleDependencies:
                if m not in projectmoduledependencies:
                    projectmoduledependencies.append(m)
            for i in traverser.ImportDependencies:
                if i not in projectimportdependencies:
                    projectimportdependencies.append(i)

    imports = checkLocalImports(importFolderList, traverser.ImportDependencies)
    for i in imports:
        if i["exists"] == False:
            print("{: <20} {: <20} {: >1}".format(*[i["import"]["name"], i["import"]["version"], 'n']))
        else:
            print("{: <20} {: <20} {: >1}".format(*[i["import"]["name"],  i["import"]["version"], 'y']))
"""
