import argparse
import numpy as np
from functools import partial
from itertools import tee, count

from .utils import tsv_reader, write_matrix_and_index_file

def create_index_map(index_file):
    index_map = dict()
    with open(index_file) as fp:
        for line in tsv_reader(fp):
            if line[0].startswith('#'):
                continue
            index_map[line[1]] = int(line[0])
    return index_map

def pick_subset_by_row_index(X, index_pairs, n):
    _, m = X.shape
    A = np.zeros((n, m), dtype=X.dtype)
    for i, j in index_pairs:
        A[i] = X[j]
    return A

pairing = lambda index_map, row_id: (row_id, index_map[row_id])

def unzip_pair_iter(it):
    it1, it2  = tee(it)
    first_it  = (a for a, b in it1)
    second_it = (b for a, b in it2)
    return (first_it, second_it)

def get_id_index_pair_iters(index_map, ids):
    pair_iter = map(partial(pairing, index_map), ids)
    ids_iter, index_iter = unzip_pair_iter(pair_iter)
    new_index_id_pairs = zip(count(), ids_iter)
    new_old_index_pairs = zip(count(), index_iter)
    return (new_index_id_pairs, new_old_index_pairs)

def pick_subset(matrix_file, index_file, output_file, ids):
    """ Given a matrix and a list of row identifiers, create a 
        new matrix which is a row-wise subset of the given matrix.

        :param matrix_file: File path to the input matrix
        :type matrix_file: str
        :param index_file: File path to the index file which coresponds to the input matrix
        :type index_file: str
        :param output_file: File path to the output matrix
        :type output_file: str
        :param ids: List of row identifiers for the input matrix
        :type start: List[str]
        :returns:  None
    """
    matrix = np.load(matrix_file)
    index_map = create_index_map(index_file)
    new_index_id_pairs, new_old_index_pairs = get_id_index_pair_iters(index_map, ids)
    sub_matrix = pick_subset_by_row_index(matrix, new_old_index_pairs, len(ids))
    write_matrix_and_index_file(output_file, sub_matrix, new_index_id_pairs)

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
