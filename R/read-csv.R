

require(readr)

flights_202212 = read_delim(
	file = "./data/On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2022_12.csv",
	delim = ",",
	col_names = TRUE,
	guess_max = 1000L,
	n_max = 10
)

flights_202212[1:3, 1:10]

