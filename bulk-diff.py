import click
from os.path import dirname, join
from os import listdir
from medite import medite as md
from medite import utils as ut

default = md.DEFAULT_PARAMETERS

@click.command()
@click.argument('source_directory', type=click.Path(exists=True))
@click.option('--lg_pivot', default=default.lg_pivot)
@click.option('--ratio', default=default.ratio)
@click.option('--seuil', default=default.seuil)
@click.option('--case-sensitive/--no-case-sensitive', default=default.case_sensitive)
@click.option('--diacri-sensitive/--no-diacri-sensitive', default=default.diacri_sensitive)
@click.option('--output-xml-suffix', type=click.Path(exists=False), default='.xml')
def run(source_directory, lg_pivot, ratio, seuil, case_sensitive, diacri_sensitive, output_xml_suffix):
    algo = default.algo
    sep_sensitive = default.sep_sensitive
    car_mot = default.car_mot
    parameters = md.Parameters(
        lg_pivot,
        ratio,
        seuil,
        car_mot,
        case_sensitive,
        sep_sensitive,
        diacri_sensitive,
        algo)

    files = sorted([k for k in listdir(source_directory) if k.endswith('.txt')])
    def f(field):
        click.echo('using {field}={value}'.format(field=field, value=parameters._asdict()[field]))
    [f(k) for k in parameters._fields]
    
    from collections import namedtuple 
    Comparison = namedtuple('Comparison', 'source target output')

    def make_output_filename(source, target):
        def strip(f):
            return f.replace('.txt','')
        return '{source}_vs_{target}_{suffix}'.format(suffix=output_xml_suffix, source=strip(source), target=strip(target))
    
    def comparison_iter():
        for source, target in zip(files[:-1],files[1:]):
            yield Comparison(source=source, target=target, output=make_output_filename(source, target))

    for comparison in comparison_iter():
        click.echo('[{source}] will be compared to [{target}] and result stored in [{output}]'.format(**comparison._asdict()))

    def mk_path(filename):
        return join(source_directory, filename)

    for comparison in comparison_iter():
        click.echo('processing [{source}] vs [{target}]'.format(**comparison._asdict()))
        source_filename =mk_path(comparison.source)
        target_filename=mk_path(comparison.target)
        txt1 = ut.read_txt(source_filename)
        txt2 = ut.read_txt(target_filename)
        appli = md.DiffTexts(
            chaine1=txt1, chaine2=txt2,
            parameters=parameters)
        ut.make_xml_output(
            appli=appli,
            source_filename=source_filename,
            target_filename=target_filename,
            info_filename=join(source_directory, comparison.output))
        ut.pretty_print(appli)
        click.echo('result stored in [{output}]'.format(output=mk_path(comparison.output)))


if __name__ == '__main__':
    run()
