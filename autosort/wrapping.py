def _dynamic_wrap(items, limit):
    scores, trace = [0], []
    for j in range(len(items)):
        best, psum, index = 0, limit, -1
        for i in reversed(range(j + 1)):
            psum -= items[i]
            score = scores[i] + psum ** 2
            if i == j or score < best and psum >= 0:
                best = score
                index = i

        scores.append(best)
        trace.append(index)

    return _build_indices(trace)


def _build_indices(trace):
    indices, index = [], len(trace) - 1
    while index >= 0:
        indices.append((trace[index], index + 1))
        index = trace[index] - 1

    return indices[::-1]
