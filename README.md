# snql
In the interest of getting better at general software engineering practices and building data pipelines, I'm building a data pipeline for my sneaker collection. Here's the plan:

1) Web interface for logging events: adding, cleaning, selling, and wearing sneakers
2) Events table with foreign keys to sneakers and manufacturers table
3) Airflow jobs to create sneakers dimension and sneakers metrics tables from events table
4) Auto-updating visualizations of my sneaker habits on justinsgage.com

If this works out at all, maybe I'll turn it into an app.

<img src="https://github.com/gagejustins/snql/blob/master/model.png" width=500>
