import os
import sys
import inspect
import textwrap
import IrisEMC_Paraview_Param as param
"""

 Credits:

  Credit for this code goes to Bane Sullivan (http://banesullivan.com/)
  the code was obtained from:
       https://github.com/banesullivan/ParaViewGeophysics

  The original code was modified based on the IRIS EMC ParaView requirements

 From the original code:

     See blog for details: 
     https://blog.kitware.com/easy-customization-of-the-paraview-python-programmable-filter-property-panel/
     This code has been heavily modified by Bane Sullivan (banesullivan@gmail.com) for making customized filters in 
     the geoscience data visualization. Credit does not go to Bane for this script but to the author of the above 
     blog post.
     Acknowledgements:
         Daan van Vugt <daanvanvugt@gmail.com> for file series implementation
             https://github.com/Exteris/paraview-python-file-reader
         Pat Marion (see blog post url above) for the foundation of this script

 History:
   2021-10-03 Manoch: v.2021.276 Python 3 release r2
   2019-01-14 Manoch: V.2019.014 support for volcano data from EMC file repository
   2018-03-21 Manoch: V.2018.080
   2018-02-28 Manoch: adopted to EMC ParaView support and added option of replacing keyword in the XML body 
                      before writing it to the file
   2018-01-20 Manoch: original code by Bane Sullivan from https://github.com/banesullivan/ParaViewGeophysics

"""



def escapeForXmlAttribute(s):

    # http://www.w3.org/TR/2000/WD-xml-c14n-20000119.html#charescaping
    # In character data and attribute values, the character information items "<" and "&" are represented by "&lt;" and "&amp;" respectively.
    # In attribute values, the double-quote character information item (") is represented by "&quot;".
    # In attribute values, the character information items TAB (#x9), newline (#xA), and carriage-return (#xD) are represented by "&#x9;", "&#xA;", and "&#xD;" respectively.

    s = s.replace('&', '&amp;') # Must be done first!
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    s = s.replace('\r', '&#xD;')
    s = s.replace('\n', '&#xA;')
    s = s.replace('\t', '&#x9;')
    return s



def getScriptPropertiesXml(info):

    e = escapeForXmlAttribute

    requestData = e(info['RequestData'])
    requestInformation = e(info['RequestInformation'])
    requestUpdateExtent = e(info['RequestUpdateExtent'])

    if requestData:
        requestData = f'''
      <StringVectorProperty
        name="Script"
        command="SetScript"
        number_of_elements="1"
        default_values="{requestData}"
        panel_visibility="advanced">
        <Hints>
         <Widget type="multi_line" syntax="python"/>
       </Hints>
      <Documentation>This property contains the text of a python program that
      the programmable source runs.</Documentation>
      </StringVectorProperty>'''

    if requestInformation:
        requestInformation = f'''
      <StringVectorProperty
        name="InformationScript"
        label="RequestInformation Script"
        command="SetInformationScript"
        number_of_elements="1"
        default_values="{requestInformation}"
        panel_visibility="advanced">
        <Hints>
          <Widget type="multi_line" syntax="python"/>
        </Hints>
        <Documentation>This property is a python script that is executed during
        the RequestInformation pipeline pass. Use this to provide information
        such as WHOLE_EXTENT to the pipeline downstream.</Documentation>
      </StringVectorProperty>'''

    if requestUpdateExtent:
        requestUpdateExtent = f'''
        <StringVectorProperty
          name="UpdateExtentScript"
          label="RequestUpdateExtent Script"
          command="SetUpdateExtentScript"
          number_of_elements="1"
          default_values="{requestUpdateExtent}"
          panel_visibility="advanced">
          <Hints>
            <Widget type="multi_line" syntax="python"/>
          </Hints>
          <Documentation>This property is a python script that is executed during
          the RequestUpdateExtent pipeline pass. Use this to modify the update
          extent that your filter ask up stream for.</Documentation>
        </StringVectorProperty>'''

    return '\n'.join([requestData, requestInformation, requestUpdateExtent])



