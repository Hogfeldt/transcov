import argparse
import attr
import re

from .transcript_annotation import pull_tx_id, pull_ensemble_gene_id, pull_ccds_id
from .tss import TranscriptionStartSite

@attr.s
class Tx_annotation:
    chrom = attr.ib()
    start = attr.ib()
    end = attr.ib()
    strand = attr.ib()
    additionals = attr.ib()

def is_chrome_autosome(chrom):
    return re.match(r"chr\d", chrom) != None

def get_transcript_annotations(file_path):
    with open(file_path, "r") as file_obj:
        for line in file_obj:
            if line[0] == '#':  # line is comment
                continue
            anno = line.replace('\n','').split()
            if anno[2] != 'transcript': # line is not a transcript
                continue
            if is_chrome_autosome(anno[0]):
                anno_obj = Tx_annotation(
                    anno[0], int(anno[3]), int(anno[4]), anno[6], anno[8]
                )
                yield anno_obj

def determine_TSS_and_format_data(tx_anno):
    if tx_anno.strand == "+":
        TSS = tx_anno.start
    elif tx_anno.strand == "-":
        TSS = tx_anno.end
    else:
        raise Exception("Strand annotation is neither '+' nor '-'")
    tss_id = "_".join((tx_anno.chrom, str(TSS)))
    return TranscriptionStartSite(tss_id, tx_anno.chrom, TSS, tx_anno.strand, pull_tx_id(tx_anno), pull_ensemble_gene_id(tx_anno), pull_ccds_id(tx_anno))

def preprocess(input_file, output_file):
    """ API docstring! """
    tx_annotations = get_transcript_annotations(input_file)
    unique_TSSs = set()
    with open(output_file, 'w') as fp:
        for tx_anno in tx_annotations:
            tss = determine_TSS_and_format_data(tx_anno)
            if tss.tss_id not in unique_TSSs:
                unique_TSSs.add(tss.tss_id)
                fp.write("%s\n" % str(tss))
    return output_file
