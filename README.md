# qmldependencyscanner

QML Dependency scanner python script that scans all QML(.qml) files described in QT project(.qml)
for imports and Modules used.

All modules used by .qml are also scanned when found in same folder.
All imports are listed with version and whether or not they are found from --imports list of folders

When no --imports are provided, root folder of project provided is used.

# Python Dependencies

## qmlprojectscanner.py
os
sys
ast
re
argparse
pyparsing

## cbmetadatascanner.py
os
sys
ast
re
argparse
pyparsing
json



# Usage
usage: qmlprojectscanner.py [-h] [--imports [IMPORTS [IMPORTS ...]]]
                            inputProject

positional arguments:
    inputProject            Project to analyze

optional arguments:
    -h, --help              show this help message and exit
    --imports [IMPORTS [IMPORTS ...]]
                            List of QML import folders used for matching import
                            
Note: Relative and absolute paths can be used.

# Example

python3 qmlprojectscanner.py /Path/To/project.pro --imports /Path/To/Qt/5.11.1/qml/

## Example output
```
File '/Path/To/project/nonexistant.qml' not found.
---------------------------------------------------
----------------------Imports----------------------
name                 version              y|n
QtQuick              2.0                  y
Qt.labs.settings     1.0                  y
QtGraphicalEffects   1.0                  y
QtQuick              2.11                 y
SomeRandomModule     1.0                  n
NonExisting          13.37                n
OtherNonExisting     37.13                n
---------------------------------------------------
----------------------Modules----------------------
Setting
Rectangle
Image
Text
Row
Repeater
SomeMyModule
SomeMyModule2
Grid
TextMetrics
GamePad
MouseArea
---------------------------------------------------
---------------------------------------------------
```

line ```File '/Path/To/project/nonexistant.qml' not found.``` shows that one file included in project does not exist.
All files not found are presented before scanning
