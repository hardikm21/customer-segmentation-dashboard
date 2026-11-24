import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Customer Segmentation Dashboard", page_icon="🛍️", layout="wide")


@st.cache_data
def load():
    customers = pd.read_csv("data/customers.csv")
    monthly = pd.read_csv("data/monthly.csv")
    strategy = pd.read_csv("data/strategy.csv")
    impact = pd.read_csv("data/impact.csv")
    return customers, monthly, strategy, impact


customers, monthly, strategy, impact = load()

st.title("Customer Segmentation & Marketing Strategy")
st.caption("UCI Online Retail II (UK retailer, 2009-2011) | RFM scoring + K-Means clustering + customer lifetime value")

with st.sidebar:
    st.header("Filters")
    all_segs = sorted(customers.segment.unique())
    all_clus = sorted(customers.cluster_name.unique())
    segs = st.multiselect("RFM segment", all_segs, default=all_segs)
    clus = st.multiselect("K-Means cluster", all_clus, default=all_clus)

f = customers[customers.segment.isin(segs) & customers.cluster_name.isin(clus)]
if f.empty:
    st.warning("No customers match the current filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Customers", f"{len(f):,}")
c2.metric("Historical revenue (GBP)", f"{f.monetary.sum():,.0f}")
c3.metric("Avg predicted 180-day value (GBP)", f"{f.clv_180d.mean():,.0f}")
c4.metric("Avg days since last order", f"{f.recency.mean():,.0f}")

tab1, tab2, tab3, tab4 = st.tabs(["RFM segments", "K-Means clusters", "Customers", "Strategy & impact"])

with tab1:
    seg = (f.groupby("segment")
             .agg(customers=("customer_id", "count"), revenue=("monetary", "sum"), avg_clv=("clv_180d", "mean"))
             .reset_index())
    a, b = st.columns(2)
    a.plotly_chart(px.bar(seg.sort_values("customers", ascending=False), x="segment", y="customers",
                          title="Customers per segment"), width="stretch")
    b.plotly_chart(px.bar(seg.sort_values("revenue", ascending=False), x="segment", y="revenue",
                          title="Historical revenue per segment (GBP)"), width="stretch")
    sample = f.sample(min(3000, len(f)), random_state=1)
    st.plotly_chart(px.scatter(sample, x="frequency", y="monetary", color="segment", log_x=True, log_y=True,
                               hover_data=["customer_id", "recency"],
                               title="Frequency vs spend (log scales)"), width="stretch")

with tab2:
    clu = (f.groupby("cluster_name")
             .agg(customers=("customer_id", "count"), revenue=("monetary", "sum"),
                  avg_recency=("recency", "mean"), avg_frequency=("frequency", "mean"),
                  avg_monetary=("monetary", "mean"), avg_clv=("clv_180d", "mean"))
             .round(1).reset_index())
    st.dataframe(clu, width="stretch", hide_index=True)
    st.plotly_chart(px.bar(clu, x="cluster_name", y="avg_clv",
                           title="Average predicted 180-day value by cluster (GBP)"), width="stretch")

with tab3:
    st.write(f"{len(f):,} customers match the filters")
    st.dataframe(f.sort_values("clv_180d", ascending=False), width="stretch", hide_index=True)
    st.download_button("Download filtered customers (CSV)", f.to_csv(index=False).encode("utf-8"),
                       file_name="customers_filtered.csv", mime="text/csv")

with tab4:
    st.subheader("Recommended actions by segment")
    st.dataframe(strategy, width="stretch", hide_index=True)
    st.subheader("Estimated annual revenue impact (scenario assumptions)")
    st.dataframe(impact, width="stretch", hide_index=True)
    st.plotly_chart(px.bar(impact, x="est_annual_revenue_gbp", y="lever", orientation="h",
                           title="Estimated annual revenue impact by lever (GBP)"), width="stretch")

st.subheader("Monthly revenue")
st.plotly_chart(px.bar(monthly, x="year_month", y="revenue"), width="stretch")
