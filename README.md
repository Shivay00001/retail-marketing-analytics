# Retail & Marketing Analytics: Customer Segmentation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Production-green)

## 📌 Project Overview

Understanding customer behavior is crucial for growth. This project implements advanced customer segmentation using **RFM Analysis (Recency, Frequency, Monetary)** and **K-Means Clustering**. By grouping customers based on their purchasing habits, businesses can tailor marketing strategies to maximize retention and revenue.

## 🚀 Key Features

- **Synthetic Transaction Data**: Generates a high-fidelity dataset mimicking real-world e-commerce transactions (InvoiceNo, StockCode, CustomerID, etc.).
- **RFM Analysis**:
  - **Recency**: Days since last purchase.
  - **Frequency**: Total number of transactions.
  - **Monetary**: Total revenue generated.
- **K-Means Clustering**: Automatically identifies 4 distinct customer segments.
- **Visualizations**: 3D scatter plots and pairplots to visualize segment separation.
- **Automated Reporting**: Generates a markdown report summarizing cluster characteristics.

## 🛠️ Tech Stack

## 🛠️ Tech Stack & Tools

A multi-disciplinary approach using the best tools in the industry:

### Programming & ML

- **Python**: Core logic and clustering algorithms.
- **Scikit-learn**: K-Means clustering and RFM feature scaling.
- **Matplotlib**: 3D clustering visualization.
- **R Programming**: Customer lifetime value (CLV) statistical modeling.

### Business Intelligence (BI)

- **PowerBI**: Executive dashboards for customer segments.
- **Tableau**: Visualizing purchase frequency and monetary value.
- **Qlik Sense**: Self-service analytics for marketing teams.
- **Excel**: Ad-hoc analysis and strategy planning.

### Data Infrastructure

- **SQL**: Transactional data querying.
- **Google BigQuery**: Scalable data storage for transaction logs.
- **Apache**: Distributed processing for large-scale retail data.
- **Talend**: Data integration from multiple retail sources.

### Advanced Analytics

- **Google Analytics**: Customer journey tracking on e-commerce platform.
- **SAS**: Predictive modeling for campaign response.
- **Splunk**: Real-time transaction monitoring.

## 📂 Project Structure

```
retail-analytics/
├── data_generator.py     # Simulates retail transaction data
├── segmentation.py       # Performs RFM analysis and clustering
├── online_retail_simulated.csv # (Generated) The dataset
├── segmentation_report.md # (Generated) Summary of segments
├── rfm_3d_plot.png       # (Generated) 3D Visualization
└── README.md             # Project documentation
```

## 📊 Methodology

1. **Data Generation**: We simulate 20,000+ transactions for 1,000 customers, incorporating seasonality and varying purchasing power.
2. **Preprocessing**: Data is cleaned (negative quantities removed) and aggregated by CustomerID.
3. **RFM Calculation**: We compute Recency, Frequency, and Monetary scores for each customer.
4. **Log Transformation**: To handle skewed data distributions (typical in monetary data).
5. **Clustering**: We use K-Means to find natural groupings in the 3D RFM space.

## 📈 Interpreting Segments

The scripts generate a report (`segmentation_report.md`) detailing the clusters. Common segments include:

- **Champions**: Bought recently, buy often, and spend the most.
- **Loyal Customers**: Buy on a regular basis.
- **Potential Loyalists**: Recent customers with average frequency.
- **At Risk**: Purchased often but haven't returned for a long time.

## 💻 How to Run

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/retail-analytics.git
    cd retail-analytics
    ```

2. **Install dependencies**:

    ```bash
    pip install pandas numpy scikit-learn faker matplotlib seaborn
    ```

3. **Generate Data**:

    ```bash
    python data_generator.py
    ```

4. **Run Segmentation**:

    ```bash
    python segmentation.py
    ```

5. **View Output**: Check `segmentation_report.md` and the generated plots.

## 📜 License

This project is licensed under the MIT License.
