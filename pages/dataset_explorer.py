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
    
    # Navigation button to recommendation page
    st.sidebar.title("Navigation")
    if st.sidebar.button("Go to Recommendation System"):
        st.switch_page("pages/recommendation.py")

if __name__ == "__main__":
    run_dataset_explorer()