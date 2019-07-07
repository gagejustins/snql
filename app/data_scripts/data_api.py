import pandas as pd

def generate_pairs_owned_over_time_df(conn):
    sql="""select
	c.month,
	count(*) as pairs_owned
from calendar_monthly c
join dim_sneakers s on s.created_at <= c.month
	and (sold_at >= c.month or sold_at is null) 
	and (trashed_at >= c.month or trashed_at is null)
	and (given_at >= c.month or given_at is null)
	and c.month <= date_trunc('month', now())
group by 1
order by 1"""
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()

    pairs_owned_over_time =  pd.DataFrame(results, columns=['date', 'num_owned'])
    if pairs_owned_over_time is None:
        return "generation failed"
    else:
        return pairs_owned_over_time 

def generate_pairs_per_brand_df(conn):
    
    sql = """select
	manufacturer_name,
	count(*)
from dim_sneakers
where is_owned = true
group by 1 
order by 2 desc"""
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    pairs_per_brand = pd.DataFrame(results, columns=['brand','num_owned'])
    if pairs_per_brand is None:
        return "generation failed"
    else:
        return pairs_per_brand
