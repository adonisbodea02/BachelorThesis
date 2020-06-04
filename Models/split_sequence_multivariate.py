from numpy import array


# split a univariate sequence into samples
def split_sequence_multivariate(data, n_steps):
    x, y = list(), list()
    for i in range(len(data)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(data)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = data[i:end_ix], data[end_ix][0]
        x.append(seq_x)
        y.append(seq_y)
    return array(x), array(y)
