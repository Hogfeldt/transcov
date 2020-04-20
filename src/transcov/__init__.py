from .generator import generate_coverage_matrix, generate_read_ends_matrix, generate_length_matrix
from .preprocessor import preprocess
from .manipulations import collapse, pick_subset

__version__ = "1.0.4"

__all__ =  ("generate_coverage_matrix", 
            "generate_read_ends_matrix", 
            "generate_length_matrix", 
            "preprocess", 
            "collapse",
            "pick_subset",)
