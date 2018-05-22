# -*- coding: utf-8 -*-
import cmd
import io
import argparse
from collections import namedtuple
import xml.etree.ElementTree as ET
from os.path import join, dirname,exists
from ansi import Fore, Style
                         
logo ='''                              
  /\/\   ___  __| (_) |_  ___  /__   \__ _  __ _  __ _  ___ _ __ 
 /    \ / _ \/ _` | | __|/ _ \   / /\/ _` |/ _` |/ _` |/ _ \ '__|
/ /\/\ \  __/ (_| | | |_|  __/  / / | (_| | (_| | (_| |  __/ |   
\/    \/\___|\__,_|_|\__|\___|  \/   \__,_|\__, |\__, |\___|_|   
                                           |___/ |___/        
'''
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
        

class Shell(cmd.Cmd):
    intro = logo + '\nType "start" to start tagging'
    prompt = '$ '

    def show_rep(self):
        rep = self.current_rep()
        left=u'{x.left}{code}{x.center}{reset}{x.right}'.format(x=rep.source, code=Fore.RED, reset=Style.RESET_ALL)
        right=u'{x.left}{code}{x.center}{reset}{x.right}'.format(x=rep.dest, code=Fore.GREEN, reset=Style.RESET_ALL)
        print('source ({rep.source.block.a},{rep.dest.block.a})'.format(**locals()).center(80,'-'))
        print(left)
        print('cible'.format(**locals()).center(80,'-'))
        print(right)
        print(80*'*')
        current_tag = rep.source.block.node.get('tag')
        print('enter y to tag change as significant else type n. (current tag is [{current_tag})]'.format(**locals()))
        self.wait_for_answer =True

    def current_rep(self):
        return self.replacements[self.cursor]

    def __init__(self, xml_filename, encoding):
        cmd.Cmd.__init__(self)
        assert exists(xml_filename), 'File {xml_filename} does not exist'.format(**locals())
        tree, replacements =  get_replacements(xml_filename, encoding)
        self.replacements = replacements
        self.xml_filename = xml_filename
        self.tree = tree
        self.cursor = 0
        self.wait_for_answer = False

    def increment_cursor(self):
        self.cursor+=1
        if self.cursor >= len(self.replacements):
            self.cursor = self.cursor % len(self.replacements)
        
    def decrement_cursor(self):
        self.cursor-=1
        if self.cursor < 0:
            self.cursor = len(self.replacements) + self.cursor
        

    def update_node(self, tag):
        self.current_rep().source.block.node.set('tag', tag)
        self.current_rep().dest.block.node.set('tag', tag)
        self.increment_cursor()
        self.show_rep()

    def do_start(self, arg):
        '''start analysis'''
        self.show_rep()

    def do_y(self, arg):
        '''tag change as significant'''
        if self.wait_for_answer:
            self.update_node('y')

    def do_n(self, arg):
        '''tag change as _not_ significant'''
        if self.wait_for_answer:
            self.update_node('n')

    def do_save(self, arg):
        '''save file'''
        filename = arg if arg else self.xml_filename
        print "Writing annotated file to {filename}".format(**locals())
        self.tree.write(filename)

    def do_undo(self, arg):
        '''re-evaluate previousgg'''
        self.decrement_cursor()
        self.show_rep()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required=True,
            help="path to input xml generated by MEDITE")
    ap.add_argument("-e", "--encoding", required=False, default='latin1',
            help="text file encoding")
    args = vars(ap.parse_args())
    shell = Shell(xml_filename=args['filename'], encoding=args['encoding'])
    shell.cmdloop()
