import numpy as np
import csv
import attr

from .bam import BAM

@attr.s
class BED:
    chrom = attr.ib()
    start = attr.ib()
    end = attr.ib()
    tss_id = attr.ib()
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

def calc_rel_start_and_end(read_start, read_end, strand, tss):
    rel_start = read_start - tss
    rel_end = read_end - tss
    if strand == "+":
        return (rel_start, rel_end)
    elif strand == "-":
        return (-rel_end, -rel_start)


def add_read_ends(A, start, end, i, k):
    _, m = A.shape
    a = start + k
    b = end + k
    if a >= 0 and a < m:
        A[i,a] += 1
    if b >= 0 and b < m:
        A[i,b] += 1


def add_fragment(A, start, end, i, k):
    _, m = A.shape
    a = min((start, end)) + k
    b = max((start, end)) + k
    if a < 0:
        a = 0
    if b > m:
        b = m
    v = np.zeros(m, dtype=A.dtype)
    v[a:b] = 1
    A[i] += v

def generate_length_matrix(
    bam_file, bed_file, output_file, max_length=500
):
    """ Creates a matrix where each row represents a region from the bed file
        and the columns are read lengths from 0 to max_length.
        The size of the matrix is (n x max_length) where n is the number of regions
        in the bed file.
        Data is read length counts, so that a_ij is the number of reads in region i, 
        with length j.

        :param bam_file: File path to the bam sample file
        :type bam_file: str
        :param bed_file: File path to the bed file, which can be compiled by the preprocessing function
        :type bed_file: str
        :param output_file: File path to the output file
        :type output_file: str
        :param max_length: Maximum read length to be counted
        :type max_length: int > 0
        :returns:  None
    """
    bed_list = load_bed_file(bed_file)
    matrix = np.zeros((len(bed_list), max_length), dtype=np.uint16)
    bam = BAM(bam_file)
    for i, region in enumerate(bed_list):
        for reading in bam.pair_generator(region.chrom, region.start, region.end):
            start = int(reading[1])
            end = int(reading[2])
            length = abs(end - start)
            if length < max_length:
                matrix[i,length] += 1
    np.save(output_file, matrix)

def generate_read_ends_matrix(
    bam_file, bed_file, output_file
):
    """ Creates a matrix where each row represents a region with a TSS in the
        center of the region and the columns represents base pair positions.
        The size of the matrix is (n x m) where n is the number of regions/TSS
        and m is the size og the region.
        Data is read-end counts, so that a_ij is the number of read-ends in region
        i at position j from region start.

        :param bam_file: File path to the bam sample file
        :type bam_file: str
        :param bed_file: File path to the bed file, which can be compiled by the preprocessing function
        :type bed_file: str
        :param output_file: File path to the output file
        :type output_file: str
        :returns:  None
    """
    bed_list = load_bed_file(bed_file)
    region_size = bed_list[0].end - bed_list[0].start
    coverage_matrix = np.zeros((len(bed_list), region_size), dtype=np.uint16)
    bam = BAM(bam_file)
    for i, region in enumerate(bed_list):
        tss = int(region.tss_id.split('_')[-1])
        for reading in bam.pair_generator(region.chrom, region.start, region.end):
            read_start = int(reading[1])
            read_end = int(reading[2])
            rel_start, rel_end = calc_rel_start_and_end(
                read_start, read_end, region.strand, tss
            )
            k = tss - region.start
            add_read_ends(coverage_matrix, rel_start, rel_end, i, k)
    np.save(output_file, coverage_matrix)

def generate_coverage_matrix(
    bam_file, bed_file, output_file
):
    """ Creates a matrix where each row represents a region with a TSS in the
        center of the region and the columns represents base pair positions.
        The size of the matrix is (n x m) where n is the number of regions/TSS
        and m is the size og the region.
        Data is read-depth/coverage, so that a_ij is the number of overlapping 
        reads in region i at position j from region start.

        :param bam_file: File path to the bam sample file
        :type bam_file: str
        :param bed_file: File path to the bed file, which can be compiled by the preprocessing function
        :type bed_file: str
        :param output_file: File path to the output file
        :type output_file: str
        :returns:  None
    """
    bed_list = load_bed_file(bed_file)
    region_size = bed_list[0].end - bed_list[0].start
    coverage_matrix = np.zeros((len(bed_list), region_size), dtype=np.uint16)
    bam = BAM(bam_file)
    for i, region in enumerate(bed_list):
        tss = int(region.tss_id.split('_')[-1])
        for reading in bam.pair_generator(region.chrom, region.start, region.end):
            read_start = int(reading[1])
            read_end = int(reading[2])
            rel_start, rel_end = calc_rel_start_and_end(
                read_start, read_end, region.strand, tss
            )
            k = tss - region.start
            add_fragment(coverage_matrix, rel_start, rel_end, i, k)
    np.save(output_file, coverage_matrix)
