import argparse
import numpy as np


def collapse(matrices, output_file, start=0, end=None, uint32=False):
    """ This function will given a list of matrices, load in the matrices one by
        one and collapse them upon each other value by value.
        The final matrix will be stored in the output file as a .npy file

        Use start and end if you want to only collapse and output a certain region.

        :param matrices: List of file paths to matrices, that should be collapsed
        :type matrices: List(str)
        :param output_file: File path to the output file
        :type output_file: str
        :param start: start index for collapsing
        :type start: int >= 0
        :param end: end index for collapsing, if None then last index is end.
        :type end: int >= 0
        :param uint32: If False numpy.dtype will be preserved, if True numpy.dtype will be changed to uint32
        :type output_file: boolean
        :returns:  None
    """
    summary_matrix = np.load(matrices[0])
    if end == None:
        _, end = summary_matrix.shape
    summary_matrix = summary_matrix[:,start:end]
    if uint32 == True:
        dtype = np.uint32
        summary_matrix = summary_matrix.astype(dtype)
    else:
        dtype = summary_matrix.dtype
    if len(matrices) > 1:
        for input_file in matrices[1:]:
            A = np.load(input_file).astype(dtype)[:,start:end]
            summary_matrix += A
    np.save(output_file, summary_matrix)
