import lux
def get_hash(vis:lux.vis.Vis)-> str:
    # Get the visualization hash for a Vis object
    # Vis(...) --> 'Vis  (x: reviews_per_month, y: number_of_reviews)'
    vis_hash = vis.__repr__()
    return vis_hash.split("mark")[0][1:-1]
def convert_vlist_to_hashmap(vlist):
    # Convert VisList to dictionary representation
    # {'Vis  (x: ..., y: ...)': 0.55,
    #  'Vis  (x: ..., y: ...)': 0.22,
    #   ...}
    vdict = {}
    for vis in vlist:
        vdict[get_hash(vis)]=vis.score
    return vdict

def get_aligned_dict(vdict,global_map):
    # Align each vdict based on global map
    aligned_dict = {}
    for vis in global_map: 
        if vis in vdict:
            aligned_dict[vis] = vdict[vis]
        else:
            aligned_dict[vis] = 0
    return aligned_dict

import numpy as np
def dcg(r, k, method=0,debug=False):
    # alternative formulation of DCG places stronger emphasis on retrieving relevant documents
    r = np.asfarray(r)[:k]
    val = 0
    for i in range(1,len(r)+1):
        val+= (r[i-1]) / np.log2(i+1)
        if debug:
            print ("i=",i,":",(r[i-1]) ,"/", np.log2(i+1))
            print ((r[i-1]) / np.log2(i+1))
    return val

def ndcg(ground_truth_r,r, k,debug=False):
    return dcg(r, k,debug=debug) / dcg(ground_truth_r,k,debug=debug)

def compute_ndcg_between_vislists(l1:lux.vis.VisList,l2:lux.vis.VisList) -> float:
    l1_scores= [vis.score for vis in l1] 
    map1 = convert_vlist_to_hashmap(l1)

    l2_scores= [vis.score for vis in l2] 
    map2 = convert_vlist_to_hashmap(l2)

    # Combine two dictionaries map1,map2 into a single global_map
    global_map = set(map1.keys())
    global_map.update(set(map2.keys()))
    global_map = list(global_map)

    aligned_score1 = list(get_aligned_dict(map1,global_map).values())
    aligned_score2 = list(get_aligned_dict(map2,global_map).values())

    from scipy.stats import stats
    rank1 = stats.rankdata(aligned_score1)
    rank2 =stats.rankdata(aligned_score2)

    return ndcg(rank1,rank2,3) 
# Tests
# ground_truth_ratings = [1,2,3,4,5,6]
# example_ratings = [3,2,3,0,1,2]
# ideal_ordering = [3,3,3,2,2,2,1,0]
# assert np.isclose(dcg(example_ratings,6),6.861,1e-2) #check DCG calculation (Based on Wikipedia example)
# assert np.isclose(ndcg(ideal_ordering,[3,2,3,0,1,2],6),0.785,1e-2) #check NDCG calculation (Based on Wikipedia example)
# assert np.isclose(ndcg([3,1,2],[3, 1, 2],3),1) #sanity check