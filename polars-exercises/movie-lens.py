import polars as pl
import pandas as pd

from lets_plot import *

LetsPlot.setup_html(no_js=True, show_status=False, isolated_frame=True, offline=True)

unames = ["user_id", "gender", "age", "occupation", "zip"]
# users = pl.from_pandas(
#     pd.read_table("users.dat", header=None, sep="::", names=unames, engine="python")
# )
# users.write_csv("users.csv")

users = pl.read_csv("users.csv", infer_schema_length=10000)

rnames = ["user_id", "movie_id", "rating", "timestamp"]
# ratings = pl.from_pandas(
#     pd.read_table(
#         "ratings.dat",
#         sep="::",
#         header=None,
#         names=rnames,
#         engine="python",
#     )
# )
# ratings.write_csv("ratings.csv")
ratings = pl.read_csv("ratings.csv", infer_schema_length=10000)

mnames = ["movie_id", "title", "genres"]
# movies = pl.from_pandas(
#     pd.read_table(
#         "movies.dat",
#         sep="::",
#         header=None,
#         names=mnames,
#         engine="python",
#     )
# )
# movies.write_csv("movies.csv")
movies = pl.read_csv("movies.csv", infer_schema_length=10000)

# Check unique id

users["user_id"].is_duplicated().any()
movies["movie_id"].is_duplicated().any()


dta = ratings.join(users, on="user_id").join(movies, on="movie_id")

dta.shape
# (1000209, 10)

dta.head()

avg_ratings = dta.pivot(
    index="title", columns="gender", values="rating", aggregate_function="mean"
)

# movies that had at least 250 ratings

active_titles = (
    dta.group_by("title")
    .agg(no_ratings=pl.len())
    .filter(pl.col("no_ratings") >= 250)
    .sort("no_ratings")
)

avg_ratings = avg_ratings.filter(pl.col("title").is_in(active_titles["title"]))


# top films among female viewers

avg_ratings.top_k(10, by="F")

avg_ratings.top_k(10, by="M")

# Measuring rating disagreement

avg_ratings = avg_ratings.with_columns(diff=(pl.col("M") - pl.col("F")))

sorted_by_diff = avg_ratings.sort("diff", descending=True)

sorted_by_diff.head()

# movies that elicited the most disagreement among viewers, independent of gender identification

rating_std_by_title = dta.group_by("title").agg(rating_std=pl.col("rating").std())

rating_std_by_title = rating_std_by_title.filter(
    pl.col("title").is_in(active_titles["title"])
)

rating_std_by_title.head()

rating_std_by_title.top_k(10, by="rating_std")

movies_exploded = movies.with_columns(pl.col("genres").str.split("|")).explode("genres")


ratings_with_genre = movies_exploded.join(ratings, on="movie_id", how="left").join(
    users, on="user_id", how="left"
)

(
    ratings_with_genre.group_by(["genres", "age"])
    .agg(pl.col("rating").mean())
    .pivot(index="genres", columns="age", values="rating")
)
