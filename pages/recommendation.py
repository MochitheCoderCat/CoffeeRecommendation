import streamlit as st
from joblib import load
import pandas as pd
from recommendation import recommend_kmeans, recommend_knn
from visuals import plot_feature_comparison, plot_categorical_comparison

def run_recommendation_system():
    st.image("static/coffee_header.jpg")
    # Step-by-step instructions
    st.header("How to Get Recommendation?")
    st.write("""
    Follow these steps to get personalized coffee recommendations:
    1. **Select Your Model**: Choose between the KNN Model and KMeans Model from the sidebar.
    2. **Choose Coffee Options**: Select your first and second coffee choices from the dropdown menus.
    3. **Randomize Choices**: If you want to explore new options, click the "Randomize" buttons to get random coffee choices.
    4. **Get Recommendation**: Click the "Get Recommendation" button to see your personalized coffee recommendation based on your selections.
    5. **View Comparison**: After receiving your recommendation, you can view a comparison of the selected coffees and the recommended coffee.
    """)
    
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
    if st.sidebar.button("Get Recommendation", type="primary"):
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

                # Extract original categorical data
                categorical_features = ['name', 'roast', 'country']  # Include other categorical features if needed
                original_data = df[categorical_features]

                # Get data for input coffee(s)
                input_data = original_data[original_data['name'].isin(user_input)].reset_index(drop=True)

                # Get data for recommended coffee
                recommended_data = original_data[original_data['name'] == recommendation].reset_index(drop=True)

                st.subheader("Comparison of Categorical Features")

                # Create columns
                cols = st.columns(len(user_input) + 1)  # Number of input coffees + 1 for recommended coffee

                # Display input coffee(s)
                for i, coffee_name in enumerate(user_input):
                    coffee_info = input_data[input_data['name'] == coffee_name].iloc[0]
                    with cols[i]:
                        st.markdown(f"**Input Coffee {i + 1}: {coffee_name}**")
                        st.markdown(f"- **Country**: {coffee_info['country']}")
                        st.markdown(f"- **Roast**: {coffee_info['roast']}")
                        # Add more features if needed

                # Display recommended coffee
                with cols[-1]:
                    coffee_info = recommended_data.iloc[0]
                    st.markdown(f"**Recommended Coffee: {recommendation}**")
                    st.markdown(f"- **Country**: {coffee_info['country']}")
                    st.markdown(f"- **Roast**: {coffee_info['roast']}")
                    # Add more features if needed



    st.sidebar.title("Navigation")
    if st.sidebar.button("Back to Dataset Explorer"):
        st.switch_page("pages/dataset_explorer.py")

if __name__ == "__main__":
    run_recommendation_system()