def getPythonPathProperty():
    return '''
      <StringVectorProperty command="SetPythonPath"
                            name="PythonPath"
                            number_of_elements="1"
                            panel_visibility="advanced">
        <Documentation>A semi-colon (;) separated list of directories to add to
        the python library search path.</Documentation>
      </StringVectorProperty>'''



def getFilterPropertyXml(propertyInfo, propertyName, propertyHelpInfo):

    vis = 'default'
    if 'HIDE' in propertyName:
        vis = 'advanced'

    propertyHelp = propertyHelpInfo.get(propertyName, '')

    e = escapeForXmlAttribute

    propertyValue = propertyInfo[propertyName]
    propertyName = propertyName.replace('_HIDE_', '')
    propertyName = propertyName.replace('_HIDE', '')
    propertyName = propertyName.replace('HIDE_', '')
    propertyName = propertyName.replace('HIDE', '')
    propertyLabel = propertyName.replace('_', ' ')

    if isinstance(propertyValue, list):
        numberOfElements = len(propertyValue)
        assert numberOfElements > 0
        propertyType = type(propertyValue[0])
        defaultValues = ' '.join([str(v) for v in propertyValue])
    else:
        numberOfElements = 1
        propertyType = type(propertyValue)
        defaultValues = str(propertyValue)

    if propertyType is bool:

        defaultValues = defaultValues.replace('True', '1').replace('False', '0')

        return f'''
      <IntVectorProperty
        panel_visibility="{vis}"
        name="{propertyName}"
        label="{propertyLabel}"
        initial_string="{propertyName}"
        command="SetParameter"
        animateable="1"
        default_values="{defaultValues}"
        number_of_elements="{numberOfElements}">
        <BooleanDomain name="bool" />
        <Documentation>{propertyHelp}</Documentation>
      </IntVectorProperty>'''


    if propertyType is int:
        return f'''
      <IntVectorProperty
        panel_visibility="{vis}"
        name="{propertyName}"
        label="{propertyLabel}"
        initial_string="{propertyName}"
        command="SetParameter"
        animateable="1"
        default_values="{defaultValues}"
        number_of_elements="{numberOfElements}">
        <Documentation>{propertyHelp}</Documentation>
      </IntVectorProperty>'''

    if propertyType is float:
        return f'''
      <DoubleVectorProperty
        panel_visibility="{vis}"
        name="{propertyName}"
        label="{propertyLabel}"
        initial_string="{propertyName}"
        command="SetParameter"
        animateable="1"
        default_values="{defaultValues}"
        number_of_elements="{numberOfElements}">
        <Documentation>{propertyHelp}</Documentation>
      </DoubleVectorProperty>'''

    if propertyType is str:
        if 'FileName' in propertyName:
            return f'''
          <StringVectorProperty
            panel_visibility="{vis}"
            name="{propertyName}"
            label="{propertyLabel}"
            initial_string="{propertyName}"
            command="SetParameter"
            animateable="1"
            default_values="{defaultValues}"
            number_of_elements="{numberOfElements}">
            <FileListDomain name="files"/>
            <Documentation>{propertyHelp}</Documentation>
          </StringVectorProperty>'''
        else:
            return f'''
            <StringVectorProperty
            panel_visibility="{vis}"
            name="{propertyName}"
            label="{propertyLabel}"
            initial_string="{propertyName}"
            command="SetParameter"
            animateable="1"
            default_values="{defaultValues}"
            number_of_elements="{numberOfElements}">
            <Documentation>{propertyHelp}</Documentation>
            </StringVectorProperty>'''

    raise Exception('Unknown property type: %r' % propertyType)


def getFilterPropertiesXml(info):

    propertyInfo = info['Properties']
    propertyHelpInfo = info.get('PropertiesHelp', {})
    xml = [getFilterPropertyXml(propertyInfo, name, propertyHelpInfo) for name in sorted(propertyInfo.keys())]
    return '\n\n'.join(xml)


def getNumberOfInputs(info):
    return info.get('NumberOfInputs', 1)


