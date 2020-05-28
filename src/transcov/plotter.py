import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import math
from functools import partial, reduce
import operator

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

def plot_indecies(matrix, start, end):
    sns.set(rc={"figure.figsize": (100.0, 40.27)})
    ax = sns.heatmap(matrix[start:end])
    ax.collections[0].colorbar.set_label("counts")
    plt.xlabel("bp-position")
    plt.ylabel("Fragment length/bp")
    plt.savefig(output_file + f'{start}_{end}')

def plot_end_length_frag_start_dist(tensor_file, output_file):
    tensor = np.load(tensor_file, allow_pickle=True)
    matrix = np.add.reduce(tensor, axis=0).toarray()
    n, m = matrix.shape
    column_bin_size = math.ceil(m / 340)
    row_bin_size = math.ceil(n / 100)
    matrix = bin_rows_by_sum(bin_columns_by_sum(matrix, column_bin_size), row_bin_size)
    matrix = pd.DataFrame(
        matrix,
        index=create_interval_labels(0, n, row_bin_size),
        columns=create_interval_labels(0, m, column_bin_size),
    )
    print(matrix)
    sns.set(rc={"figure.figsize": (100.0, 40.27)})
    ax = sns.heatmap(matrix[:17])
    ax.collections[0].colorbar.set_label("counts")
    plt.xlabel("bp-position")
    plt.ylabel("Fragment length/bp")
    plt.savefig(output_file + f'first.png')
    plt.clf()
    ax = sns.heatmap(matrix[17:44])
    ax.collections[0].colorbar.set_label("counts")
    plt.xlabel("bp-position")
    plt.ylabel("Fragment length/bp")
    plt.savefig(output_file + f'midt.png')
    plt.clf()
    ax = sns.heatmap(matrix[44:])
    ax.collections[0].colorbar.set_label("counts")
    plt.xlabel("bp-position")
    plt.ylabel("Fragment length/bp")
    plt.savefig(output_file + f'last.png')

def prep_matrix_for_plot(matrix):
    n, m = matrix.shape
    column_bin_size = math.ceil(m / 340)
    row_bin_size = math.ceil(n / 100)
    matrix = bin_rows_by_sum(bin_columns_by_sum(matrix, column_bin_size), row_bin_size)
    return pd.DataFrame(
        matrix,
        index=create_interval_labels(0, n, row_bin_size),
        columns=create_interval_labels(0, m, column_bin_size),
    )

def norm_tensor(tensor):
    return tensor/np.sum(np.add.reduce(tensor))

def plot_end_length_frag_start_dist_diff(tensor_files, output_file):
    matrix  = reduce(operator.sub, map(np.add.reduce , map(norm_tensor, map(partial(np.load, allow_pickle=True), tensor_files))))
    print(matrix)
    matrix = prep_matrix_for_plot(matrix.toarray())
    print(matrix)
    sns.set(rc={"figure.figsize": (100.0, 40.27)})
    ax = sns.heatmap(matrix[:17], cmap="RdBu", center=0)
    ax.collections[0].colorbar.set_label("counts")
    plt.xlabel("bp-position")
    plt.ylabel("Fragment length/bp")
    plt.savefig(output_file + f'short.png')
    plt.clf()
    ax = sns.heatmap(matrix[17:44], cmap="RdBu", center=0)
    ax.collections[0].colorbar.set_label("counts")
    plt.xlabel("bp-position")
    plt.ylabel("Fragment length/bp")
    plt.savefig(output_file + f'midt.png')
    plt.clf()
    ax = sns.heatmap(matrix[44:], cmap="RdBu", center=0)
    ax.collections[0].colorbar.set_label("counts")
    plt.xlabel("bp-position")
    plt.ylabel("Fragment length/bp")
    plt.savefig(output_file + f'last.png')
    plt.clf()
    ax = sns.heatmap(matrix, cmap="RdBu", center=0)
    ax.collections[0].colorbar.set_label("counts")
    plt.xlabel("bp-position")
    plt.ylabel("Fragment length/bp")
    plt.savefig(output_file)


def plot_coverage_distribution(matrix_file, output_file):
    matrix = np.load(matrix_file)
    sns.distplot(np.add.reduce(matrix, axis=1))
    plt.savefig(output_file)
