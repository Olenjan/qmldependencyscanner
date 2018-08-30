# qmldependencyscanner

QML Dependency scanner python script that scans all QML(.qml) files described in QT project(.qml)
for imports and Modules used.

All modules used by .qml are also scanned when found in same folder.
All imports are listed with version and whether or not they are found from --imports list of folders

When no --imports are provided, root folder of project provided is used.

usage: qmlprojectscanner.py [-h] [--imports [IMPORTS [IMPORTS ...]]]
                            inputProject

positional arguments:
    inputProject            Project to analyze

optional arguments:
    -h, --help              show this help message and exit
    --imports [IMPORTS [IMPORTS ...]]
                            List of QML import folders used for matching import
