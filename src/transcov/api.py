from .generator import generate_coverage_matrix
from .preprocessor import preprocess
from .collapser import collapse

def preprocess_gencode_annotation(annotation_path, output_path):
    return preprocess(annotation_path, output_path)

def generate_coverage_matrix_with_read_ends(bam_file, annotation_file, k, output_file):
    generate_coverage_matrix(bam_file, annotation_file, k, output_file)

def generate_coverage_matrix_with_fragments(bam_file, annotation_file, k, output_file):
    generate_coverage_matrix(bam_file, annotation_file, k, output_file, whole_fragment=True)

def collapse_matrices(matrices, output, uint32):
    collapse(matrices, output, uint32)
