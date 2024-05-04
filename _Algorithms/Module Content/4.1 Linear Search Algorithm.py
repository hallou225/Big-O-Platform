def linear_search(arr, val):
    for i in range(0, len(arr)):
        if arr[i] == val:
            return i
    return -1