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
