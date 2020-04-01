import argparse
import numpy as np

def main(inputs, output, uint32):
    summary_matrix = np.load(inputs[0])
    if uint32 == True:
        dtype = np.uint32
        summary_matrix = summary_matrix.astype(dtype)
    else:
        dtype = summary_matrix.dtype
    for input_file in inputs:
        A = np.load(input_file).astype(dtype)
        summary_matrix += A
    print(summary_matrix.dtype)
    np.save(output, summary_matrix)

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description="This script will add rows in n coverage matrices in a lazy fashion"
    )
    parser.add_argument(
        "--inputs", help="File paths for the coverage matrices", nargs="+"
    )
    parser.add_argument(
        "output", help="File path to the output file"
    )
    parser.add_argument(
        "--uint32", help="Change the dtype of the matrices", action="store_true"  
    )
    args = parser.parse_args()
    main(args.inputs, args.output, args.uint32)
