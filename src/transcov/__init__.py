from .generator import generate_coverage_matrix, generate_read_ends_matrix, generate_length_matrix
from .preprocessor import preprocess
from .collapser import collapse

__version__ = "1.0.4"

__all__ = ("generate_coverage_matrix", "preprocess", "collapse")
