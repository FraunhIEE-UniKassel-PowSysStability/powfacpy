Module powfacpy.general_helpers
===============================

Functions
---------

`get_indices(subset: list, superset: list, large_list: bool = True) ‑> list[int]`
:   Get all indices in 'superset' of items in 'subset'.
    
    Args:
        subset (list): subset of superset
        superset (list): superset of subset
        large_list (bool, optional): If true, 'b' is converted to a dict first for O(1) lookups. Improves performance for large datasets. Defaults to True.
    
    Returns:
        list[int]: indices in superset