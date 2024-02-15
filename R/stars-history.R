
require(ggplot2)

rc = "Roboto Condensed"

options(
	ggplot2.discrete.colour = ggokabeito::palette_okabe_ito()
)

theme_set(
	theme_minimal(
		base_family = rc,
		base_size = 14
	)
)

stars_hist = readr::read_csv('./data/star-history-2024215.csv', col_names = c('project', 'date', 'stars'))

stars_hist = stars_hist |>
	dplyr::mutate(date = substr(date, 1, 15)) |>
	dplyr::mutate(date = as.Date(date, format = '%a %b %d %Y'))

ggplot(stars_hist) +
	aes(date, stars, color=project) +
	geom_line(linewidth=1.2) +
	labs(title = "Stars history") +
	scale_y_continuous(labels = scales::comma_format()) +
	theme(legend.title = element_blank())

