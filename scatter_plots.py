__author__ = 'slyfocks'
import numpy as np
import mlpy
import matplotlib.pyplot as plt
import house_similarities as hs
import most_least


def make_scatter(congress_num):
    fig = plt.figure(1)
    arr = hs.make_similarity_array(congress_num)
    cls, means, steps = mlpy.kmeans(arr, k=2, plus=True)
    members = hs.members(congress_num)
    extreme_index1 = members.index(most_least.most_extreme(congress_num, 10)[0])
    extreme_index2 = list(arr[extreme_index1]).index(min(arr[extreme_index1]))
    if members[extreme_index1].split(' ')[1] == 'R':
        for i in range(len(cls)):
            if cls[i] == 0:
                cls[i] = 1
            else:
                cls[i] = 0
        plot = plt.scatter(arr[:, extreme_index1], arr[:, extreme_index2], c=cls, alpha=0.75)
        plt.xlabel("Conservatism (Cosine similarity to most conservative member, "
                   + members[extreme_index1].split(' ')[0] + ")")
        plt.ylabel("Liberalism (Cosine similarity to most liberal member, "
                   + members[extreme_index2].split(' ')[0] + ")")
    else:
        plot = plt.scatter(arr[:, extreme_index2], arr[:, extreme_index1], c=cls, alpha=0.75)
        plt.ylabel("Liberalism (Cosine similarity to most liberal member, "
                   + members[extreme_index1].split(' ')[0] + ")")
        plt.xlabel("Conservatism (Cosine similarity to most conservative member, "
                   + members[extreme_index2].split(' ')[0] + ")")
    return


def main():
    #set congress_num variable to any integer in [104,113]
    CONGRESS_NUM = 104
    make_scatter(CONGRESS_NUM)
    plt.savefig(str(CONGRESS_NUM) + 'similarity.png')

if __name__ == "__main__":
    main()