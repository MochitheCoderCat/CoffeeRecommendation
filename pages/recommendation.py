import streamlit as st
from joblib import load
import pandas as pd
from recommendation import recommend_kmeans, recommend_knn
from visuals import plot_feature_comparison, plot_categorical_comparison

def run_recommendation_system():
    # Your existing recommendation system code here
    st.title("Coffee Recommendation System")
    
    # Load the models
    knn_model = load('./model/knn_model.joblib')
    kmeans_model = load('./model/kmeans_model.joblib')

    # Load the dataset to extract coffee names
    df = pd.read_csv('coffee_cleaned.csv')  
    coffee_names = df['name'].dropna().unique()  

    # Function to get random coffee choices
    def get_random_coffees():
        return pd.Series(coffee_names).sample(n=min(15, len(coffee_names)), random_state=None)

    # Initialize session states for random coffee choices
    if "random_coffee_1" not in st.session_state:
        st.session_state.random_coffee_1 = get_random_coffees()

    if "random_coffee_2" not in st.session_state:
        st.session_state.random_coffee_2 = get_random_coffees()

    # Sidebar for model selection
    st.sidebar.title("Recommendation models")
    model_choice = st.sidebar.radio(
        "Select your model",
        ("KNN Model", "KMeans Model")
    )

    # Dropdown for first coffee choice
    st.sidebar.title("Choose Coffee Options")
    coffee_1 = st.sidebar.selectbox(
        "Select your first coffee choice:",
        ["None"] + list(st.session_state.random_coffee_1)
    )

    # Button to randomize first coffee choices (placed below the dropdown)
    if st.sidebar.button("Randomize First Coffee Choices"):
        st.session_state.random_coffee_1 = get_random_coffees()

    # Dropdown for second coffee choice
    coffee_2 = st.sidebar.selectbox(
        "Select your second coffee choice (optional):",
        ["None"] + list(st.session_state.random_coffee_2)
    )

    # Button to randomize second coffee choices (placed below the dropdown)
    if st.sidebar.button("Randomize Second Coffee Choices"):
        st.session_state.random_coffee_2 = get_random_coffees()


    # Get Recommendation Button
    if st.sidebar.button("Get Recommendation"):
        if coffee_1 == "None" and coffee_2 == "None":
            st.warning("Please select at least one coffee to get a recommendation.")
        else:
            # Filter out "None" inputs
            user_input = [coffee for coffee in [coffee_1, coffee_2] if coffee != "None"]

            recommendation = None
            if model_choice == "KNN Model":
                st.write("Using KNN Model...")
                # Call the provided KNN recommendation logic
                recommendation = recommend_knn(user_input)

            elif model_choice == "KMeans Model":
                st.write("Using KMeans Model...")
                recommendation = recommend_kmeans(user_input)

            # Display the recommendation and plot the feature comparison
            if recommendation:
                st.success(f"Recommended Coffee: {recommendation}")
                plot_feature_comparison(user_input, recommendation, df)

                # Plot categorical features
                categorical_features = ['roast', 'country']  # Add your non-numerical feature names here
                plot_categorical_comparison(user_input, recommendation, df, categorical_features)
            else:
                st.error("No recommendation could be generated. Please try again.")

    st.sidebar.title("Navigation")
    if st.sidebar.button("Back to Dataset Explorer"):
        st.switch_page("pages/dataset_explorer.py")

if __name__ == "__main__":
    run_recommendation_system()