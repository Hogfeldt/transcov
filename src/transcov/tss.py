import attr

@attr.s
class TranscriptionStartSite:
    tss_id = attr.ib()
    chrom = attr.ib()
    tss = attr.ib()
    strand = attr.ib()
    tx_id = attr.ib()
    gene_id = attr.ib()
    ccds_id = attr.ib()

    def __str__(self):
        return f"{self.tss_id} {self.chrom} {self.tss} {self.strand} {self.tx_id} {self.gene_id} {self.ccds_id}"
