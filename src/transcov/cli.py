import click

from .api import preprocess_gencode_annotation, generate_coverage_matrix_with_read_ends

@click.group()
def cli():
    pass

@cli.command()
@click.argument('annotation_file')
@click.option('-o', '--output-file', default='transcription_start_sites.tsv')
def preprocess(annotation_file, output_file):
    preprocess_gencode_annotation(annotation_file, output_file)

@cli.command()
@click.argument('bam_file')
@click.argument('tss_file')
@click.option('-k', '--region-size', default=10000)
@click.option('-o', '--output-file', default='coverage_matrix.npy')
def generate(bam_file, tss_file, region_size, output_file):
    generate_coverage_matrix_with_read_ends(bam_file, tss_file, region_size, output_file) 

