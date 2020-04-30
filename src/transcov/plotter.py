import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import math

from .utils import tsv_reader


def fetch_tss_ids(index_file):
    with open(index_file) as fp:
        reader = tsv_reader(fp)
        for line in reader:
            if line[0].startswith("#"):
                continue
            yield line[1]


def bin_columns_by_sum(X, bin_size):
    return bin_rows_by_sum(X.transpose(), bin_size).transpose()


def bin_rows_by_sum(X, bin_size):
    if bin_size == 1:
        return X
    old_n, m = X.shape
    n_floor = int(old_n / bin_size)
    remainder = old_n % bin_size
    if remainder == 0:
        return np.add.reduce(X.reshape(n_floor, bin_size, m), axis=1)
    else:
        A, B = np.vsplit(X, [old_n - remainder])
        return np.vstack(
            (
                np.add.reduce(A.reshape(n_floor, bin_size, m), axis=1),
                np.add.reduce(B, axis=0),
            )
        )

def create_interval_labels(start, stop, steps):
    left_interval = list(range(start, stop, steps))
    right_interval = left_interval[1:] + [stop]
    return (f'{a}-{b}' for a,b in zip(left_interval, right_interval))

def plot_end_length_frag_start_dist(tensor_file, output_file):
    tensor = np.load(tensor_file, allow_pickle=True)
    matrix = np.add.reduce(tensor, axis=0).toarray()
    n, m = matrix.shape
    column_bin_size = math.ceil(m / 67)
    row_bin_size = math.ceil(n / 50)
    matrix = bin_rows_by_sum(bin_columns_by_sum(matrix, column_bin_size), row_bin_size)
    matrix = pd.DataFrame(
        matrix,
        index=create_interval_labels(0, n, row_bin_size),
        columns=create_interval_labels(0, m, column_bin_size),
    )
    sns.set(rc={"figure.figsize": (20.0, 12.27)})
    ax = sns.heatmap(matrix)
    ax.collections[0].colorbar.set_label("counts")
    plt.xlabel("bp-position")
    plt.ylabel("Fragment length/bp")
    plt.savefig(output_file)


def plot_coverage_distribution(matrix_file, output_file):
    matrix = np.load(matrix_file)
    sns.distplot(np.add.reduce(matrix, axis=1))
    plt.savefig(output_file)
