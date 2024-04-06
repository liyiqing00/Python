from xml.etree.ElementTree import *
tree=parse('P12-10.xml')
elem=tree.getroot()
filepath='tour.csv'
try:
    f=open(filepath,'w',encoding="utf-8")
except IOError:
    pass

def dump_node(node,values):
    if node.tag=='{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}KSN':
        if len(values.keys())==4:
            f.write(f"{values['KSN']},{values['PRC']},{values['AAC']},")
            f.write(f"{values['KSS']}\n")
        values={}
        values['KSN']=node.text
    elif node.tag=='{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}PRC':
        values['PRC']=node.text
    elif node.tag == '{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}AAC':
        values['AAC']=node.text
    elif node.tag == '{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}KSS':
        values['KSS']=node.text
    for child in node:
        values=dump_node(child,values)
    return(values)

values=dump_node(elem[1],{})
if len(values.keys())==4:
    print(values)
    f.write(f"{values['KSN']},{values['PRC']},{values['AAC']},")
    f.write(f"{values['KSS']}\n")
