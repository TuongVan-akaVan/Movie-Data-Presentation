import pandas as pd

def load_data():
    links = pd.read_csv("./data/links.csv")
    movies = pd.read_csv("./data/movies.csv")
    ratings = pd.read_csv("./data/ratings.csv")
    tags = pd.read_csv("./data/tags.csv")
    return links, movies, ratings, tags

def get_basic_stats(links, movies, ratings, tags):
    stats = {}
    # Basic stats
    stats["total_movies"] = len(movies)
    stats["total_ratings"] = len(ratings)
    stats["total_unique_users"] = ratings["userId"].nunique()
    stats["total_tags"] = len(tags)
    return stats

def get_movies_table_stats(movies):
    """
    Top 10 most common genres
    Number of genres per movie (min, max, avg)
    Ex: most genre-diverse movies
    """
    stats = {}
    genres_series = movies["genres"].str.split("|").explode()
    stats["top_genres"] = genres_series.value_counts().head(10)
    genre_counts = movies["genres"].str.count("\|") + 1
    stats["genres_per_movie"] = {
        "min": genre_counts.min(),
        "max": genre_counts.max(),
        "avg": genre_counts.mean()
    }
    max_genre_count = genre_counts.max()
    stats["most_genre_diverse_movies"] = movies[genre_counts == max_genre_count][["title", "genres"]]
    return stats

def get_rating_table_stats(movies, ratings):
    """
    - Average rating overall
    - Rating distribution (histogram)
    - Most-rated movies (by count)
    - Top-rated movies (by avg rating, with min number of ratings threshold)
    - Most active users (by ratings count)
    """
    stats = {}
    stats["avg_rating_overall"] = ratings["rating"].mean()
    stats["rating_distribution"] = ratings["rating"].value_counts().sort_index()
    most_rated = ratings.groupby("movieId").size().sort_values(ascending=False)
    stats["most_rated_movies"] = movies.set_index("movieId").loc[most_rated.head(10).index][["title"]]
    top_rated = ratings.groupby("movieId").agg({"rating": "mean", "userId": "count"})
    top_rated = top_rated[top_rated["userId"] >= 100].sort_values("rating", ascending=False)
    stats["top_rated_movies"] = movies.set_index("movieId").loc[top_rated.head(10).index][["title"]]
    most_active_users = ratings.groupby("userId").size().sort_values(ascending=False)
    stats["most_active_users"] = most_active_users.head(10)
    return stats
  
def get_tag_table_stat(tags):
    """
    - Most common tags
    - Number of unique tags
    - Users who tagged the most movies
    """
    stats = {}
    stats["most_common_tags"] = tags["tag"].value_counts().head(10)
    stats["unique_tags_count"] = tags["tag"].nunique()
    user_tag_counts = tags.groupby("userId")["movieId"].nunique().sort_values(ascending=False)
    stats["top_tagging_users"] = user_tag_counts.head(10)
    return stats

def get_cross_table_stats(movies, ratings, tags):
    """
    - Ratings coverage: % of movies that have at least 1 rating
    - Tags coverage: % of movies that have at least 1 tag
    - Correlation between genres and average rating
    """
    stats = {}
    stats["ratings_coverage"] = ratings["movieId"].nunique() / len(movies) * 100
    stats["tags_coverage"] = tags["movieId"].nunique() / len(movies) * 100
    genre_avg_rating = ratings.merge(movies, on="movieId")
    genre_avg_rating = genre_avg_rating.assign(genres=genre_avg_rating["genres"].str.split("|")).explode("genres")
    stats["genre_rating_correlation"] = genre_avg_rating.groupby("genres")["rating"].mean().sort_values(ascending=False)
    return stats


