# Customer Segmentation & Marketing Strategy

**🔴 Live demo: [customer-segmentation-dashboard-hardikm21.streamlit.app](https://customer-segmentation-dashboard-hardikm21.streamlit.app/)**

*Note: the app runs on a free tier and may take a few seconds to wake up if it has been idle.*

## Key results
- Top 20% of customers generate 77% of revenue
- 28% of customers bought only once
- K-Means with k=4 (silhouette 0.37); CLV method: BG/NBD + Gamma-Gamma
- Scenario estimate: GBP 482,520 extra annual revenue (5.7% of current) under the stated assumptions

## Method
1. Cleaning with a logged decision per step (duplicates, missing IDs, cancellations, non-product codes, invalid values)
2. SQL (SQLite) and EDA, including Pareto analysis
3. RFM quintile scoring with 10 rule-based segments
4. K-Means on log-scaled RFM, k chosen by elbow and silhouette
5. BG/NBD + Gamma-Gamma for predicted 180-day value, validated on a 90-day holdout
6. Segment-level actions and an impact estimate

## Run the dashboard
```
pip install -r requirements.txt
streamlit run app.py
```

Tools: Python, pandas, SQL, scikit-learn, lifetimes, Plotly, Streamlit
