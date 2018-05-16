from collections import namedtuple
import xml.etree.ElementTree as ET
from os.path import join, dirname

Block = namedtuple('Block', 'a b')

def node2block(node, begin_attr='d', end_attr='f'):
    dic = node.attrib
    return Block(
            a=int(dic[begin_attr]),
            b=int(dic[end_attr]))
    
    
def gen_replacements(xml_filename):
    def mk_path(filename):
        return join(dirname(xml_filename), filename)

    def read_txt(filename):
        encoding = 'latin1'
        # if '01LaBelle' in filename:
        #     encoding = 'utf16'
        with open(filename,'r', encoding=encoding) as o:
            txt = o.read()
        return txt

    tree = ET.parse(xml_filename)
    transformations = tree.find('./informations/transformations')
    root = tree.getroot()
    informations = tree.find('./informations').attrib
    txt_1 = read_txt(mk_path(informations['fsource']))
    txt_2 = read_txt(mk_path(informations['fcible']))
    txt = txt_1 + txt_2
    pivot = int(tree.find('./informations/transformations/lgsource').attrib['lg'])

    def gen_blocks(block_type='./remplacements/remp'):
        for replacement in transformations.findall(block_type):
            block = node2block(replacement)
            yield block

    def get_text(block):
        return txt[block.a:block.b]

    blocks = list(gen_blocks())
    assert len(blocks)%2 == 0
    N = len(blocks)//2
    Replacement = namedtuple('Replacement', 'source dest')
    for ba, bb in list(zip(blocks[:N], blocks[N:])):
        yield Replacement(get_text(ba), get_text(bb))
        
# xmllint --format samples/LaBelle/Informations.xml
xml_filename = 'samples/LaBelle/Informations.xml'
for rep in gen_replacements(xml_filename):
    print(80*'-')
    print('{rep.source}'.format(**locals()))
    print('{rep.dest}'.format(**locals()))