def getInputPropertyXml(info):

    numberOfInputs = getNumberOfInputs(info)
    if not numberOfInputs:
        return ''


    inputDataType = info.get('InputDataType', 'vtkDataObject')

    inputDataTypeDomain = ''
    if inputDataType:
        inputDataTypeDomain = f'''
          <DataTypeDomain name="input_type">
            <DataType value="{inputDataType}"/>
          </DataTypeDomain>'''

    inputPropertyAttributes = 'command="SetInputConnection"'
    if numberOfInputs > 1:
        inputPropertyAttributes = '''\
            clean_command="RemoveAllInputs"
            command="AddInputConnection"
            multiple_input="1"'''

    inputPropertyXml = f'''
      <InputProperty
        name="Input"
        {inputPropertyAttributes}>
          <ProxyGroupDomain name="groups">
            <Group name="sources"/>
            <Group name="filters"/>
          </ProxyGroupDomain>
          {inputDataTypeDomain}
      </InputProperty>'''

    return inputPropertyXml


def getOutputDataSetTypeXml(info):


    outputDataType = info.get('OutputDataType', '')

    # these values come from vtkType.h in VTK Code Base
    typeMap = {
        '': 8, # same as input
        'vtkPolyData': 0,
        'vtkStructuredPoints': 1,
        'vtkStructuredGrid': 2,
        'vtkRectilinearGrid': 3,
        'vtkUnstructuredGrid': 4,
        'vtkPiecewiseFunction': 5,
        'vtkImageData': 6,
        'vtkDataObject': 7,
        'vtkPointSet': 9,
        'vtkUniformGrid': 10,
        'vtkCompositeDataSet': 11,
        #'vtkMultiGroupDataSet': 12, # obsolete
        'vtkMultiBlockDataSet': 13,
        #'vtkHierarchicalDataSet': 14, # obsolete
        #'vtkHierarchicalBoxDataSet': 15, # obsolete
        # 'vtkGenericDataSet': 16, # obsolete
        'vtkHyperOctree': 17,
        #'vtkTemporalDataSet': 18, # obsolete
        'vtkTable': 19,
        'vtkGraph': 20,
        'vtkTree': 21
    }

    typeValue = typeMap[outputDataType]

    return f'''
      <!-- Output data type: "{outputDataType}  or 'Same as input'" -->
      <IntVectorProperty command="SetOutputDataSetType"
                         default_values="{typeValue}"
                         name="OutputDataSetType"
                         number_of_elements="1"
                         panel_visibility="never">
        <Documentation>The value of this property determines the dataset type
        for the output of the programmable filter.</Documentation>
      </IntVectorProperty>'''


def getProxyGroup(info):
    if "Group" not in info:
        return 'sources' if getNumberOfInputs(info) == 0 else 'filters'
    else:
        return info["Group"]


def generatePythonFilter(info):
    e = escapeForXmlAttribute

    proxyName = info['Name']
    proxyLabel = info['Label']
    shortHelp = e(info['Help'])
    longHelp = e(info['Help'])
    extraXml = info.get('ExtraXml', '')

    proxyGroup = getProxyGroup(info)
    inputPropertyXml = getInputPropertyXml(info)
    outputDataSetType = getOutputDataSetTypeXml(info)
    scriptProperties = getScriptPropertiesXml(info)
    filterProperties = getFilterPropertiesXml(info)
    filterGroup = getFilterGroup(info)


    outputXml = f'''\
<ServerManagerConfiguration>
  <ProxyGroup name="{proxyGroup}">
    <SourceProxy name="{proxyName}" class="vtkPythonProgrammableFilter" label="{proxyLabel}">
      <Documentation
        long_help="{longHelp}"
        short_help="{shortHelp}">
      </Documentation>
{filterGroup}
{extraXml}
{inputPropertyXml}
{filterProperties}
{outputDataSetType}
{scriptProperties}
    </SourceProxy>
 </ProxyGroup>
</ServerManagerConfiguration>
      '''
    return textwrap.dedent(outputXml)


def getFilterGroup(info):
    if "FilterCategory" not in info:
        return ''
    else:
        return (f'''\
        <Hints>
            <ShowInMenu category="{info['FilterCategory']}" />
        </Hints>
        ''')


