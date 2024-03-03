

import pandas as pd
import numpy as np

purchases = pd.read_csv("data/purchases.csv")

# 1 `country` is treated as index

(purchases
 .groupby("country")["amount"]
 .sum())

# 2 reset index, but the column `amount` is not OK

(purchases
 .groupby("country")["amount"]
 .sum()
 .reset_index())


# 3 so rename it

(purchases
 .groupby("country")["amount"]
 .sum()
 .reset_index()
 .rename(columns={"amount": "total"}))

# 4 other way(s) to get same result

(purchases
 .groupby("country")
 .agg(total = ("amount", "sum"))
 .reset_index())


(purchases
 .groupby("country")
 .agg(total = ("amount", np.sum))
 .reset_index())
