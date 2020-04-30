import click
from os.path import isfile

from .generator import (
    generate_coverage_matrix,
    generate_read_ends_matrix,
    generate_length_matrix,
    generate_end_length_tensor,
)
from . import preprocessor
from . import manipulations
from . import plotter
from .utils import tsv_reader, determine_index_file_name


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
@click.argument("bam_file")
@click.argument("bed_file")
@click.option("-o", "--output-file", default="end_length_tensor.npy")
@click.option("-m", "--max-length", default=500, type=click.IntRange(min=1))
def generate_end_length(bam_file, bed_file, output_file, max_length):
    generate_end_length_tensor(bam_file, bed_file, output_file, max_length)

@cli.command()
@click.argument("matrices", nargs=-1)
@click.option("-o", "--output-file", default="collapsed_matrix.npy")
@click.option("-s", "--start", default=0, type=click.IntRange(min=0))
@click.option("-e", "--end", default=None, type=int)
@click.option("--uint32", is_flag=True)
def collapse(matrices, output_file, start, end, uint32):
    if len(matrices) > 0:

        def isfile_or_none(file_path):
            if isfile(file_path):
                return file_path
            else:
                return None

        indexes = map(isfile_or_none, map(determine_index_file_name, matrices))
        print(indexes)
        manipulations.collapse(zip(matrices, indexes), output_file, start, end, uint32)


@cli.command()
@click.argument("input_matrix")
@click.argument("index_file")
@click.argument("ids_file")
@click.option("-o", "--output-file", default="subset_matrix.npy")
def pick_subset(input_matrix, index_file, ids_file, output_file):
    ids = list()
    with open(ids_file) as fp:
        for line in tsv_reader(fp):
            if line[0].startswith("#"):
                continue
            ids.append(line[0])
    manipulations.pick_subset(input_matrix, index_file, output_file, ids)


@cli.command()
@click.argument("input_matrix")
@click.argument("index_file")
@click.option("-o", "--output-file", default="tail_cutted_matrix.npy")
@click.option("-c", "--cut", default=0.05, type=click.FloatRange(min=0,max=1))
@click.option("-m", "--mode", default="both", type=click.Choice(['both','left','right'], case_sensitive=False))
def cut_tails(input_matrix, index_file, output_file, cut, mode):
    tail_funcs = {'both': manipulations.cut_tails_both,
                  'left': manipulations.cut_tails_left,
                  'right': manipulations.cut_tails_right,
                  }
    tail_funcs[mode](input_matrix, index_file, output_file, cut)

@cli.command()
@click.argument("input_tensor")
@click.option("-o", "--output-file", default="plot.png")
def plot_tensor_dist(input_tensor, output_file):
    plotter.plot_end_length_frag_start_dist(input_tensor, output_file)

@cli.command()
@click.argument("input_matrix")
@click.option("-o", "--output-file", default="coverage_distribution.png")
def plot_coverage_dist(input_matrix, output_file):
    plotter.plot_coverage_distribution(input_matrix, output_file)
