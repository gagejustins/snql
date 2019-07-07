# SNQL
In the interest of getting better at general software engineering practices and building data pipelines, I built a full stack web app and data pipeline for my sneaker collection. Here's how it works:

1) Web interface for logging events: adding, cleaning, selling, and wearing sneakers
2) Data flows to events (kind of like logs, or the fact table of this schema), sneakers, and manufacturers tables
3) Airflow job to create a dim_sneakers table for downstream metrics
4) Auto-updating visualizations of my sneaker habits on justinsgage.com

If this works out at all, maybe I'll turn it into an app.

<img src='https://github.com/gagejustins/snql/blob/master/front_end.png'>
