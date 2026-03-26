import pandas as pd

def compare_versions(data1, data2):
    """
    Compares two lists of dictionaries (Excel data).
    Detects added, removed, and modified rows.
    """
    added = []
    removed = []
    modified = []

    # Identify a common key if possible
    key = None
    if data1 and data2:
        keys1 = set(data1[0].keys())
        keys2 = set(data2[0].keys())
        common_keys = keys1.intersection(keys2)
        
        for k in ['ID', 'id', 'Id', 'S.No', 'Serial No']:
            if k in common_keys:
                key = k
                break
    
    if key:
        # Map data by key for faster lookup
        map1 = {row[key]: row for row in data1 if key in row}
        map2 = {row[key]: row for row in data2 if key in row}
        
        all_ids = set(map1.keys()).union(set(map2.keys()))
        
        for row_id in all_ids:
            if row_id not in map1:
                added.append(map2[row_id])
            elif row_id not in map2:
                removed.append(map1[row_id])
            else:
                # Both exist, check for modifications
                if map1[row_id] != map2[row_id]:
                    # Find specific column changes
                    changes = {}
                    for k in map1[row_id]:
                        if k in map2[row_id] and map1[row_id][k] != map2[row_id][k]:
                            changes[k] = {
                                "old": map1[row_id][k],
                                "new": map2[row_id][k]
                            }
                    modified.append({
                        "key": key,
                        "id": row_id,
                        "changes": changes
                    })
    else:
        # No key found, use simple set-based comparison for added/removed
        # This treats each row as a whole.
        str_data1 = [str(r) for r in data1]
        str_data2 = [str(r) for r in data2]
        
        # This is very basic and won't detect "modified" accurately without a key
        # Rows that are different are just "removed from v1" and "added to v2"
        for i, r2 in enumerate(data2):
            if r2 not in data1:
                added.append(r2)
        
        for i, r1 in enumerate(data1):
            if r1 not in data2:
                removed.append(r1)

    return {
        "added": added,
        "removed": removed,
        "modified": modified
    }
