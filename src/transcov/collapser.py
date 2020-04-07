import argparse
import numpy as np


def collapse(matrices, output_file, uint32=False):
    """ This function will given a list of matrices, load in the matrices one by
        one and collapse them upon each other value by value.
        The final matrix will be stored in the output file as a .npy file

        :param matrices: List of file paths to matrices, that should be collapsed
        :type matrices: List(str)
        :param output_file: File path to the output file
        :type output_file: str
        :param uint32: If False numpy.dtype will be preserved, if True numpy.dtype will be changed to uint32
        :type output_file: boolean
        :returns:  None
    """
    print(matrices)
    print(output_file)
    summary_matrix = np.load(matrices[0])
    if uint32 == True:
        dtype = np.uint32
        summary_matrix = summary_matrix.astype(dtype)
    else:
        dtype = summary_matrix.dtype
    if len(matrices) > 1:
        for input_file in matrices[1:]:
            A = np.load(input_file).astype(dtype)
            summary_matrix += A
    np.save(output_file, summary_matrix)
