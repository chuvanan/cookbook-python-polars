

import polars as pl
from loguru import logger

years = range(1880, 2011)

for year in years:
    base_url = f"https://raw.githubusercontent.com/wesm/pydata-book/3rd-edition/datasets/babynames/yob{year}.txt"
    filename = f"yob{year}.csv"
    dta = pl.read_csv(base_url, separator=",")
    logger.debug("Read file: `{}`", base_url)
    dta.write_csv(filename)
    logger.debug("Saved file: `{}`", filename)
