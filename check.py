import io
import argparse
from collections import namedtuple
import xml.etree.ElementTree as ET
from os.path import join, dirname,exists
from ansi import Fore, Style


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
        return x.encode(encoding)
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
        

def process(xml_filename, encoding):
    assert exists(xml_filename), 'File {xml_filename} does not exist'.format(**locals())
    print(repr(Fore.RED))
    print(80*'*')
    tree, replacements = get_replacements(xml_filename, encoding)
    response2tag = {'y': 'y', 'n': 'n'} 

    def query_user_input(rep, i, N):
        left='{x.left}{code}{x.center}{reset}{x.right}'.format(x=rep.source, code=Fore.RED, reset=Style.RESET_ALL)
        right='{x.left}{code}{x.center}{reset}{x.right}'.format(x=rep.dest, code=Fore.GREEN, reset=Style.RESET_ALL)
        print('source [{rep.source.block.a}]'.format(**locals()).center(80,'-'))
        print(left)
        print('cible [{rep.dest.block.a}]'.format(**locals()).center(80,'-'))
        print(right)
        print(80*'*')
        result = None
        while not result in response2tag:
            result = raw_input('{i}/{N} Change significant? [y/n]'.format(**locals()))
        return response2tag[result]

    def annotate():
        for i, rep in enumerate(replacements[0:3]): 
            tag = query_user_input(rep, i+1, len(replacements))
            rep.source.block.node.set('tag', tag)
            rep.dest.block.node.set('tag', tag)

    def get_annotated_filename(xml_filename): 
        return xml_filename.replace('.xml', '.annotated.xml')

    annotate()
    annotated_filename = get_annotated_filename(xml_filename) 
    print "Writing file to {annotated_filename}".format(**locals())
    tree.write(annotated_filename)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required=True,
            help="path to input xml generated by MEDITE")
    ap.add_argument("-e", "--encoding", required=False, default='latin1',
            help="text file encoding")
    args = vars(ap.parse_args())
    process(xml_filename=args['filename'], encoding=args['encoding'])
