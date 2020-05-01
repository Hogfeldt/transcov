from .generator import (
    generate_coverage_matrix,
    generate_read_ends_matrix,
    generate_length_matrix,
    generate_end_length_tensor,
)
from .preprocessor import preprocess
from .manipulations import collapse, pick_subset, cut_tails_left, cut_tails_right, cut_tails_both
from .plotter import plot_end_length_frag_start_dist, plot_coverage_distribution

__version__ = "1.1.2"

__all__ = (
    "generate_coverage_matrix",
    "generate_read_ends_matrix",
    "generate_length_matrix",
    "generate_end_length_tensor",
    "preprocess",
    "collapse",
    "pick_subset",
    "cut_tails_both",
    "cut_tails_right",
    "cut_tails_both",
    "plot_end_length_frag_start_dist", 
    "plot_coverage_distribution",
)
