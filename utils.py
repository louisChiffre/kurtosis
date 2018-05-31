import io
from collections import namedtuple
import xml.etree.ElementTree as ET
from os.path import join, dirname,exists

Block = namedtuple('Block', 'a b node')

def node2block(node, begin_attr='d', end_attr='f'):
    dic = node.attrib
    return Block(
            a=int(dic[begin_attr]),
            b=int(dic[end_attr]),
            node=node)

def mk_path(xml_filename, filename):
    return join(dirname(xml_filename), filename)

def read_txt(filename, encoding):
    with io.open(filename,'r', encoding=encoding) as o:
        txt = o.read()
    return txt

def read_xml(xml_filename):
    tree = ET.parse(xml_filename)
    return tree

def get_replacements(xml_filename, encoding):
    tree = read_xml(xml_filename)
    transformations = tree.find('./informations/transformations')
    root = tree.getroot()
    informations = tree.find('./informations').attrib
    txt_1 = read_txt(mk_path(xml_filename, informations['fsource']), encoding)
    txt_2 = read_txt(mk_path(xml_filename, informations['fcible']), encoding)
    txt = txt_1 + txt_2
    pivot = int(tree.find('./informations/transformations/lgsource').attrib['lg'])

    def gen_blocks(block_type='./remplacements/remp'):
        for replacement in transformations.findall(block_type):
            block = node2block(replacement)
            yield block

    Fragment = namedtuple('Fragment', 'left center right block')
    def p(x):
        return x
    def get_text(block, window=32):
        return Fragment(
            left = p(txt[(block.a-window):block.a]),
            center = p(txt[block.a:block.b]),
            right = p(txt[block.b:(block.b+window)]),
            block = block)

    blocks = list(gen_blocks())
    assert len(blocks)%2 == 0
    N = len(blocks)//2
    Replacement = namedtuple('Replacement', 'source dest')
    def gen_replacements():
        for ba, bb in list(zip(blocks[:N], blocks[N:])):
            yield Replacement(get_text(ba), get_text(bb))
    return tree, list(gen_replacements())

