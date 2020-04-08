import attr
import csv


@attr.s
class TranscriptionStartSite:
    tss_id = attr.ib()
    chrom = attr.ib()
    tss = attr.ib()
    strand = attr.ib()
    tx_ids = attr.ib()
    gene_id = attr.ib()
    ccds_id = attr.ib()
    tx_type = attr.ib()

    def __str__(self):
        return "\t".join(
            (
                self.tss_id,
                self.chrom,
                str(self.tss),  # is integer
                self.strand,
                " ".join(self.tx_ids),
                self.gene_id,
                str(self.ccds_id),  # is string or None
                self.tx_type,
            )
        )


def get_header():
    return "\t".join(
        ("tss_id", "chrom", "tss", "strand", "tx_ids", "gene_id", "ccds_id", "tx_type")
    )


def load_transcription_start_sites(input_file):
    TSSs = list()
    with open(input_file) as fp:
        tsv_reader = csv.reader(fp, delimiter="\t")
        header = next(tsv_reader)
        for line in tsv_reader:
            tss = TranscriptionStartSite(
                line[0],
                line[1],
                int(line[2]),
                line[3],
                line[4].split(),
                line[5],
                line[6],
                line[7],
            )
            TSSs.append(tss)
    return TSSs
