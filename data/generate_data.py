import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_dataset(output_path="data/synthetic_fb_data.csv"):
    # Create the data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("⏳ Generating synthetic data...")
    
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    dates.reverse()
    data = []
    
    # Generate "Ad Fatigue" Scenario
    # (Frequency goes UP, CTR goes DOWN -> Causes ROAS drop)
    for i, date in enumerate(dates):
        # Simulation logic:
        # Frequency starts at 1.2 and creeps up to ~3.6
        freq = 1.2 + (i * 0.08) 
        
        # CTR starts healthy (2.5%) and drops to 0.5%
        ctr = max(0.005, 0.025 - (i * 0.0006))
        
        spend = 1000
        imps = int((spend / 20) * 1000) # CPM around $20
        clicks = int(imps * ctr)
        revenue = clicks * 2.5 * 60 # Assume $150 Revenue per click (approx)
        
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "spend": spend,
            "impressions": imps,
            "clicks": clicks,
            "frequency": round(freq, 2),
            "revenue": round(revenue, 2)
        })
            
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✅ Success! Data saved to: {output_path}")

if __name__ == "__main__":
    generate_dataset()