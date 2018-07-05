import xml.etree.ElementTree as ET
from xml.dom import minidom
import io
import textwrap as tw
import itertools as it
from collections import namedtuple
from ansi import Fore, Style

# from constantesDonnees
FICHIER_INFO = 'Informations.xml'
## Balises ##
B_ROOT = 'root'
B_AUTEUR = 'auteur'
B_NOM = 'nom'
B_PRENOM = 'prenom'
B_NAISSANCE = 'naissance'
B_DECES = 'deces'
B_OEUVRE = 'oeuvre'
B_TITRE = 'titre'
B_EDITION = 'edition'
B_PUBLICATION = 'publication'
B_INFORMATIONS = u'informations'
B_VERS_SOURCE = u'vsource'
B_ETAT_SOURCE = 'fsource'
B_VERS_CIBLE = u'vcible'
B_ETAT_CIBLE = u'fcible'
B_PARAM_1 = u'lg_pivot'
B_PARAM_2 = u'ratio'
B_PARAM_3 = u'seuil'
B_PARAM_4 = u'car_mot'
B_PARAM_5 = u'caseSensitive'
B_PARAM_6 = u'sepSensitive'
B_PARAM_7 = u'diacriSensitive'
B_TRANSFORMATIONS = u'transformations'
B_LGSOURCE = u'lgsource'
B_INSERTIONS = u'insertions'
B_SUPPRESSIONS = u'suppressions'
B_DEPLACEMENTS = u'deplacements'
B_REMPLACEMENTS = u'remplacements'
B_BLOCSCOMMUNS = u'blocscommuns'
B_BLOCSDEPLACES = u'blocsdeplaces'
B_NONDEF = u'blocsNonDefinis'
B_LG = u'lg'
B_INS = u'ins'
B_SUP = u'sup'
B_DEP = u'dep'
B_REMP = u'remp'
B_BC = u'bc'
B_ND = u'nd'
B_MOT = u'mot'
B_DEB = u'd'
B_FIN = u'f'
B_DEP = u'bd'
B1_D = u'b1d'
B1_F = u'b1f'
B2_D = u'b2d'
B2_F = u'b2f'
#B_REMP = 'remp'
B_MOT_AVANT = 'motavant'
B_MOT_APRES = 'motapres'
B_TEXT_SOURCE = 'textsource'
B_TEXT_CIBLE = 'textcible'
B_TEXT = 'tcommun'
B_TEXT_INSER = 'tinsertion'
B_TEXT_SUPP = 'tsuppression'
B_TEXT_DEPL = 'tdeplacement'
B_TEXT_REMP = 'tremplacement'
B_COMMENTAIRE = 'commentaire'

B_ARBRE = 'arbre'
B_VERSION = 'version'
B_ETAT = 'etat'
B_ID = "id"


def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def read_txt(filename, encoding='cp1252'):
    with io.open(filename, 'r', encoding=encoding) as o:
        txt = o.read()
    return txt

