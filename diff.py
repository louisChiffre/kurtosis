import click
from os.path import dirname, join
from medite import medite as md
from medite import utils as ut


@click.command()
@click.argument('source_filename', type=click.Path(exists=True))
@click.argument('target_filename', type=click.Path(exists=True))
@click.option('--lg_pivot', default=7)
@click.option('--ratio', default=15)
@click.option('--seuil', default=50)
@click.option('--case-sensitive/--no-case-sensitive', default=True)
@click.option('--diacri-sensitive/--no-diacri-sensitive', default=True)
@click.option('--output-xml', type=click.Path(exists=False), default='informations.xml')
@click.option('--output-html', type=click.Path(exists=False), default='diff_table.html')
def run(source_filename, target_filename, lg_pivot, ratio, seuil, case_sensitive, diacri_sensitive, output_xml, output_html):
    algo = 'HIS'
    sep_sensitive = True
    car_mot = True
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
    ut.make_xml_output(
        appli=appli,
        source_filename=source_filename,
        target_filename=target_filename,
        info_filename=join(base_dir, output_xml))
    click.echo('xml output written to {output_xml}'.format(**locals()))
    ut.pretty_print(appli)


if __name__ == '__main__':
    run()