def replaceFunctionWithSourceString(namespace, functionName, allowEmpty=False):

    func = namespace.get(functionName)
    if not func:
        if allowEmpty:
            namespace[functionName] = ''
            return
        else:
            raise Exception(f'Function {functionName} not found in input source code.')

    if not inspect.isfunction(func):
        raise Exception(f'Object {functionName} is not a function object.')

    lines = inspect.getsourcelines(func)[0]

    if len(lines) <= 1:
        raise Exception(f'Function {functionName} must not be a single line of code.')

    # skip first line (the declaration) and then dedent the source code
    sourceCode = textwrap.dedent(''.join(lines[1:]))

    namespace[functionName] = sourceCode


def generatePythonFilterFromFiles(scriptFile, outputFile):
    
    namespace = {}
    exec(compile(open(scriptFile, "rb").read(), scriptFile, 'exec'), namespace)

    replaceFunctionWithSourceString(namespace, 'RequestData')
    replaceFunctionWithSourceString(namespace, 'RequestInformation', allowEmpty=True)
    replaceFunctionWithSourceString(namespace, 'RequestUpdateExtent', allowEmpty=True)

    usgsDropDownItems = ""
    for i in range(len(param.usgsSlabKeys)):
        usgsDropDownItems += '<Entry value="%i" text="%s"/>\n' % (i, param.usgsSlabValues[i])

    earthquakeDropDownItems = ""
    for i in range(len(param.earthquakeKeys)):
        earthquakeDropDownItems += '<Entry value="%i" text="%s"/>\n' % (i, param.earthquakeValues[i])

    boundaryDropDownItems = ""
    for i in range(len(param.boundaryKeys)):
        boundaryDropDownItems += '<Entry value="%i" text="%s"/>\n' % (i, param.boundaryValues[i])

    topoDropDownItems = ""
    for i in range(len(param.topoKeys)):
        topoDropDownItems += f'<Entry value="{i}" text="{param.topoValues[i]}/>\n'

    areaDropDownItems = ""
    for i in range(len(param.areaKeys)):
        areaDropDownItems += f'<Entry value="{i}" text="{param.areaValues[i]}"/>\n'

    xmlOutput = generatePythonFilter(namespace)
    for key in list(param.pathDict.keys()):
       xmlOutput = xmlOutput.replace(key+'/',param.pathDict[key]+os.sep)
       xmlOutput = xmlOutput.replace(key,param.pathDict[key])
    for key in list(param.filesDict.keys()):
       xmlOutput = xmlOutput.replace(key+'/',param.filesDict[key]+os.sep)
       xmlOutput = xmlOutput.replace(key,param.filesDict[key])

    if 'USGS_SLAB_DROP_DOWN' in xmlOutput:
        xmlOutput = xmlOutput.replace('USGS_SLAB_DROP_DOWN', usgsDropDownItems)
     
    if 'EARTHQUAKE_DROP_DOWN' in xmlOutput:
        xmlOutput = xmlOutput.replace('EARTHQUAKE_DROP_DOWN', earthquakeDropDownItems)

    if 'BOUNDARY_DROP_DOWN' in xmlOutput:
        xmlOutput = xmlOutput.replace('BOUNDARY_DROP_DOWN', boundaryDropDownItems)

    if 'TOPO_DROP_DOWN' in xmlOutput:
        xmlOutput = xmlOutput.replace('TOPO_DROP_DOWN', topoDropDownItems)

    if 'AREA_DROP_DOWN' in xmlOutput:
        xmlOutput = xmlOutput.replace('AREA_DROP_DOWN', areaDropDownItems)

    for key in list(param.filesDict.keys()):
        xmlOutput = xmlOutput.replace(key,param.filesDict[key])

    open(outputFile, 'w').write(xmlOutput)


def main():

    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <python input filename> <xml output filename>')
        sys.exit(1)

    inputScript = sys.argv[1]
    outputFile = sys.argv[2]

    generatePythonFilterFromFiles(inputScript, outputFile)


if __name__ == '__main__':
    main()
