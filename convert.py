import click
import io


@click.command()
@click.argument('source_filename', type=click.Path(exists=True))
@click.argument('target_filename', type=click.Path(exists=False))
@click.option('--source-encoding', default='cp1252')
@click.option('--target-encoding', default='utf-8')
def convert(source_filename, target_filename, source_encoding, target_encoding):
    click.echo('converting file {source_filename} encoded as {source_encoding} to {target_filename} with {target_encoding}'.format(**locals()))
    with io.open(source_filename, 'r', encoding=source_encoding) as o:
        source = o.read()
    with io.open(target_filename, 'w', encoding=target_encoding) as o:
        o.write(source)

if __name__ == '__main__':
    convert()
