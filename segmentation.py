import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime
import os

# Set style
plt.style.use('ggplot')

def load_data(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

def perform_rfm_analysis(df):
    print("Performing RFM Analysis...")
    
    # Filter out cancellations and missing CustomerID
    df_clean = df[(df['Quantity'] > 0) & (df['CustomerID'].notnull())]
    
    # Calculate TotalPrice
    df_clean['TotalPrice'] = df_clean['Quantity'] * df_clean['UnitPrice']
    
    # Reference date (1 day after last transaction)
    snapshot_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    # Calculate RFM metrics
    rfm = df_clean.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    })
    
    rfm.rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency',
        'TotalPrice': 'Monetary'
    }, inplace=True)
    
    print(f"RFM Table created for {len(rfm)} customers.")
    return rfm

def segment_customers(rfm):
    print("Segmenting customers with K-Means...")
    
    # Unskew data (log transformation)
    rfm_log = np.log1p(rfm)
    
    # Scale data
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_log)
    
    # K-Means (Assuming K=4 for simplicity)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled)
    
    rfm['Cluster'] = kmeans.labels_
    
    # Calculate mean values for each cluster
    cluster_avg = rfm.groupby('Cluster').mean()
    print("Cluster Averages:")
    print(cluster_avg)
    
    return rfm, rfm_scaled, kmeans

def visualize_clusters(rfm, rfm_scaled, kmeans):
    print("Generating visualizations...")
    
    # Add Cluster labels to scaled data for plotting
    rfm_scaled_df = pd.DataFrame(rfm_scaled, columns=['Recency', 'Frequency', 'Monetary'])
    rfm_scaled_df['Cluster'] = kmeans.labels_
    
    # Pairplot
    sns.pairplot(rfm_scaled_df, hue='Cluster', palette='viridis')
    plt.savefig('rfm_clusters_pairplot.png')
    plt.close()
    
    # 3D Scatter Plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    colors = ['r', 'g', 'b', 'y']
    for i in range(4):
        subset = rfm_scaled_df[rfm_scaled_df['Cluster'] == i]
        ax.scatter(subset['Recency'], subset['Frequency'], subset['Monetary'], c=colors[i], label=f'Cluster {i}', s=50)
    
    ax.set_xlabel('Recency (Scaled)')
    ax.set_ylabel('Frequency (Scaled)')
    ax.set_zlabel('Monetary (Scaled)')
    plt.legend()
    plt.title('3D Customer Segments')
    plt.savefig('rfm_3d_plot.png')
    plt.close()
    print("Plots saved.")

def generate_report(rfm):
    print("Generating report...")
    with open("segmentation_report.md", "w") as f:
        f.write("# Customer Segmentation Report\n\n")
        f.write("## Cluster Analysis\n\n")
        f.write("| Cluster | Recency (Mean) | Frequency (Mean) | Monetary (Mean) | Size |\n")
        f.write("|---|---|---|---|---|\n")
        
        counts = rfm['Cluster'].value_counts()
        cluster_avg = rfm.groupby('Cluster').mean()
        
        for i in sorted(cluster_avg.index):
            r = cluster_avg.loc[i, 'Recency']
            freq = cluster_avg.loc[i, 'Frequency']
            m = cluster_avg.loc[i, 'Monetary']
            size = counts[i]
            f.write(f"| {i} | {r:.1f} days | {freq:.1f} | ${m:.2f} | {size} |\n")
            
        f.write("\n## Interpretation\n")
        f.write("- **Gold Customers**: High Frequency, High Monetary, Low Recency.\n")
        f.write("- **At Risk**: High Monetary/Frequency but High Recency (Haven't bought in a while).\n")
        f.write("- **New Customers**: Low Frequency, Low Monetary, Low Recency.\n")
        f.write("- **Lost**: Low Frequency, Low Monetary, High Recency.\n")

def main():
    data_path = "online_retail_simulated.csv"
    if not os.path.exists(data_path):
        print("Data file not found. Run data_generator.py first.")
        return
        
    df = load_data(data_path)
    rfm = perform_rfm_analysis(df)
    rfm, rfm_scaled, kmeans = segment_customers(rfm)
    visualize_clusters(rfm, rfm_scaled, kmeans)
    generate_report(rfm)
    print("Segmentation completed. Check 'segmentation_report.md' and PNG files.")

if __name__ == "__main__":
    main()
