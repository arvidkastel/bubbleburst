import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import twitter
import json
from math import sqrt
import time
import sys

api = twitter.Api(
    consumer_key='pMHK2JWh84BLy0e0gPkEiJUT1',
    consumer_secret='JRUuAmOVY79NBfAh8xFC0XUqTEG6VElQGkRlMPI9e0EE4R3dnH',
    access_token_key='20718078-go8p0Nv6PXqQ4x5X2J0OESABSnif4blDeOJQKC1oL',
    access_token_secret='pjggss6g9eNAGjdUAM2xlrBF3EWnzmbS3RkLSn2hcyIcB'
)

with open('usernames.json') as data_file:
    screen_names = json.load(data_file)

try:
    with open('users.json') as data_file:
        users = json.load(data_file)
except:
    users = []

def write_users(usersarg):
    print "saving users"
    with open('users.json', 'w') as outfile:
        json.dump(usersarg, outfile, sort_keys=True, indent=4, separators=(',', ': '));
def loadUserData(screen_name):
    print "loading: " + screen_name 
    try:
        user = api.UsersLookup(screen_name=screen_name)[0]
        users.append({
            'uid': user.id,
            'screen_name': screen_name,
            'friends': api.GetFriendIDs(
                screen_name=screen_name, 
                stringify_ids=True
            )
        })
    except twitter.error.TwitterError as e:
        print e
        write_users(users)
        time.sleep(10*60)
        loadUserData(screen_name)

loaded_screen_names = [user['screen_name'] for user in users]
not_loaded_screen_names = [screen_name for screen_name in screen_names if not screen_name in loaded_screen_names]
for screen_name in not_loaded_screen_names:
    loadUserData(screen_name)

write_users(users)
def intersect(a, b):
    return list(set(a) & set(b))

def similarity(u1, u2):
    commonFriends = intersect(u1['friends'], u2['friends'])

    sim = len(commonFriends) / sqrt(len(u1['friends']) * len(u2['friends']))
    return sim

def computeSimilarityMatrix():
    matrix = []
    for user1 in users:
        column = []
        for user2 in users:
            column.append(similarity(user1, user2))
        matrix.append(column)
    return matrix


similarityMatrix = computeSimilarityMatrix()
#print similarityMatrix

eig_vals, eig_vecs = np.linalg.eig(similarityMatrix)

# eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]
# for i in eig_pairs:
#     print(i[0])

# print 

def rowForScreenName(screen_name):
    for i in range(len(users)):
        if users[i]['screen_name'] == screen_name:
            return i
    return Null
def screenNameForRow(row):
    return users[row]['screen_name']

def mostSimilarAccounts(screen_name):
    ix = rowForScreenName(screen_name)
    pairs = [(i, similarityMatrix[ix][i]) for i in range(len(users))]
    pairs.sort(key=lambda pair: -pair[1])
    return [screenNameForRow(pair[0]) for pair in pairs]


print mostSimilarAccounts('annieloof')
print eig_vecs[0,:]
plt.scatter(eig_vecs[:,0],eig_vecs[:,1])
for i in range(len(eig_vals)):
    plt.annotate(users[i]['screen_name'], xy=(eig_vecs[i,0],eig_vecs[i,1]))
plt.show()