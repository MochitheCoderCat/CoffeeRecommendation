'''
# Using KNN model
Calculation the distance between one coffee bean and all other coffee beans, return the top10 nearest neighbors.
*   For a single coffee bean: Recommend the highest-rated coffee bean among the top10 nearest neighbors.
*   For two coffee beans:
If there is an overlap between the 2 sets of top10 nearest neighbors for each inputted coffee beans, recommend the highest-rated coffee bean in the overlap.
If no overlap, combine the two sets of nearest neighbors and recommend the highest-rated coffee bean among all 20 neighbors
'''

# Load the pre-exported dictionary
from joblib import load

# Load the KNN model
nearest_neighbors = load('./model/knn_model.joblib')
clusters_dict = load('./model/kmeans_model.joblib')


def recommend_knn(user_input_names):
    if len(user_input_names) == 1:
        # Single input: Recommend the highest-rated neighbor
        coffee_name = user_input_names[0]
        neighbors = nearest_neighbors[coffee_name]["neighbors"]
        ratings = nearest_neighbors[coffee_name]["ratings"]
        highest_rated_idx = ratings.index(max(ratings))
        return neighbors[highest_rated_idx]

    elif len(user_input_names) == 2:
        # Two inputs: Check for overlap
        coffee_1, coffee_2 = user_input_names
        neighbors_1 = set(nearest_neighbors[coffee_1]["neighbors"])
        neighbors_2 = set(nearest_neighbors[coffee_2]["neighbors"])

        overlap = neighbors_1.intersection(neighbors_2)
        if overlap:
            # Recommend the highest-rated coffee in the overlap
            overlap_ratings = [(name, nearest_neighbors[name]["ratings"][0]) for name in overlap]
            return max(overlap_ratings, key=lambda x: x[1])[0]
        else:
            # Recommend the highest-rated coffee among all 20 neighbors
            combined_neighbors = list(neighbors_1.union(neighbors_2))
            combined_ratings = [(name, nearest_neighbors[name]["ratings"][0]) for name in combined_neighbors]
            return max(combined_ratings, key=lambda x: x[1])[0]


def recommend_kmeans(user_input_names):
    input_clusters = set()
    relevant_beans = []

    for name in user_input_names:
        # Add the cluster ID to input_clusters
        input_clusters.add(clusters_dict[name]["cluster"])

        # Add all neighbors to relevant beans
        neighbors = clusters_dict[name]["neighbors"]
        ratings = clusters_dict[name]["ratings"]
        relevant_beans.extend(zip(neighbors, ratings))

    # Filter unique beans if input clusters are different
    if len(input_clusters) > 1:
        # Deduplicate neighbors
        relevant_beans = list({bean[0]: bean for bean in relevant_beans}.values())

    # Recommend the highest-rated coffee bean
    recommended_bean = max(relevant_beans, key=lambda x: x[1])
    return recommended_bean[0]



# Example usage
# user_input_1 = ["Kenya Nyeri AA Ichuga"]
# user_input_2 = ["Kenya Nyeri AA Ichuga", "Ethiopia Yirgacheffe"]

# print("Recommended coffee bean for single input:", recommend_knn(user_input_1))
# print("Recommended coffee bean for two inputs:", recommend_knn(user_input_2))


# Example usage
# user_input_1 = ["Kenya Nyeri AA Ichuga"]  # Single coffee bean name input
# user_input_2 = ["Kenya Nyeri AA Ichuga", "Ethiopia Yirgacheffe"]  # Two coffee bean names input

# print("Recommended coffee bean for single input:", recommend_kmeans(user_input_1))
# print("Recommended coffee bean for two inputs:", recommend_kmeans(user_input_2))