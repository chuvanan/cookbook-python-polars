

import polars as pl

chipo = pl.read_csv(source="https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv",
                    separator="\t")


# See the first 10 entries
chipo.head(10)

# What is the number of observations in the dataset?
chipo.shape[0]

chipo.height

# Print the name of all the columns.
chipo.columns

# Which was the most-ordered item?

(
    chipo.group_by("item_name")
    .agg(count_item=pl.col("quantity").sum())
    .top_k(1, by="count_item")
    ["item_name"]
)

# For the most-ordered item, how many items were ordered?
(
    chipo.group_by("item_name")
    .agg(count_item=pl.col("quantity").sum())
    .top_k(1, by="count_item")
    ["count_item"]
)


# How many items were orderd in total?
chipo.select(pl.col("quantity").sum().alias("total_ordered_items"))


# Turn the item price into a float

chipo = (
    chipo.with_columns(
        pl.col("item_price").str.replace("\\$", "").str.strip_chars(" ").cast(pl.Float32)
    )
)

# How much was the revenue for the period in the dataset?

chipo = chipo.with_columns(
    total_rev=pl.col("quantity") * pl.col("item_price")
)

print("total revenue:", chipo["total_rev"].sum(), "USD")

# What is the average revenue amount per order?
(
    chipo.select(
        total_orders=pl.col("order_id").n_unique(),
        avg_rev_per_order=pl.col("total_rev").sum() / pl.col("order_id").n_unique()
    )
)


# How many different items are sold?
(
    chipo["item_name"].n_unique()
)
