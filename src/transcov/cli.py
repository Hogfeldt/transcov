import click

from . import generate_coverage_matrix, generate_read_ends_matrix, generate_length_matrix
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
@click.option("-k", "--region-size", default=10000, type=click.IntRange(min=0))
@click.option("--bed-file", default="transcription_start_sites.bed")
@click.option("--tss-file", default="transcription_start_sites.tsv")
def preprocess(annotation_file, region_size, bed_file, tss_file):
    preprocessor.preprocess(annotation_file, region_size, bed_file, tss_file)

@cli.command()
@click.argument("bam_file")
@click.argument("bed_file")
@click.option("-o", "--output-file", default="coverage_matrix.npy")
def generate_coverage(bam_file, bed_file, output_file):
    generate_coverage_matrix(bam_file, bed_file, output_file)

@cli.command()
@click.argument("bam_file")
@click.argument("bed_file")
@click.option("-o", "--output-file", default="read_ends_matrix.npy")
def generate_read_ends(bam_file, bed_file, output_file):
    generate_read_ends_matrix(bam_file, bed_file, output_file)

@cli.command()
@click.argument("bam_file")
@click.argument("bed_file")
@click.option("-o", "--output-file", default="length_matrix.npy")
@click.option("-m", "--max-length", default=500, type=click.IntRange(min=1))
def generate_length(bam_file, bed_file, output_file, max_length):
    generate_length_matrix(bam_file, bed_file, output_file, max_length)

@cli.command()
@click.argument("matrices", nargs=-1)
@click.option("-o", "--output-file", default="collapsed_matrix.npy")
@click.option("-s", "--start", default=0, type=click.IntRange(min=0))
@click.option("-e", "--end", default=None, type=int)
@click.option("--uint32", is_flag=True)
def collapse(matrices, output_file, start, end, uint32):
    if len(matrices) > 0:
        collapser.collapse(matrices, output_file, start, end, uint32)
