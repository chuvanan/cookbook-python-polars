



Read file @data_manipulation.qmd, write the section about Join DataFrames. The section should include
the following content:


- Quick reference table for people who know what they are looking for:

| Types of join  | Types of join   | dplyr                                                        | polars                     |
|----------------|-----------------|--------------------------------------------------------------|----------------------------|
| Equi joins     | Mutating joins  | left_join(x, y)                                              | x.join(y, how='left')      |
|                |                 | right_join()                                                 | join(how='right')          |
|                |                 | full_join()                                                  | join(how='full')           |
|                |                 | inner_join()                                                 | join(how='full')           |
|                | Filtering joins | semi_join(x, y)                                              | x.join(y, how='semi')      |
|                |                 | anti_join(x, y)                                              | x.join(y, how='anti')      |
| Non-equi joins | Cross join      | cross_join(x, y)                                             | x.join(y, how='cross')     |
|                | Inequality join | inner_join(x, y, join_by(key >= key))                        | x.join_where(y)            |
|                | Rolling join    | left_join(x, y, join_by(closest(key < key)))                 | x.join_asof(y)             |
|                | Overlap join    | inner_join(x, y, join_by( overlaps(start, end, start, end))) |                            |


- Often-used equi joins are very similiar between dplyr and polars
- And also validation method in polars vs. dplyr's handling of many-to-many relationships
- The difference in implementation of non-equi joins between dplyr and polars

Selected references for section about Join:

- dplyr's join functions: https://r4ds.hadley.nz/joins.html
- Polars DataFrame join methods: https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.join.html
