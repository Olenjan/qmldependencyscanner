import re
import os
import chardet

#Hardcoded temporarily
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plugins.types")

def getRegisteredImports(data):
    """"returns list of {\"name\": name, \"version\": version}"""
    # do magic

    import_result = []

    # encoding
    encoding_info = chardet.detect(data)
    data = data.decode('%s' % encoding_info['encoding'])

    # cleanup
    data = data.strip()

    # analyze
    re_pattern = r'exports: \[(\".*\")]' # must be stripped format
    re_results = re.findall(re_pattern, data)

    # print
    for import_statement in re_results:
        split_import = import_statement.replace("\"", "").split(" ")

        #create object
        o = {
                "name": split_import[0],
                "version": split_import[1]
            }
        import_result.append(o)

    if len(import_result) == 0:
        return None

    return import_result
