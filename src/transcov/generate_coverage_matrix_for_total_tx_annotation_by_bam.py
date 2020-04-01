import argparse
from tss import TranscriptionStartSite
from bam import BAM
import numpy as np
import csv


def load_transcription_start_sites(input_file):
    TSSs = list()
    with open(input_file) as fp:
        tsv_reader = csv.reader(fp, delimiter=" ")
        for line in tsv_reader:
            tss = TranscriptionStartSite(line[0], line[1], int(line[2]), line[3], line[4], line[5])
            TSSs.append(tss)
    return TSSs


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

def main(annotation_file, bam_file, k, output_file, whole_fragment):
    tss_list = load_transcription_start_sites(annotation_file)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for creating a data structure containing the coverage relative to TSS, given a set og bam files, for all transcript in gencode annotation"
    )
    parser.add_argument(
        "annotation_file", help="File path to the gencode annotation file"
    )
    parser.add_argument(
        "bam_file",
        help="File path to a file containing paths to all the bam file which should be read from",
    )
    parser.add_argument(
        "-k",
        dest="k",
        default=5000,
        help="The range in bp that defines the region of interest. The region is +-2k bp with the TSS in the center",
    )
    parser.add_argument(
        "output_file", help="The file path to where the output data should be stored"
    )
    parser.add_argument(
        "--whole-fragment", action="store_true", help="Add one for every bp between readends"
    )
    args = parser.parse_args()
    main(args.annotation_file, args.bam_file, int(args.k), args.output_file, args.whole_fragment)
