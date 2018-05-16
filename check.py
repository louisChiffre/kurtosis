from collections import namedtuple
from colorama import Fore, Back, Style
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

    Fragment = namedtuple('Fragment', 'left center right')
    def get_text(block, window=32):
        return Fragment(
            left = txt[(block.a-window):block.a],
            center = txt[block.a:block.b],
            right = txt[block.b:(block.b+window)])

    blocks = list(gen_blocks())
    assert len(blocks)%2 == 0
    N = len(blocks)//2
    Replacement = namedtuple('Replacement', 'source dest')
    for ba, bb in list(zip(blocks[:N], blocks[N:])):
        yield Replacement(get_text(ba), get_text(bb))
        
# xmllint --format samples/LaBelle/Informations.xml
xml_filename = 'samples/LaBelle/Informations.xml'
print(80*'*')
for rep in gen_replacements(xml_filename):
    left='{x.left}{code}{x.center}{reset}{x.right}'.format(x=rep.source, code=Fore.RED, reset=Style.RESET_ALL)
    right='{x.left}{code}{x.center}{reset}{x.right}'.format(x=rep.dest, code=Fore.GREEN, reset=Style.RESET_ALL)
    print('source'.center(80,'-'))
    print(left)
    print('cible'.center(80,'-'))
    print(right)
    print(80*'*')
    result = input('Change significant? [y/n]')
