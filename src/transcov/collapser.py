import argparse
import numpy as np

def collapse(inputs, output, uint32=False):
    summary_matrix = np.load(inputs[0])
    if uint32 == True:
        dtype = np.uint32
        summary_matrix = summary_matrix.astype(dtype)
    else:
        dtype = summary_matrix.dtype
    if len(inputs) > 1:
        for input_file in inputs[1]:
            A = np.load(input_file).astype(dtype)
            summary_matrix += A
    print(summary_matrix.dtype)
    np.save(output, summary_matrix)
