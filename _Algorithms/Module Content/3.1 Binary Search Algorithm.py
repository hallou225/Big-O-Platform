def binary_search(arr, val):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == val:
            return mid
        elif arr[mid] < val
            left = mid + 1
        else:
            right = mid - 1
    return -1