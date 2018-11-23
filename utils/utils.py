# -*- coding: utf-8 -*-
import io
from collections import namedtuple
import xml.etree.ElementTree as ET
from os.path import join, dirname

Block = namedtuple('Block', 'a b node')
REPLACEMENT = 'REPLACEMENT'
INSERTION = 'INSERTION'
DELETION = 'DELETION'
MOVE = 'MOVE'


def node2block(node, begin_attr='d', end_attr='f'):
    dic = node.attrib
    return Block(
            a=int(dic[begin_attr]),
            b=int(dic[end_attr]),
            node=node)


def mk_path(xml_filename, filename):
    return join(dirname(xml_filename), filename)


def read_txt(filename, encoding):
    with io.open(filename, 'r', encoding=encoding) as o:
        txt = o.read()
    return txt


def read_xml(xml_filename):
    tree = ET.parse(xml_filename)
    return tree


def get_changes(xml_filename, window_size, encoding):
    tree = read_xml(xml_filename)
    transformations = tree.find('./informations/transformations')
    informations = tree.find('./informations').attrib
    txt_1 = read_txt(mk_path(xml_filename, informations['fsource']), encoding)
    txt_2 = read_txt(mk_path(xml_filename, informations['fcible']), encoding)
    txt = txt_1 + txt_2

    def gen_blocks(block_type):
        for replacement in transformations.findall(block_type):
            if block_type == './blocsdeplaces/bd':
                yield node2block(replacement, begin_attr='b1d', end_attr='b1f')
                yield node2block(replacement, begin_attr='b2d', end_attr='b2f')
            else:
                block = node2block(replacement)
                yield block

    Fragment = namedtuple('Fragment', 'left center right block')

    def p(x):
        return x

    def get_fragment(block):
        return Fragment(
            left=p(txt[(block.a-window_size):block.a]),
            center=p(txt[block.a:block.b]),
            right=p(txt[block.b:(block.b+window_size)]),
            block=block)

    empty_fragment = Fragment(left='', center='', right='', block='')
    # retrieve replacements
    blocks = list(gen_blocks(block_type='./remplacements/remp'))
    assert len(blocks) % 2 == 0
    N = len(blocks)//2
    Change = namedtuple('Change', 'type source dest')

    def gen_replacements():
        for ba, bb in list(zip(blocks[:N], blocks[N:])):
            yield Change(REPLACEMENT, get_fragment(ba), get_fragment(bb))

    replacements = list(gen_replacements())

    insertions = [Change(INSERTION, empty_fragment, get_fragment(b)) for b in gen_blocks(block_type='./insertions/ins')]
    deletions = [Change(DELETION, get_fragment(b), empty_fragment) for b in gen_blocks(block_type='./suppressions/sup')]
    moves_ = [k for k in gen_blocks(block_type='./blocsdeplaces/bd')]
    moves = [ Change(MOVE, get_fragment(a), get_fragment(b)) for a,b in zip(*[iter(moves_)]*2)]


    Changes = namedtuple('Changes', 'tree changes')
    return Changes(tree, replacements + insertions + deletions + moves)
