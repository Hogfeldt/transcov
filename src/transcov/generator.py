import numpy as np

from .bam import BAM
from .tss import load_transcription_start_sites


def calc_rel_start_and_end(read_start, read_end, strand, TSS):
    rel_start = read_start - TSS
    rel_end = read_end - TSS
    if strand == "+":
        return (rel_start, rel_end)
    elif strand == "-":
        return (-rel_end, -rel_start)


def add_read_ends(A, start, end, i, k):
    if start >= -k and start <= k:
        A[i][k + start] += 1
    if end >= -k and end <= k:
        A[i][k + end] += 1


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


def generate_coverage_matrix(
    bam_file, tss_file, region_size, output_file, whole_fragment=False
):
    """ This function will iterate over the TSS' in the tss file, and fetch
        all fragments from the bam file, in a region of the size defined by region_size. 
        The TSS will be the center of the region.
        For each tss the index of an array represents base pair position relative 
        to the TSS, and the value 1 is added to each index of the array, where a 
        fragment or the ends of the fragments are positioned.
        This gives a histogram of coverage around the TSS for each TSS.
        All the arrays are then composed in a matrix so that rows represents
        TSS' and columns represents a positions relative to the TSS.
        Values are read-depth/coverage for either fragments or end-pairs


        :param bam_file: File path to the bam sample file
        :type bam_file: str
        :param tss_file: File path to the tss file, compiled by the preprocessing function
        :type tss_file: str
        :param region_size: Size og the region to inspect where the TSS is in the center of the region
        :type region_size: positive int
        :param output_file: File path to the output file
        :type output_file: str
        :param whole_fragment: If False add only end pairs if True add the whole fragment
        :type output_file: boolean
        :returns:  None
    """
    k = int(region_size / 2)
    tss_list = load_transcription_start_sites(tss_file)
    coverage_matrix = np.zeros((len(tss_list), 2 * k + 1), dtype=np.uint16)
    for i, tss in enumerate(tss_list):
        bam = BAM(bam_file)
        for reading in bam.pair_generator(tss.chrom, tss.tss - k, tss.tss + k):
            read_start = int(reading[1])
            read_end = int(reading[2])
            rel_start, rel_end = calc_rel_start_and_end(
                read_start, read_end, tss.strand, tss.tss
            )
            if whole_fragment == True:
                add_fragment(coverage_matrix, rel_start, rel_end, i, k)
            else:
                add_read_ends(coverage_matrix, rel_start, rel_end, i, k)
    np.save(output_file, coverage_matrix)
