import numpy as np
import csv
import attr

from .bam import BAM
from .tss import load_transcription_start_sites

@attr.s
class BED:
    chrom = attr.ib()
    start = attr.ib()
    end = attr.ib()
    name = attr.ib()
    score = attr.ib()
    strand = attr.ib()


def load_bed_file(file_path):
    bed_list = list()
    with open(file_path) as fp:
        reader = csv.reader(fp, delimiter='\t')
        for line in reader:
            if line[0].startswith('#'):
                continue
            bed_list.append(BED(line[0], int(line[1]), int(line[2]), line[3], int(line[4]), line[5]))
    return bed_list

def calc_rel_start_and_end(read_start, read_end, strand, start):
    rel_start = read_start - start
    rel_end = read_end - start
    if strand == "+":
        return (rel_start, rel_end)
    elif strand == "-":
        return (-rel_end, -rel_start)


def add_read_ends(A, start, end, i):
    _, m = A.shape
    if start >= 0 and start < m:
        A[i][start] += 1
    if end >= 0 and end < m:
        A[i][end] += 1


def add_fragment(A, start, end, i):
    _, m = A.shape
    a = min((start, end))
    b = max((start, end))
    if a < 0:
        a = 0
    if b > m:
        b = m
    v = np.zeros(m, dtype=A.dtype)
    v[a:b] = 1
    A[i] += v


def generate_coverage_matrix(
    bam_file, bed_file, output_file, whole_fragment=False
):
    """ This function will iterate over a bed file and for each region fetch
        all fragments from the bam file.
        For each region the index of an array represents base pair position relative 
        to the start of the region, and the value 1 is added to each index of the array, 
        where a fragment or the ends of the fragments are positioned.
        This gives a histogram of coverage in the region.
        If the bed file is generated be the preprocessor, the TSS is in the center
        and we have a histogram of coverage around a TSS.
        All the arrays are then composed in a matrix so that rows represents
        TSS' and columns represents a positions relative to the TSS.
        Values are read-depth/coverage for either fragments or end-pairs

        :param bam_file: File path to the bam sample file
        :type bam_file: str
        :param bed_file: File path to the bed file, which can be compiled by the preprocessing function
        :type bed_file: str
        :param output_file: File path to the output file
        :type output_file: str
        :param whole_fragment: If False add only end pairs if True add the whole fragment
        :type output_file: boolean
        :returns:  None
    """
    bed_list = load_bed_file(bed_file)
    region_size = bed_list[0].end - bed_list[0].start
    coverage_matrix = np.zeros((len(bed_list), region_size), dtype=np.uint16)
    for i, region in enumerate(bed_list):
        bam = BAM(bam_file)
        for reading in bam.pair_generator(region.chrom, region.start, region.end):
            read_start = int(reading[1])
            read_end = int(reading[2])
            rel_start, rel_end = calc_rel_start_and_end(
                read_start, read_end, region.strand, region.start
            )
            if whole_fragment == True:
                add_fragment(coverage_matrix, rel_start, rel_end, i)
            else:
                add_read_ends(coverage_matrix, rel_start, rel_end, i)
    np.save(output_file, coverage_matrix)
