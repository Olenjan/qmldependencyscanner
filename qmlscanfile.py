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
        
