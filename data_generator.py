import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)
random.seed(42)

def generate_retail_data(n_transactions=20000, n_customers=1000):
    print(f"Generating {n_transactions} transactions for {n_customers} customers...")
    
    # --- Customers ---
    customer_ids = [fake.unique.random_int(min=10000, max=99999) for _ in range(n_customers)]
    countries = ['United Kingdom', 'Germany', 'France', 'EIRE', 'Spain', 'Netherlands', 'Belgium', 'Switzerland', 'Portugal', 'Australia']
    customer_country = {cid: np.random.choice(countries, p=[0.8, 0.05, 0.05, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01]) for cid in customer_ids}
    
    # --- Products ---
    n_products = 500
    products = []
    for _ in range(n_products):
        stock_code = fake.unique.bothify(text='??###')
        description = fake.sentence(nb_words=3).upper().replace('.', '')
        price = round(np.random.uniform(1.0, 100.0), 2)
        products.append({'StockCode': stock_code, 'Description': description, 'UnitPrice': price})
    
    # --- Transactions ---
    data = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    # Simulate meaningful patterns: some customers buy often, some rarely
    # Assign 'frequency' and 'monetary' factors to customers
    cust_freq_factor = {cid: np.random.gamma(2, 2) for cid in customer_ids}
    
    for _ in range(n_transactions):
        # Pick a customer based on frequency factor
        cid = random.choices(customer_ids, weights=list(cust_freq_factor.values()), k=1)[0]
        
        # Pick a date
        # Add seasonality: more sales in Nov/Dec
        days_offset = np.random.randint(0, 365)
        month = (start_date + timedelta(days=days_offset)).month
        if month in [11, 12]:
             if random.random() < 0.3: # 30% boost chance
                 days_offset = np.random.randint(300, 365)
        
        invoice_date = start_date + timedelta(days=days_offset, seconds=np.random.randint(0, 86400))
        
        # Invoice number
        invoice_no = fake.unique.random_int(min=500000, max=600000)
        
        # Determine number of items in this invoice
        n_items = np.random.randint(1, 10)
        
        for _ in range(n_items):
            product = random.choice(products)
            qty = np.random.randint(1, 20)
            
            # Chance of return/cancellation (Quantity negative)
            if random.random() < 0.02:
                qty = -qty
                invoice_no_str = f"C{invoice_no}"
            else:
                invoice_no_str = str(invoice_no)
            
            data.append([
                invoice_no_str,
                product['StockCode'],
                product['Description'],
                qty,
                invoice_date,
                product['UnitPrice'],
                cid,
                customer_country[cid]
            ])
            
    df = pd.DataFrame(data, columns=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'])
    
    # Add TotalPrice column for convenience
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    print(f"Data generation complete. Shape: {df.shape}")
    print(df.head())
    
    return df

if __name__ == "__main__":
    df = generate_retail_data(25000, 1500)
    output_file = "online_retail_simulated.csv"
    df.to_csv(output_file, index=False)
    print(f"Dataset saved to {output_file}")
