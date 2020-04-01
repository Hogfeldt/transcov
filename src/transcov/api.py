from .generator import main
from .preprocessor import preprocess

def preprocess_gencode_annotation(annotation_path, output_path):
    return preprocess(annotation_path, output_path)

def generate_coverage_matrix_with_read_ends(bam_file, annotation_file, k, output_file):
    pass
