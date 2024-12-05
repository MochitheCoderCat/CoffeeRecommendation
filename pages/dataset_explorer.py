import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_dataset_explorer():
    st.title("Coffee Dataset Explorer")
    
    # Load the dataset
    df = pd.read_csv('coffee_cleaned.csv')

    # Display basic dataset information
    st.header("Dataset Overview")
    st.write(f"Total number of coffee beans: {len(df)}")
    
    # Display sample of the dataset
    st.subheader("Sample Data")
    st.dataframe(df.head())

    # Basic statistics
    st.subheader("Statistical Summary")
    st.write(df.describe())

    # Feature distributions
    st.header("Feature Distributions")
    # Numeric features visualization
    numeric_features = ['aroma', 'acid', 'body', 'flavor', 'aftertaste']
    
    # Create distribution plots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for idx, feature in enumerate(numeric_features):
        sns.histplot(data=df, x=feature, ax=axes[idx])
        axes[idx].set_title(f'{feature.capitalize()} Distribution')
    
    # Remove the extra subplot
    axes[-1].remove()
    plt.tight_layout()
    st.pyplot(fig)
    
    # Categorical features
    st.header("Categorical Features")
      
    # Country distribution
    st.subheader("Coffee Origins")
    country_counts = df['country'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    country_counts.plot(kind='bar')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

    # Roast distribution
    st.subheader("Roast Types")
    roast_counts = df['roast'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    roast_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Roast Types')
    st.pyplot(fig)


    # Distribution of Ratings
    st.subheader("Distribution of Coffee Ratings")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['rating'], bins=20, kde=True)
    plt.title("Distribution of Coffee Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    st.pyplot(plt)

    # Bar Chart of Coffee Origins (Top 10)
    st.subheader("Top 10 Coffee Origins Count")
    plt.figure(figsize=(12, 6))
    
    # Get the top 10 origins
    origin_counts = df['origin'].value_counts().head(10)  # Get the top 10 origins
    top_origins = origin_counts.reset_index()
    top_origins.columns = ['origin', 'count']  # Rename columns for clarity

    # Create the bar plot
    sns.barplot(data=top_origins, x='origin', y='count', palette='viridis', hue='origin', legend=False)
    plt.title("Count of Coffee Beans by Origin (Top 10)")
    plt.xlabel("Origin")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Scatter Plot of Aroma vs. Flavor
    st.subheader("Aroma vs. Flavor")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='aroma', y='flavor', hue='roast', style='roast', palette='deep')
    plt.title("Aroma vs. Flavor")
    plt.xlabel("Aroma")
    plt.ylabel("Flavor")
    st.pyplot(plt)

    # Convert relevant columns to numeric
    numeric_columns = ['rating', 'aroma', 'acid', 'body', 'flavor', 'price_per_ounce']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # User selects columns to compare
    st.subheader("Select Features to Compare")
    feature_x = st.selectbox("Select X-axis feature:", numeric_columns)
    feature_y = st.selectbox("Select Y-axis feature:", numeric_columns)

    # Scatter Plot of Selected Features
    st.subheader(f"{feature_x} vs. {feature_y}")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=feature_x, y=feature_y, hue='roast', style='roast', palette='deep')
    plt.title(f"{feature_x} vs. {feature_y}")
    plt.xlabel(feature_x)
    plt.ylabel(feature_y)
    st.pyplot(plt)

    # Price Distribution Plot
    st.subheader("Price Distribution")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price_per_ounce'], bins=20, kde=True)
    plt.title("Distribution of Coffee Price per Ounce")
    plt.xlabel("Price (USD/Ounce)")
    plt.ylabel("Frequency")
    st.pyplot(plt)

    # Price vs. Rating Scatter Plot
    st.subheader("Price vs. Rating Scatter Plot")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='price_per_ounce', y='rating')
    plt.title("Relationship between Price and Rating")
    plt.xlabel("Price (USD/Ounce)")
    plt.ylabel("Rating")
    st.pyplot(plt)

    # Average Price by Roast Type Bar Chart
    st.subheader("Average Price by Roast Type")
    plt.figure(figsize=(12, 6))
    average_price_by_roast = df.groupby('roast')['price_per_ounce'].mean()
    sns.barplot(x=average_price_by_roast.index, y=average_price_by_roast.values, palette='viridis')
    plt.title("Average Price by Roast Type")
    plt.xlabel("Roast Type")
    plt.ylabel("Average Price (USD/Ounce)")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Price vs. Other Features Correlation Heatmap
    st.subheader("Price vs. Other Features Correlation Heatmap")
    plt.figure(figsize=(12, 8))
    correlation_matrix = df[['price_per_ounce', 'rating', 'aroma', 'acid', 'body', 'flavor']].corr()
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
    plt.title("Correlation of Price with Other Features")
    st.pyplot(plt)

    # Navigation button to recommendation page
    st.sidebar.title("Navigation")
    if st.sidebar.button("Go to Recommendation System", type="primary"):
        st.switch_page("pages/recommendation.py")

if __name__ == "__main__":
    run_dataset_explorer()