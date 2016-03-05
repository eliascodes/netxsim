"""

"""


def dict_lists_to_list_dicts(d):
    return map(dict, zip(*[[(key, val) for val in val_list] for key, val_list in d.items()]))
