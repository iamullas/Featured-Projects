from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Simulated user-movie rating data (rows: users, columns: movies)
ratings = np.array([
    [5, 4, 0, 0, 3],
    [4, 0, 5, 3, 4],
    [0, 5, 4, 4, 5],
    [3, 4, 0, 5, 0]
])

# Compute similarity between users
user_similarity = cosine_similarity(ratings)
