import click

from .generator import generate_coverage_matrix
from . import preprocessor
from . import collapser


@click.group()
def cli():
    # Add debug info like:
    # click.echo('No matrices was given to collapse')
    # click.echo('Only one matrix was given to collapse')
    pass


@cli.command()
@click.argument("annotation_file")
@click.option("-o", "--output-file", default="transcription_start_sites.tsv")
def preprocess(annotation_file, output_file):
    preprocessor.preprocess(annotation_file, output_file)


@cli.command()
@click.argument("bam_file")
@click.argument("tss_file")
@click.option("-k", "--region-size", default=10000)
@click.option("-o", "--output-file", default="coverage_matrix.npy")
def generate(bam_file, tss_file, region_size, output_file):
    generate_coverage_matrix(bam_file, tss_file, region_size, output_file)


@cli.command()
@click.argument("matrices", nargs=-1)
@click.option("-o", "--output-file", default="collapsed_matrix.npy")
@click.option("--uint32", is_flag=True)
def collapse(matrices, output_file, uint32):
    if len(matrices) > 0:
        collapser.collapse(matrices, output_file, uint32)
