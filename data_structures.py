"""
Examples of various data structures
"""


def do_binary_search(search_list, start, end, element):
    """
    Recursive function to do binary search
    :param search_list:
    :param start:
    :param end:
    :param element:
    :return:
    """
    pivot = int((start + end)/2)
    if search_list[pivot] == element:
        return pivot
    elif start == end:
        return None
    elif search_list[pivot] < element:
        return do_binary_search(search_list, start=pivot+1, end=end, element=element)
    elif search_list[pivot] > element:
        return do_binary_search(search_list, start=start, end=pivot-1, element=element)
    else:
        raise Exception("No Idea man")


def binary_search(search_list, element):
    """
    Function to find the index of the element in the list, if present using binary search
    :param search_list:
    :param element:
    :return:
    """
    start = 0
    end = len(search_list) - 1

    return do_binary_search(search_list, start, end, element)


# Example - Binary Search
print("Position of 5 in [1,2,3,4,5] is {}".format(binary_search([1,2,3,4,5], 5)))
print("Position of 6 in [1,2,3,4,5] is {}".format(binary_search([1,2,3,4,5], 6)))
print("Position of 2 in [1,2,3,4,5] is {}".format(binary_search([1,2,3,4,5], 2)))
