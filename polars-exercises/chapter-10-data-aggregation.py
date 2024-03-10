# This is a polars' port of chapter 10 in Pandas book
# Source: https://wesmckinney.com/book/data-aggregation

import polars as pl
import numpy as np
import polars.selectors as cs

np.random.seed(123)

df = pl.DataFrame(
    {
        "key1": ["a", "a", None, "b", "b", "a", None],
        "key2": pl.Series([1, 2, 1, 2, 1, None, 1], dtype=pl.Int64),
        "data1": np.random.standard_normal(7),
        "data2": np.random.standard_normal(7),
    }
)


# Does polars has a data structure like Pandas's Series groupby object?
# No. Polars works with DataFrame only


grouped = df.group_by("key1")

grouped.agg(pl.col("data1").mean())


grouped2 = df.group_by(["key1", "key2"])  # grouped data using two key

(
    grouped2.agg(pl.col("data1").mean()).pivot(
        index="key1", values="data1", columns="key2"
    )
)


states = pl.Series(["OH", "CA", "CA", "OH", "OH", "CA", "OH"])
df.group_by(states).agg(
    pl.col("data1").mean()
)  # any Series of the right length also works


(df.group_by("key1").agg(pl.all().mean()))


(
    df.group_by("key2").agg(
        cs.float().mean()  # aggreate float columns
    )
)

# Get group size
(df.group_by("key1").agg(pl.len().alias("size")))

df.group_by("key1").len()  # GroupBy has its own method
df.group_by("key1").max()


# Iterating over groups

for name, group in grouped:
    print(name)
    print(group)


for (k1, k2), group in grouped2:
    print((k1, k2))
    print(group)

people = pl.DataFrame(np.random.standard_normal((5, 5)))
people.columns = ["a", "b", "c", "d", "e"]  # rename columns

people = people.with_columns(
    pl.Series(name="key1", values=["Joe", "Steve", "Wanda", "Jill", "Trey"])
)  #  add a list as new column

# Grouping with functions

people.group_by(pl.col("key1").str.len_chars()).agg(pl.all().sum())


# Mixing functions with Series

key_list = ["one", "one", "one", "two", "two"]
people.group_by(
    [pl.col("key1").str.len_chars(), pl.Series(name="key_list", values=key_list)]
).agg(pl.all().sum())


grouped.agg(pl.col("data1").bottom_k(2))


# Custom aggregation functions


def peak_to_peak(x: pl.Expr) -> pl.Expr:
    return x.list.max() - x.list.min()


grouped.agg(
    cs.float().map_batches(peak_to_peak, return_dtype=pl.Float64, agg_list=True)
)

# Column wise and multiple function application

tips = pl.read_csv("tips.csv")

tips = tips.with_columns((pl.col("tip") / pl.col("total_bill")).alias("tip_pct"))

tips_grouped = tips.group_by(["day", "smoker"])

tips_grouped.agg(
    pl.col("tip_pct").mean().alias("avg_tip_pct"),
    pl.col("tip_pct").std().alias("std_tip_pct"),
    pl.col("tip_pct")
    .map_batches(peak_to_peak, agg_list=True, return_dtype=pl.Float64)
    .alias("peak_tip_pct"),
).sort(["day", "smoker"])


# Apply
# It's advised not to use UDFs where Polars-native expression can

tips.group_by("smoker").agg(pl.col("tip_pct").top_k(5).alias("top5")).explode(
    "top5"
)  # DataFrame.explode()


tips.with_columns(
    pl.col("tip_pct").rank("ordinal", descending=True).over("smoker").alias("rn")
).filter(pl.col("rn") <= 5).sort(["smoker", "rn"])

# Quantile and bucket analysis

dta = pl.DataFrame(
    {
        "data1": np.random.standard_normal(1000),
        "data2": np.random.standard_normal(1000),
    }
)

dta = dta.with_columns(
    pl.col("data1")
    .qcut(quantiles=4, labels=["g1", "g2", "g3", "g4"])
    .alias("quartiles")
)

dta["quartiles"].value_counts()

dta.group_by("quartiles").agg(
    pl.col("data2").min().alias("min_2"),
    pl.col("data2").max().alias("max_2"),
    pl.col("data2").mean().alias("avg_2"),
    pl.col("data2").std().alias("std_2"),
)

# Example: random sampling and permutation

suits = ["H", "S", "C", "D"]  # Hearts, Spades, Clubs, Diamonds
card_val = (list(range(1, 11)) + [10] * 3) * 4
base_names = ["A"] + list(range(2, 11)) + ["J", "K", "Q"]
cards = []
for suit in suits:
    cards.extend(str(num) + suit for num in base_names)

deck = pl.Series(name="card_val", values=cards)
deck.sample(5)

for i in range(0, 6):
    print("Times: ", i)
    print(deck.sample(5))


# Example: weighted average and correlation

w = pl.DataFrame(
    {
        "category": ["a", "a", "a", "a", "b", "b", "b", "b"],
        "data": np.random.standard_normal(8),
        "weights": np.random.uniform(size=8),
    }
)

w.group_by("category").agg(
    ((pl.col("data") * pl.col("weights")).sum() / pl.col("weights").sum()).alias(
        "w_avg"
    )
)

# ┌──────────┬───────────┐
# │ category ┆ w_avg     │
# │ ---      ┆ ---       │
# │ str      ┆ f64       │
# ╞══════════╪═══════════╡
# │ a        ┆ -0.152434 │
# │ b        ┆ -0.567091 │
# └──────────┴───────────┘

# Panda's implementation

w_grouped = w.to_pandas().groupby("category")


def get_w_avg(g):
    return np.average(g["data"], weights=g["weights"])


w_grouped.apply(get_w_avg)
# category
# a   -0.152434
# b   -0.567091
# dtype: float64


close_px = pl.read_csv("stock_px.csv", try_parse_dates=True)
close_px = close_px.rename({"": "day"})

close_px = close_px.with_columns(pl.col("day").dt.year().alias("report_year"))


rets = (
    close_px.select(pl.col("report_year"), cs.float())
    .with_columns(cs.float().pct_change())
    .drop_nulls()
)

rets.group_by("report_year").agg(
    pl.corr(pl.col("AAPL"), pl.col("SPX")),
    pl.corr(pl.col("MSFT"), pl.col("SPX")),
    pl.corr(pl.col("XOM"), pl.col("SPX")),
).sort("report_year")


# Pivot tables and cross-tabulation

tips.pivot(
    index=["time", "day"],
    columns=["smoker"],
    values=["size", "tip_pct"],
    aggregate_function="mean",  # this arg takes pre-defined aggregate function string (min, max, first, last, sum, mean, median, len)
).sort(["time", "day"])


tips.pivot(
    index=["time", "smoker"],
    columns=["day"],
    values=["tip_pct"],
    aggregate_function="len",
).sort(["time", "smoker"]).with_columns(
    pl.sum_horizontal(pl.col(["Sun", "Sat", "Thur", "Fri"])).alias("All")
)

# I didn't known column assignment is valid in Polars
tips.with_columns(
    double_size=pl.col("size") * 2,
    tip_pct_scaled=pl.col("tip_pct") * 100,
    total_bill_by_smoker=pl.col("total_bill").sum().over("smoker"),
)
