import click

from .api import preprocess_gencode_annotation

@click.group()
def cli():
    pass

@cli.command()
@click.argument('annotation_file')
@click.argument('output_file')
def preprocess(annotation_file, output_file):
    preprocess_gencode_annotation(annotation_file, output_file)

@cli.command()
def generate(annotation_file, output_file):
    pass

