from numpy import array


def sampling(data, sample_size):
    samples = list()
    for i in range(0, len(data), sample_size):
        sample = data[i:i+sample_size]
        samples.append(sample)
    data = array(samples)
    data = data.reshape((len(samples), sample_size, 1))
    return data
