"""
for use via command line
prints list of imported modules found in qml tree
prints all except modules starting with "Qt"
"""


import qmlscanfile
import qmltraverser
import os 
import sys

dir_path = os.path.dirname(os.path.realpath(sys.argv[1]))

built_in_imports = []
import_dependencies = []
module_dependencies = []

print("Parsing: %s" % sys.argv[1])
traverser = qmltraverser.CQmlTraverser(dir_path, sys.argv[1], list())
traverser.traverse()

for i in traverser.ImportDependencies:
	if i["name"][0:2] == "Qt":
		continue
	if i["name"] in built_in_imports:
		continue
	print(i["name"])