import click
from os.path import dirname, join
from medite import medite as md
from medite import utils as ut

default = md.DEFAULT_PARAMETERS

@click.command()
@click.argument('source_filename', type=click.Path(exists=True))
@click.argument('target_filename', type=click.Path(exists=True))
@click.option('--lg_pivot', default=default.lg_pivot)
@click.option('--ratio', default=default.ratio)
@click.option('--seuil', default=default.seuil)
@click.option('--case-sensitive/--no-case-sensitive', default=default.case_sensitive)
@click.option('--diacri-sensitive/--no-diacri-sensitive', default=default.diacri_sensitive)
@click.option('--output-xml', type=click.Path(exists=False), default='informations.xml')
@click.option('--output-html', type=click.Path(exists=False), default='diff_table.html')
def run(source_filename, target_filename, lg_pivot, ratio, seuil, case_sensitive, diacri_sensitive, output_xml, output_html):
    algo = default.algo
    sep_sensitive = default.sep_sensitive
    car_mot = default.car_mot
    assert dirname(source_filename) == dirname(target_filename),\
        "source filename [{source_filename}] and target filename [{target_filename}] are not in the same directory".format(**locals())
    base_dir = dirname(source_filename)
    parameters = md.Parameters(
        lg_pivot,
        ratio,
        seuil,
        car_mot,
        case_sensitive,
        sep_sensitive,
        diacri_sensitive,
        algo)
    txt1 = ut.read_txt(source_filename)
    txt2 = ut.read_txt(target_filename)

    def f(field):
        click.echo('using {field}={value}'.format(field=field, value=parameters._asdict()[field]))
    [f(k) for k in parameters._fields]

    appli = md.DiffTexts(
        chaine1=txt1, chaine2=txt2,
        parameters=parameters)
    ut.make_html_output(
        appli=appli,
        html_filename=join(base_dir, output_html))
    click.echo('html output written to {output_html}'.format(**locals()))
    output_path = join(base_dir, output_xml)
    ut.make_xml_output(
        appli=appli,
        source_filename=source_filename,
        target_filename=target_filename,
        info_filename=output_path)
    ut.pretty_print(appli)
    click.echo('xml output written to {output_path}'.format(**locals()))


if __name__ == '__main__':
    run()
