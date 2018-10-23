import argparse
import qmldependencyscanner.qmlscanfile

def getModuleID(content):
    for line in content.splitlines():
        tmpqmlid = qmldependencyscanner.qmlscanfile.parseqmldirmoduleidline(line)
        if tmpqmlid is not None:
                return tmpqmlid
    return None
    

def getResourceID(content):
    """"returns list of {\"name\": name, \"version\": version}"""
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