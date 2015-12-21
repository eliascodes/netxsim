def count_num_samples(samples, mean, sigma_level):
    count = 0
    for sample in samples:
        if sample < mean+sigma_level and sample > mean-sigma_level:
            count += 1
    return count
