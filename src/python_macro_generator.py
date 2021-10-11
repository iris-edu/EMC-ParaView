import sys, os
import IrisEMC_Paraview_Param as param

"""
 Description:
     Converts a macro template to an actual macro ready for installation

 History:
   2021-10-03 Manoch: v.2021.276 Python 3 release r2
   2018-03-21 Manoch: v.2018.080
   2018-03-02 Manoch: created

"""


def generatePythonMacroFromFiles(scriptFile, outputFile):
    fp = open(scriptFile, 'r')
    data = fp.read()
    fp.close()

    for key in list(param.pathDict.keys()):
        data = data.replace(key + '/', param.pathDict[key] + os.sep)
        data = data.replace(key, param.pathDict[key])

    fp = open(outputFile.replace('macro_', ''), 'w')
    fp.write(data)
    fp.close()


def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <python input filename> <python output filename>')
        sys.exit(1)

    inputScript = sys.argv[1]
    outputFile = sys.argv[2]

    generatePythonMacroFromFiles(inputScript, outputFile)


if __name__ == '__main__':
    main()
