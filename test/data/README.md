# Test data

For testing purpose we have collected an open access bam file from a study called "Cell-free DNA Comprises an In Vivo Nucleosome Footprint that Informs Its Tissues-Of-Origin", the artile can be found here (https://www.sciencedirect.com/science/article/pii/S009286741501569X?via%3Dihub).

- id: SRR2130051_GSM1833277_IH02_Homo_sapiens_OTHER
- reference: hg19

We have used samtools to collect a subset of reads with the following command:
`samtools view -b -o test.bam SRR2130051_GSM1833277_IH02_Homo_sapiens_OTHER.bam 2:201,900,000-202,000,000`
