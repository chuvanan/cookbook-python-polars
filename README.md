# A tidyverse user's guide to Polars

A practical cookbook for R/tidyverse users learning the [Polars](https://pola.rs/) DataFrame library for Python. Each section pairs Polars syntax with its dplyr/tidyr/lubridate equivalent so the concepts map directly onto what you already know.

The book's website is available at https://chuvanan.github.io/cookbook-python-polars/, and its structure closely mirrors https://ddotta.github.io/cookbook-rpolars/.

## Table of Contents

- **First steps with Polars** — installation, reading data, inspecting DataFrames

- **Data manipulation**
  - Data type conversion and casting
  - Introduction to method chaining
  - Filtering rows (`filter` → `dplyr::filter`)
  - Selecting columns and selectors (`select`, `cs.*` → `dplyr::select`)
  - Modifying, renaming, and removing columns (`with_columns`, `rename`, `drop` → `dplyr::mutate`)
  - Aggregation by group (`group_by().agg()` → `dplyr::summarise`)
  - Sorting (`sort` → `dplyr::arrange`)
  - Joining DataFrames (equi, filtering, and non-equi joins → `dplyr::*_join`)
  - Concatenating DataFrames (`pl.concat` → `dplyr::bind_rows/bind_cols`)
  - Pivoting (`pivot`, `unpivot` → `tidyr::pivot_wider/pivot_longer`)
  - Missing values (`fill_null`, `drop_nulls` → `tidyr::fill`, `dplyr::coalesce`)
  - String methods (`.str` namespace → `stringr`)
  - Handling datetime (`.dt` namespace → `lubridate`)
  - Other useful methods (`when/then/otherwise`, `sample`, `top_k/bottom_k`)

- **Import / Export** — reading and writing CSV, Parquet, Excel, and SQL databases

- **Lazy API** — `LazyFrame`, predicate and projection pushdown, `explain()`, streaming for larger-than-memory data

## Contribution

Contributions, corrections, and suggestions are welcome — please open an issue or pull request on [GitHub](https://github.com/chuvanan/cookbook-python-polars).

## Acknowledgement

Inspired by [cookbook-rpolars](https://ddotta.github.io/cookbook-rpolars/) by Damien Dotta.
