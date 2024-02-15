import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Function to load data from URL
def load_data(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data from {url}: {str(e)}")

# Define Streamlit app title
st.title('E-Commerce Data Analysis')

# Sidebar menu for selecting analysis
analysis_choice = st.sidebar.selectbox(
    "Select Analysis",
    ["Payment Analysis", "Order Delivery Analysis", "Product Analysis"]
)

# Function for payment analysis
def payment_analysis(order_payments_data):
    # Task 1: Visualize Payment Type Distribution
    st.header('Payment Type Distribution')
    st.write("Pada soal no 1 terjadi perhitungan data dan visualisasi data untuk pembayaran menggunakan (debit card,credit card,voucher,boleto). Catatan terdapat data tidak terdefinisi sebanyak 3 buah namun di asumsikan telah membayar namun hanya saja pembayaran tidak termasuk ke 4 hal tadi.")
    payment_type_counts = order_payments_data['payment_type'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.bar(payment_type_counts.index, payment_type_counts.values, color='skyblue')
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # Table for Payment Type Distribution Explanation
    st.subheader('Explanation - Payment Type Distribution')
    payment_type_explanation_df = pd.DataFrame({
        'Payment Type': payment_type_counts.index,
        'Frequency': payment_type_counts.values
    })
    st.table(payment_type_explanation_df)

    # Task 2: Visualize Payment Installments Distribution
    st.header('Payment Installments Distribution')
    st.write("Terjadi perhitungan beserta visualisasi data untuk banyaknya angsuran pembayaran dan terlihat secara jelas pada data kebanyakan pembayaran di lakukan sekali (lunas) tidak ada hal yang terlalu menonjol maupun error pada soal ini ,interval terjadi mulai dari 1x hingga 24x")
    payment_installments_counts = order_payments_data['payment_installments'].value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    ax2.bar(payment_installments_counts.index, payment_installments_counts.values, color='salmon')
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # Table for Payment Installments Distribution Explanation
    st.subheader('Explanation - Payment Installments Distribution')
    payment_installments_explanation_df = pd.DataFrame({
        'Installments': payment_installments_counts.index,
        'Frequency': payment_installments_counts.values
    })
    st.table(payment_installments_explanation_df)

    # Task 3: Visualize Payment Value Distribution
    st.header('Payment Value Distribution')
    st.write("Soal ini menegaskan untuk memproses data agar bisa menampilkan grafik / visualisasi jumlah uang yang di keluarkan untuk pembelian entitas(barang, dll) ini bertujuan untuk pemantauan bisnis juga pengambilan keputusan lebih lanjut dalam dunia nyata")
    payment_value_intervals = pd.cut(order_payments_data['payment_value'], bins=[0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 10000])
    payment_value_counts = payment_value_intervals.value_counts().sort_index()
    fig3, ax3 = plt.subplots()
    ax3.bar(payment_value_counts.index.astype(str), payment_value_counts.values, color='lightgreen')
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # Table for Payment Value Distribution Explanation
    st.subheader('Explanation - Payment Value Distribution')
    payment_value_intervals_str = [f"{int(interval.left)} - {int(interval.right)}" for interval in payment_value_counts.index]
    payment_value_explanation_df = pd.DataFrame({
        'Interval': payment_value_intervals_str,
        'Frequency': payment_value_counts.values
    })
    st.table(payment_value_explanation_df)

# Function for order delivery analysis
def order_delivery_analysis(orders_data):
    # Task 1: Visualize Order Purchase Timestamps Distribution (Quarterly Intervals)
    st.header('Order Purchase Timestamps Distribution (Quarterly Intervals)')
    st.write("Menghitung banyaknya terjadi pembelian dan memvisualisasikannya dengan interval yang di minta (3 bulan ) dari tahun 2016")
    orders_data['order_purchase_timestamp'] = pd.to_datetime(orders_data['order_purchase_timestamp'])
    orders_data['purchase_quarter'] = orders_data['order_purchase_timestamp'].dt.to_period("Q")
    quarterly_counts = orders_data['purchase_quarter'].value_counts().sort_index()
    fig4, ax4 = plt.subplots()
    ax4.bar(quarterly_counts.index.astype(str), quarterly_counts.values, color='purple')
    plt.xticks(rotation=45)
    st.pyplot(fig4)

    # Table for Order Purchase Timestamps Distribution Explanation
    st.subheader('Explanation - Order Purchase Timestamps Distribution')
    quarterly_counts_explanation_df = pd.DataFrame({
        'Quarter': quarterly_counts.index.astype(str),
        'Frequency': quarterly_counts.values
    })
    st.table(quarterly_counts_explanation_df)

    # Task 2: Visualize Delivery Time Intervals Distribution
    st.header('Delivery Time Intervals Distribution')
    st.write("Memproses data untuk perhitungan lama pengiriman entitas(barang,dll) sedemikian hingga menghasilkan interval data yang di presentasikan dalam bentuk grafik. Catatan terdapat banyak data kosong (bukan berarti null) namun tidak termasuk terhitung banyaknya hari yang di perlukan pada persebaran rentetan interval dalam grafik tersebut.")
    orders_data['order_delivered_customer_date'] = pd.to_datetime(orders_data['order_delivered_customer_date'])
    orders_data['delivery_interval'] = (orders_data['order_delivered_customer_date'] - orders_data['order_purchase_timestamp']).dt.days
    max_interval = orders_data['delivery_interval'].max()
    delivery_intervals = list(range(1, int(max_interval) + 2, 2))
    hist, bins = np.histogram(orders_data['delivery_interval'], bins=delivery_intervals + [float('inf')])
    fig5, ax5 = plt.subplots()
    ax5.bar(delivery_intervals, hist, color='green', align='center')
    plt.xticks(rotation=45)
    st.pyplot(fig5)

    # Table for Delivery Time Intervals Distribution Explanation
    st.subheader('Explanation - Delivery Time Intervals Distribution')
    delivery_intervals_str = [f"{float(interval)} - {float(bins[i+1])}" for i, interval in enumerate(bins[:-1])]
    delivery_intervals_explanation_df = pd.DataFrame({
        'Interval': delivery_intervals_str,
        'Frequency': hist
    })
    st.table(delivery_intervals_explanation_df)

# Function for product analysis
def product_analysis(products_data):
    st.header('Product Analysis')
    # Add your product analysis code here

# Load data based on analysis choice
if analysis_choice == "Payment Analysis":
    order_payments_data = load_data("https://raw.githubusercontent.com/Maenzzz/Tugas_Besar_Sains_data/main/order_payments_dataset.csv")
    if order_payments_data is not None:
        payment_analysis(order_payments_data)
elif analysis_choice == "Order Delivery Analysis":
    orders_data = load_data("https://raw.githubusercontent.com/Maenzzz/Tugas_Besar_Sains_data/main/orders_dataset.csv")
    if orders_data is not None:
        order_delivery_analysis(orders_data)
elif analysis_choice == "Product Analysis":
    products_data = load_data("https://raw.githubusercontent.com/Maenzzz/Tugas_Besar_Sains_data/main/products_dataset.csv")
    if products_data is not None:
        product_analysis(products_data)


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def product_analysis(products_data):
    st.header('Product Analysis')

    # Drop rows with missing values for simplicity
    products_data.dropna(inplace=True)

    # Select relevant features for clustering
    features = products_data[['product_length_cm', 'product_height_cm', 'product_width_cm']]

    # Standardize the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    products_data['cluster'] = kmeans.fit_predict(scaled_features)

    # Display cluster distribution
    st.subheader('Cluster Distribution')
    st.write(products_data['cluster'].value_counts())

    # Optional: Visualize cluster centroids
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)
    centroids_df = pd.DataFrame(centroids, columns=features.columns)
    st.subheader('Cluster Centroids')
    st.write(centroids_df)

#-----------------------------
    import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Function to load data
st.cache_data
def load_data(url):
    return pd.read_csv(url)

# Load the product data
products_file_path = "https://raw.githubusercontent.com/Maenzzz/Tugas_Besar_Sains_data/main/products_dataset.csv"
products_data = load_data(products_file_path)

# Select relevant features for clustering
features = products_data[['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 
                          'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']]

# Impute missing values with the mean of each feature
imputer = SimpleImputer(strategy='mean')
features_imputed = imputer.fit_transform(features)

# Data Preprocessing: Standardize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features_imputed)

# Perform KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(features_scaled)

# Add cluster labels to the original data
products_data['Cluster'] = kmeans.labels_

# Display the clustered products
st.subheader('Clustered Products:')
st.write(products_data[['product_id', 'product_category_name', 'Cluster']].head(50  ))