def make_informations(appli, source_filename, target_filename):
    result = appli.result
    parameters = appli.parameters
    root = ET.Element(B_ROOT)
    info = ET.SubElement(root, B_INFORMATIONS)
    info.set(B_ETAT_SOURCE, source_filename)
    info.set(B_ETAT_CIBLE,  target_filename)

    info.set(B_PARAM_1, '%s' % parameters.lg_pivot)
    info.set(B_PARAM_2, '%s' % parameters.ratio)
    info.set(B_PARAM_3, '%s' % parameters.seuil)
    info.set(B_PARAM_4, '%s' % int(parameters.car_mot))
    info.set(B_PARAM_5, '%s' % int(parameters.case_sensitive))
    info.set(B_PARAM_6, '%s' % int(parameters.sep_sensitive))
    info.set(B_PARAM_7, '%s' % int(parameters.diacri_sensitive))
    transfo = ET.SubElement(info, B_TRANSFORMATIONS)
    lg = ET.SubElement(transfo, B_LGSOURCE)
    lg.set(B_LG, str(result.getLgSource()))

    insertions = ET.SubElement(transfo, B_INSERTIONS)
    for deb, fin in result.getListeInsertions():
        node = ET.SubElement(insertions, B_INS)
        node.set(B_DEB, str(deb))
        node.set(B_FIN, str(fin))

    suppressions = ET.SubElement(transfo, B_SUPPRESSIONS)
    for deb, fin in result.getListeSuppressions():
        node = ET.SubElement(suppressions, B_SUP)
        node.set(B_DEB, str(deb))
        node.set(B_FIN, str(fin))

    deplacements = ET.SubElement(transfo, B_DEPLACEMENTS)
    for deb, fin in result.getListeDeplacements():
        node = ET.SubElement(deplacements, B_DEP)
        node.set(B_DEB, str(deb))
        node.set(B_FIN, str(fin))
    #print prettify(root)
    remplacements = ET.SubElement(transfo, B_REMPLACEMENTS)
    for deb, fin in result.getListeRemplacements():
        node = ET.SubElement(remplacements, B_REMP)
        node.set(B_DEB, str(deb))
        node.set(B_FIN, str(fin))

    blocsCommuns = ET.SubElement(transfo, B_BLOCSCOMMUNS)
    for deb, fin in result.getBlocsCommuns():
        node = ET.SubElement(blocsCommuns, B_BC)
        node.set(B_DEB, str(deb))
        node.set(B_FIN, str(fin))

    nonDefined = ET.SubElement(transfo, B_NONDEF)
    for deb, fin in result.getNonDef():
        node = ET.SubElement(nonDefined, B_ND)
        node.set(B_DEB, str(deb))
        node.set(B_FIN, str(fin))

    blocsDeplaces = ET.SubElement(transfo, B_BLOCSDEPLACES)
    for (b1deb, b1fin), (b2deb, b2fin) in result.getPairesBlocsDeplaces():
        node = ET.SubElement(blocsDeplaces, B_DEP)
        node.set(B1_D, str(b1deb))
        node.set(B1_F, str(b1fin))
        node.set(B2_D, str(b2deb))
        node.set(B2_F, str(b2fin))
    return prettify(root)


def make_html_output(appli, html_filename):
    table_html_str = appli.bbl._BiBlocList__listeToHtmlTable()
    with io.open(html_filename, 'w', encoding='utf8') as o:
        html = u'<html><body><table>{table_html_str}</table></body></html>'.format(
            **locals())
        o.write(html)

def make_xml_output(appli, source_filename, target_filename, info_filename):
    info = make_informations(
        appli=appli, source_filename=source_filename, target_filename=target_filename)
    with io.open(info_filename, 'w', encoding='utf8') as o:
        o.write(info)



Fragment=namedtuple('fragment', 'type txt')
def pretty_print(appli):
    def f(block):
        if not block:
            return Fragment('', '')
        start = block[1]
        end   = block[2]
        return Fragment(block[0], appli.bbl.texte[start:end])
    W=40
    template = u'{la:<4}|{lcode}{ta:<__W__}{reset}|{rcode}{tb:<__W__}{reset}|{lb:>4}'.replace('__W__', str(W))
    for a,b in appli.bbl.liste:
        fa = f(a)
        fb = f(b)
        type2code = {'BC':Fore.BLACK, 'R':Fore.RED, 'I': Fore.BLUE, '':Fore.YELLOW}
        lcode=type2code.get(fa.type,Fore.YELLOW)
        rcode=type2code.get(fb.type,Fore.YELLOW)
        for la,lb,ta,tb in it.izip_longest(
            [fa.type], [fb.type], tw.wrap(fa.txt, W), tw.wrap(fb.txt, W), fillvalue=' '):
            print(template.format(
                lcode=lcode,
                rcode=rcode,
                reset=Style.RESET_ALL,
                la=la,
                lb=lb,
                ta=ta,
                tb=tb))

