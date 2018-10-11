
"""
for use via command line
prints list of imported modules found in qml tree
prints all except modules starting with "Qt"
"""


from qmldependencyscanner import *
import qmldependencyscanner.qmlscanfile
import qmldependencyscanner.qmltraverser
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

import_dependencies = []
module_dependencies = []

traverser = qmldependencyscanner.qmltraverser.CQmlTraverser(dir_path, "otioseMain.qml", list())
traverser.traverse()


for i in traverser.ImportDependencies:
	if i["name"][0:2] == "Qt":
		continue
	if i["name"] in built_in_imports:
		continue
	print(i["name"])