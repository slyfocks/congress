__author__ = 'slyfocks'

import house_similarities as hs


def most_unique(congress_num, knn):
    arr = hs.make_similarity_array(congress_num)
    congresspeople = hs.members(congress_num)
    #takes k-nearest members in cos similarity
    sorted_similarity = [sorted(arr[i])[-knn:] for i in range(len(arr[0]))]
    sums = [sum(sorted_similarity[i]) for i in range(len(sorted_similarity))]
    sorted_unique = sorted(range(len(sums)), key=lambda k: sums[k])
    unique_rank = [(congresspeople[index]) for index in sorted_unique]
    return unique_rank


def most_extreme(congress_num, knn):
    arr = hs.make_similarity_array(congress_num)
    congresspeople = hs.members(congress_num)
    #takes k-furthest members in cos similarity
    sorted_similarity = [sorted(arr[i])[:knn] for i in range(len(arr[0]))]
    #sums those similarities
    sums = [sum(sorted_similarity[i]) for i in range(len(sorted_similarity))]
    #sorts members from lowest to highest
    sorted_extreme = sorted(range(len(sums)), key=lambda k: sums[k])
    extreme_rank = [(congresspeople[index]) for index in sorted_extreme]
    return extreme_rank


def nadler_index(congress_num, knn):
    arr = hs.make_similarity_array(congress_num)
    unique_rank = most_unique(congress_num, knn)
    nadler_array = [arr[index][303] for (index, congressperson) in unique_rank]
    return nadler_array

