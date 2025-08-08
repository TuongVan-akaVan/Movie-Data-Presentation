# MovieLens Data Presentation Project

This project demonstrates Python and Pandas skills by presenting key statistics and summaries from the MovieLens dataset using a Streamlit dashboard.

## What It Shows

- Basic stats: total movies, ratings, users, tags, and missing TMDb IDs  
- Movies table insights: top 10 genres, genres per movie (min, max, avg), and most genre-diverse movies  
- Ratings table insights: average rating, rating distribution, most-rated and top-rated movies, most active users  
- Tags table insights: most common tags, unique tag count, top tagging users  
- Cross-table insights: coverage of ratings and tags across movies, and genre-average rating correlation  

## Skills Demonstrated

- Loading and handling CSV data with Pandas  
- Data aggregation, grouping, and filtering  
- String manipulation and exploding list-like columns  
- Merging datasets and calculating derived statistics  
- Presenting results interactively with Streamlit and Altair charts  
## Data Source

Download the dataset from Kaggle and place the data files into the `data` folder in the project.

Python script to download the dataset using `kagglehub`:

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("shubhammehta21/movie-lens-small-latest-dataset")

print("Path to dataset files:", path)
```

## Requirements
- Python 3+ 
- Pandas  
- Streamlit  
- Altair  


