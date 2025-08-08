import streamlit as st
import altair as alt
import pandas as pd
from analyzer import load_data, get_basic_stats, get_movies_table_stats, get_rating_table_stats, get_tag_table_stat, get_cross_table_stats

def bar_chart_with_labels(data, x_col, y_col, x_title, y_title, width=500, height=300):
    if isinstance(data, pd.Series):
        df = data.reset_index()
        df.columns = [x_col, y_col]
    else:
        df = data.copy()
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_col, title=x_title),
        y=alt.Y(y_col, title=y_title)
    ).properties(width=width, height=height)
    st.altair_chart(chart, use_container_width=True)

def show_basic_stats(stats):
    cols = st.columns(4)
    cols[0].metric("Total Movies", stats["total_movies"])
    cols[1].metric("Total Ratings", stats["total_ratings"])
    cols[2].metric("Unique Users", stats["total_unique_users"])
    cols[3].metric("Total Tags", stats["total_tags"])

def show_movies_insights(stats):
    st.markdown("---")
    st.header("⭐ Movies Table Insights")
    # average stats
    c1, spacer, c2 = st.columns([4, 1, 4])
    with c1:
        st.subheader("Top 10 Most Common Genres")
        bar_chart_with_labels(stats["top_genres"], 'Genre', 'Count', "Genre", "Count")
    with c2:
        st.subheader("Genres per Movie Summary")
        stats_dict = stats["genres_per_movie"]
        st.write("")  # add vertical space
        cols = st.columns(3)
        labels = ["Min Genres per Movie", "Max Genres per Movie", "Avg Genres per Movie"]
        values = [stats_dict["min"], stats_dict["max"], f"{stats_dict['avg']:.2f}"]
        for col, label, value in zip(cols, labels, values):
            col.markdown(f"**{label}**")
            col.metric(label="", value=value)
    # Movie with the most genres
    df = stats["most_genre_diverse_movies"]
    max_genres = df.iloc[0]["genres"].count("|") + 1 if not df.empty else 0
    st.subheader(f"Most Genre-Diverse Movies: {max_genres} genres")
    for _, row in df.iterrows():
        st.markdown(f"**{row['title']}** — Genres: {row['genres']}")

def show_ratings_insights(stats):
    st.markdown("---")
    st.header("⭐ Ratings Table Insights")
    # chart part
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Average Rating", round(stats["avg_rating_overall"], 2))
        st.subheader("Rating Distribution")
        bar_chart_with_labels(stats["rating_distribution"], 'Rating', 'Count', "Rating", "Count")
    with c2:
        st.subheader("Most Active Users")
        bar_chart_with_labels(stats["most_active_users"], 'User ID', 'Ratings Count', "User ID", "Ratings Count")
    st.subheader("Top Movies Overview")
    # top list part
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Most Rated Movies (Top 10)**")
        most_rated = stats["most_rated_movies"]
        for i, (movieId, row) in enumerate(most_rated.iterrows(), 1):
            st.markdown(f"{i}. {row['title']} (ID: {movieId})")
    with c4:
        st.markdown("**Top Rated Movies (Top 10)**")
        top_rated = stats["top_rated_movies"]
        for i, (movieId, row) in enumerate(top_rated.iterrows(), 1):
            st.markdown(f"{i}. {row['title']} (ID: {movieId})")

def show_tags_insights(stats):
    st.markdown("---")
    st.header("⭐ Tags Table Insights")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Most Common Tags")
        bar_chart_with_labels(stats["most_common_tags"], 'Tag', 'Count', "Tag", "Count")
    with c2:
        st.metric("Unique Tags", stats["unique_tags_count"])
        st.subheader("Top Tagging Users")
        bar_chart_with_labels(stats["top_tagging_users"], 'User ID', 'Movies Tagged', "User ID", "Movies Tagged")

def show_cross_table_insights(stats):
    st.markdown("---")
    st.header("⭐ Cross-Table Insights")
    cols = st.columns(2)
    cols[0].write("Percentage of movies with at least one rating")
    cols[1].write("Percentage of movies with at least one tag")
    cols[0].metric("Ratings Coverage (%)", f"{stats['ratings_coverage']:.1f}")
    cols[1].metric("Tags Coverage (%)", f"{stats['tags_coverage']:.1f}")
    st.subheader("Average Rating per Genre")
    bar_chart_with_labels(stats["genre_rating_correlation"], 'Genre', 'Average Rating', "Genre", "Average Rating")

def main():
    st.set_page_config(page_title="MovieLens Data Dashboard", layout="wide")
    # get statistics data from 4 data files
    links, movies, ratings, tags = load_data()
    basic_stats = get_basic_stats(links, movies, ratings, tags)
    movies_stats = get_movies_table_stats(movies)
    rating_stats = get_rating_table_stats(movies, ratings)
    tag_stats = get_tag_table_stat(tags)
    cross_table_stats = get_cross_table_stats(movies, ratings, tags)
    # visual presentation
    st.title("MovieLens Data Dashboard")
    st.caption("Quick facts and summaries from the dataset")
    # component of layout
    show_basic_stats(basic_stats)
    show_movies_insights(movies_stats)
    show_ratings_insights(rating_stats)
    show_tags_insights(tag_stats)
    show_cross_table_insights(cross_table_stats)

if __name__ == "__main__":
    main()




