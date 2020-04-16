from gwf import Workflow, AnonymousTarget
from glob import glob
from os.path import join

gwf = Workflow(defaults={"walltime": "00:10:00"})

# Target functions
def preprocess_gencode_annotation(annotation_file, bed_file, tss_file, region_size):
    """ This target will generate a file bed file and meta data file, defining the TSS' 
        to look for in the bam files. Theese TSS' will define the rows of the matrices """
    inputs = [annotation_file]
    outputs = [bed_file, tss_file]
    options = {}
    spec = """
    transcov preprocess {} --bed-file {} --tss-file {} --region-size {}
    """.format(
        annotation_file, bed_file, tss_file, region_size
    )
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def generate_matrix(bam_file, bed_file, output_file):
    """ This target will given a bam file and a bed file created by the preprocesser
        generate a coverage matrix, showing read depth in a region around the TSS """
    inputs = [bam_file, bed_file]
    outputs = [output_file]
    options = {"walltime": "12:00:00", "memory": "6gb"}
    spec = """
    transcov generate {} {} --output-file {}
    """.format(
        bam_file, bed_file, output_file
    )
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def collapse_matrices_upon_eachother(matrices, output_file):
    """ This target will add coverage matrices together value by value, which can
        be helpfull if you look at coverage across different samples """
    inputs = matrices
    outputs = [output_file]
    options = {"walltime": "1:00:00", "memory": "24gb"}
    spec = """
    transcov collapse {} --output-file {} 
    """.format(
        " ".join(matrices), output_file
    )
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


#   Input Files:
#   Here we assume that you have a gencode annotation file in a directory called
#   gencodes and your bam files in a directory called bams
#
gencode_annotation_file = "gencodes/gencode.v19.annotation.gff3"
bams = glob("bams/*.bam")

#   Output Files:
#   Here we assume that you have directory called coverage_matrices for storing
#   the output files
tss_file = "gencodes/gencode.v19.annotation.tss.tsv"
bed_file = "gencodes/gencode.v19.annotation.tss.bed"
output_dir = "coverage_matrices"
collapsed_coverage_matrix = join(output_dir, "collapsed_coverage_matrix.npy")

# defining targets
gwf.target_from_template(
    name="preprocess_gencode_annotation",
    template=preprocess_gencode_annotation(
        annotation_file=gencode_annotation_file, 
        bed_file=bed_file, 
        tss_file=tss_file, 
        region_size=10000
    ),
)

coverage_matrices = list()
for i, bam_file in enumerate(bams):
    output_file = join(output_dir, bam_file.replace(".bam", ".coverage_matrix.npy").split('/')[-1])
    gwf.target_from_template(
        name=f"generate_matrix_{i}",
        template=generate_matrix(
            bam_file=bam_file,
            bed_file=bed_file,
            output_file=output_file,
        ),
    )
    coverage_matrices.append(output_file)

gwf.target_from_template(
    name="collapse_coverage_matrices",
    template=collapse_matrices_upon_eachother(
        matrices=coverage_matrices, output_file=collapsed_coverage_matrix,
    ),
)
