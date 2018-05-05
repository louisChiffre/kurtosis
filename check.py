from collections import namedtuple
import xml.etree.ElementTree as ET
from os.path import join, dirname

Block = namedtuple('Block', 'a b')

def node2block(node, begin_attr='d', end_attr='f'):
    dic = node.attrib
    return Block(
            a=int(dic[begin_attr]),
            b=int(dic[end_attr]))
    
    
def load(xml_filename):
    def mk_path(filename):
        return join(dirname(xml_filename), filename)

    def read_txt(filename):
        with open(filename,'r', encoding='latin9') as o:
            txt = o.read()
        return txt

    tree = ET.parse(xml_filename)
    transformations = tree.find('./informations/transformations')
    root = tree.getroot()
    informations = tree.find('./informations').attrib
    txt_1 = read_txt(mk_path(informations['fsource']))
    txt_2 = read_txt(mk_path(informations['fcible']))
    txt = txt_1 + txt_2

    def gen_blocks():
        for replacement in transformations.findall('./remplacements/remp')[0:10]:
            block = node2block(replacement)
            yield block

    def get_text(block):
        return txt[block.a:block.b]

    blocks = list(gen_blocks())
    assert len(blocks)%2 == 0
    N = len(blocks)//2
    for ba, bb in zip(blocks[:N], blocks[N:]):
        txt_a = get_text(ba)
        txt_b = get_text(bb)
        print(80*'-')
        print(repr(txt_a))
        print(repr(txt_b))
        
# to format the xml for readability
# xmllint --format samples/LaBelle/Informations.xml


# xml_filename = 'samples/Chedid/Informations.xml'
xml_filename = 'samples/LaBelle/Informations.xml'
load(xml_filename)
