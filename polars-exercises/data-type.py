
import polars as pl

x = pl.Series(name="a", values=[1,2,3], dtype=pl.Int8)

x.dtype.is_integer()

x.dtype.is_float()

x.dtype.base_type()

y = pl.Series(name="b", values=["a", "b", "c"], dtype=pl.Utf8)

z = x.cast(pl.Float64)

z = z.rename("c")

dta = pl.DataFrame([x, y, z])

p = pl.Series(name="n", values=[None, None, None])

p.dtype.base_type()

p.dtype.is_(pl.Int8)

p.dtype.is_(pl.Null)
