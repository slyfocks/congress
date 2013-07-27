__author__ = 'slyfocks'
import simplejson as json
import fnmatch
import os
import numpy as np


#returns list of bills and committees for any congress number from 106 to 113
def bill_committees(congress_num):
    path = str(congress_num) + '/bills'
    files = [os.path.join(dirpath, f)
                for dirpath, dirnames, files in os.walk(path)
                    for f in fnmatch.filter(files, 'data.json')]
    bill_committees = {}
    for file in files:
        json_data = open(file).read()
        data = json.loads(json_data)
        bill_id = data["bill_id"]
        # get committee codes with duplicates removed
        committees = sorted(set([committee['committee_id']
                            for committee in data['committees']]))
        bill_committees.update({bill_id: committees})
    return bill_committees


#returns dictionary with members and their vote (Yea = 1, Nay = -1, Present/Not Voting = 0)
def vote_tally(congress_num):
    committee_votes = {}
    member_votes = {}
    path = str(congress_num) + '/votes'
    files = [os.path.join(dirpath, f) for dirpath, dirnames, files
             in os.walk(path) for f in fnmatch.filter(files, 'data.json')]
    for file in files:
        json_data = open(file).read()
        data = json.loads(json_data)
        #some of the votes are on procedural things and not bills...we don't want these
        try:
            bill_id = data['bill']['type'] + str(data['bill']['number']) + '-' + str(congress_num)
        except KeyError:
            continue
        #silly data uses two synonymous pairs for Yes and No...
        if 'No' in data['votes']:
            nays = [member['display_name'] for member in data['votes']['No']]
            yeas = [member['display_name'] for member in data['votes']['Aye']]
        else:
            nays = [member['display_name'] for member in data['votes']['Nay']]
            yeas = [member['display_name'] for member in data['votes']['Yea']]
        not_voting = [member['display_name'] for member in data['votes']['Not Voting']]
        presents = [member['display_name'] for member in data['votes']['Present']]
        for member in nays:
            member_votes.setdefault(member, []).append(-1)
        for member in yeas:
            member_votes.setdefault(member, []).append(1)
        for member in not_voting or presents:
            member_votes.setdefault(member, []).append(0)
        #for committee in bill_committees(congress_num)[bill_id]:
            #committee_votes.update({committee: member_votes})
    return member_votes


def cos_similarity(x, y):
    X = np.array(x)
    Y = np.array(y)
    #if they're not equal in size, an error does arise
    if len(X) > len(Y):
        Y.resize(len(X))
        dot_product = np.vdot(X, Y)
    else:
        X.resize(len(Y))
        dot_product = np.vdot(X, Y)
    norm_x = np.vdot(X, X)
    norm_y = np.vdot(Y, Y)
    #cosine similarity formula
    return dot_product/np.sqrt(norm_x*norm_y)


def members(congress_num):
    return sorted(vote_tally(congress_num).keys())


def votes(congress_num):
    vote_list = vote_tally(congress_num)
    return [vote_list[member] for member in members(congress_num)]


def make_similarity_array(congress_num):
    vote_list = votes(congress_num)
    arr = np.zeros((435, 435))
    for i in range(435):
        for j in range(435):
            arr[i][j] = cos_similarity(vote_list[i], vote_list[j])
    return arr
def main():
    #set congress_num variable to any integer in [106,113]
    CONGRESS_NUM = 112
    np.savetxt('array' + str(CONGRESS_NUM) + '.txt', make_similarity_array(CONGRESS_NUM))

if __name__ == "__main__":
    main()
