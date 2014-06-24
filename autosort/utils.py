from collections import defaultdict


def interpose(lists, sep):
    result = []
    for lst in lists:
        if result:
            result.extend(sep)
        result.extend(lst)
    return result


def ordered_subgroups(items, key):
    result = defaultdict(list)
    for item in items:
        result[key(item)].append(item)

    return [result[k] for k in sorted(result.keys())]
