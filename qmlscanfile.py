import os
import sys
from pyparsing import *
import re

def getModules(data):
    modules = []
    expr = Forward()
    expr << Word(alphas.upper(), alphanums) + Literal('{').suppress() + Optional(Word(alphanums) + expr) | expr + Literal('}').suppress()
    for tplt in expr.searchString(data):
        modules.append(tplt[0])
    return modules

def parseqmldirresourceline(line):
    requery = "(([^\s]+) ([-+]?[0-9]*\.?[0-9]*)) ([^\s]+)+[.qml]"

    matched = re.match(requery, line)

    if matched == None:
        return None

    name = matched.groups(0)[1]
    version = matched.groups(1)[2]
    return {
        "name": name,
        "version": version,
    }

	
def parseqmldirpluginline(line):
    requery = "plugin ([^\s]+)"

    matched = re.match(requery, line)

    if matched == None:
        return None

    name = matched.groups(0)[0]
    return {"plugin": name}

	
def parseqmldirmoduleidline(line):
    requery = "module ([^\s]+)"

    matched = re.match(requery, line)

    if matched == None:
        return None

    name = matched.groups(0)[0]
    return {"name": name}

def parseqmldirpluginline(line):
    requery = "plugin ([^\s]+)"

    matched = re.match(requery, line)

    if matched == None:
        return None

    name = matched.groups(0)[0]
    return {"plugin": name}



def parseimportline(line):
    # Splits into import <Module> <version> | as <alias>
    splitLine = re.sub(' +',' ', line).split(' ')

    if len(splitLine) < 3:
        raise Exception("Import line '%s' Does not have version" % line)

    return {"name": splitLine[1], "version": splitLine[2]}

def getImports(data):
    importlines = []
    for line in data.split("\n"):
        if 'import' in line:
            prunedline = parseimportline(line.strip())
            importlines.append(prunedline)
    return importlines
        
