import glob
import xml.etree.ElementTree

def convertToJars(path):
    for file in glob.iglob(path+'\**\.classpath',recursive=True):
        data = xml.etree.ElementTree.parse(file)
        root = data.getroot()
        for classpathentry in root.findall('classpathentry'):
            if classpathentry.attrib['kind'] == 'src' and classpathentry.attrib['path'] != 'src' and 'cz' not in classpathentry.attrib['path']:
                classpathentry.set('kind','var')
                classpathentry.set('path','DIGX_LIB' + classpathentry.attrib['path'] + '.jar')
        data.write(file,xml_declaration=True)

def convertToSource(path):
    for file in glob.iglob(path+'\**\.classpath',recursive=True):
        data = xml.etree.ElementTree.parse(file)
        root = data.getroot()
        for classpathentry in root.findall('classpathentry'):
            if classpathentry.attrib['kind'] == 'var' and 'DIGX_LIB' in classpathentry.attrib['path']:
                classpathentry.set('kind','src')
                path = classpathentry.attrib['path'].replace('DIGX_LIB','').replace('.jar','')
                classpathentry.set('path',path)
        data.write(file, xml_declaration=True)



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'toJar':
        convertToJars(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == 'toSource':
        convertToSource(sys.argv[2])
    else:
        print('''options: 
        toJar <root_path_of_projects> - to convert from source to jar
        toSource <root_path_of_projects> - to convert from jar to source''')
