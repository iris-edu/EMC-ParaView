#
# Description:
#     Convers a macro template to an actual macro ready for installation
# 
# History:
#
#   2018-03-21 Manoch: R.0.2018.080
#   2018-03-02 Manoch: created
#

import sys, os
import IrisEMC_Paraview_Param as param


def generatePythonMacroFromFiles(scriptFile, outputFile):
    
    fp = open(scriptFile,'r')
    data = fp.read()
    fp.close()

    for key in param.pathDict.keys():
       data = data.replace(key+'/',param.pathDict[key]+os.sep)
       data = data.replace(key,param.pathDict[key])

    fp = open(outputFile.replace('macro_',''), 'w')
    fp.write(data)
    fp.close()


def main():
    if len(sys.argv) != 3:
        print('Usage: %s <python input filename> <python output filename>' % sys.argv[0])
        sys.exit(1)

    inputScript = sys.argv[1]
    outputFile  = sys.argv[2]

    generatePythonMacroFromFiles(inputScript, outputFile)


if __name__ == '__main__':
    main()
