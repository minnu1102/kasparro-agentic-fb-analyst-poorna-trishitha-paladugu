import pandas as pd
import json
import numpy as np
from .base import BaseAgent

class DataAgent(BaseAgent):
    def __init__(self, path="data/synthetic_fb_data.csv"):
        super().__init__("DataAgent")
        try:
            self.df = pd.read_csv(path)
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = pd.DataFrame()

    def execute(self, query):
        """
        Calculates summary statistics from the CSV.
        In a real app, 'query' would determine which metrics to pull.
        """
        if self.df.empty:
            return json.dumps({"error": "No data available. Run data generation script."})
        
        # Calculate Correlations (Detects Fatigue: High Freq + Low CTR)
        freq_ctr_corr = 0
        if len(self.df) > 5:
            freq_ctr_corr = self.df['frequency'].corr(self.df['clicks'] / self.df['impressions'])

        # Prepare a dictionary summary
        summary = {
            "total_spend": float(self.df['spend'].sum()),
            "freq_ctr_correlation": float(0 if np.isnan(freq_ctr_corr) else freq_ctr_corr),
            "latest_frequency": float(self.df['frequency'].iloc[-1]),
            "latest_ctr": float((self.df['clicks'].iloc[-1] / self.df['impressions'].iloc[-1])),
            "weekly_trend_sample": self.df.tail(5).to_dict(orient='records')
        }
        
        return json.dumps(summary, default=str)