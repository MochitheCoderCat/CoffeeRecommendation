import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

def run_dataset_explorer():
    st.title("Coffee Dataset Explorer")
    
    # Load the dataset
    df = pd.read_csv('coffee_cleaned.csv')

    # Sidebar for selecting the type of visualization
    st.sidebar.title("Select Visualization")
    visualization_type = st.sidebar.radio("Choose a visualization type:", 
                                           ("Overview", "Category Features", "Price Analysis", "Feature Comparison", "Fun Facts 🆕"))

    if visualization_type == "Overview":
        # Search Form
        st.header("Search the Dataset")
        with st.form(key='search_form'):
            search_term = st.text_input("Enter a coffee bean name or roaster name:")
            submit_button = st.form_submit_button(label='Search')

        if submit_button:
            # Filter the DataFrame based on the search term
            filtered_df = df[df['name'].str.contains(search_term, case=False) | df['roaster'].str.contains(search_term, case=False)]

            # Display the results
            if not filtered_df.empty:
                st.subheader("Search Results")
                st.dataframe(filtered_df)
            else:
                st.write("No results found.")

        # Display basic dataset information
        st.header("Dataset Overview")
        st.write(f"Total number of coffee beans: {len(df)}")
        
        # Display sample of the dataset
        st.subheader("Sample Data")
        st.dataframe(df.head())

        # Basic statistics
        st.subheader("Statistical Summary")
        st.write(df.describe())

        # Overview visualizations
        st.subheader("Distribution of Coffee Ratings")
        plt.figure(figsize=(10, 6))
        sns.histplot(df['rating'], bins=20, kde=True)
        plt.title("Distribution of Coffee Ratings")
        plt.xlabel("Rating")
        plt.ylabel("Frequency")
        st.pyplot(plt)
        
        # Feature distributions
        st.header("Feature Distributions")
        
        # Numeric features visualization
        numeric_features = ['aroma', 'acid', 'body', 'flavor', 'aftertaste']
        
        # Create distribution plots
        fig, axes = plt.subplots(3, 2, figsize=(15, 15))  # Adjusted to fit 6 plots
        axes = axes.ravel()
        
        # Plot numeric features
        for idx, feature in enumerate(numeric_features):
            sns.histplot(data=df, x=feature, ax=axes[idx])
            axes[idx].set_title(f'{feature.capitalize()} Distribution')
        
        # Plot roast type distribution
        sns.countplot(data=df, x='roast', ax=axes[len(numeric_features)])  # Use the next available subplot
        axes[len(numeric_features)].set_title("Count of Coffee Beans by Roast Type")
        axes[len(numeric_features)].set_xlabel("Roast Type")
        axes[len(numeric_features)].set_ylabel("Count")
        
        # Remove the extra subplot if needed
        if len(numeric_features) + 1 < len(axes):
            axes[-1].remove()
        
        plt.tight_layout()
        st.pyplot(fig)

    elif visualization_type == "Price Analysis":
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
        sns.barplot(x=average_price_by_roast.index, y=average_price_by_roast.values)
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

    elif visualization_type == "Category Features":
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

    elif visualization_type == "Feature Comparison":

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
    
    elif visualization_type == "Fun Facts 🆕":
        # Fun Facts Section

        # Coffee Beans Selection
        st.subheader("🌟 Fun Facts about Coffee Beans")
        coffee_fact_type = st.selectbox(
            "Select Coffee Bean Fact:", 
            ("Select Fact", "Best", "Worst", "Most Expensive", "Most Affordable")
        )
        coffee_roast_type = st.selectbox(
            "Select Roast Type:", 
            ("Select Roast Type", "All Coffee Beans", "Light", "Medium-Light", "Medium", "Medium-Dark", "Dark")
        )
        
        # Generate Results button for Coffee
        generate_coffee = st.button("Generate Coffee Bean Fact")

        # Check if the default roast type is selected
        if not generate_coffee:
            st.info("Let's find out the most ❓ coffee ☕️ !")
        else:  # Only run after the button is clicked
            if coffee_roast_type == "Select Roast Type" or coffee_fact_type == "Select Fact":
                st.info("Let's find out the most ❓ coffee ☕️ !")
            else:
                with st.spinner("Exploring in the mysterious dataset..."):
                    time.sleep(1)
                    # Filter the DataFrame based on the selected roast type
                    if coffee_roast_type != "All Coffee Beans":
                        filtered_coffee_df = df[df['roast'] == coffee_roast_type]
                    else:
                        filtered_coffee_df = df

                    if coffee_fact_type == "Best":
                        best_coffee = filtered_coffee_df.loc[filtered_coffee_df['rating'].idxmax()]
                        st.markdown(f"**The Best {coffee_roast_type} Coffee Bean is...** 🏆")
                        time.sleep(1)
                        st.markdown(f"**Name:**\n\n✨ *{best_coffee['name']}* ✨")
                        time.sleep(1)
                        st.markdown(f"**Rating:** {best_coffee['rating']:.2f}")

                    elif coffee_fact_type == "Worst":
                        worst_coffee = filtered_coffee_df.loc[filtered_coffee_df['rating'].idxmin()]
                        st.markdown(f"**The Worst {coffee_roast_type} Coffee Bean is...** 💔")
                        time.sleep(1)
                        st.markdown(f"**Name:**\n\n💀 *{worst_coffee['name']}* 💀")
                        time.sleep(1)
                        st.markdown(f"**Rating:** {worst_coffee['rating']:.2f}")

                    elif coffee_fact_type == "Most Expensive":
                        most_expensive_coffee = filtered_coffee_df.loc[filtered_coffee_df['price_per_ounce'].idxmax()]
                        st.markdown(f"**The Most Expensive {coffee_roast_type} Coffee Bean is...** 💎")
                        time.sleep(1)
                        st.markdown(f"**Name:**\n\n💲 *{most_expensive_coffee['name']}* 💲")
                        time.sleep(1)
                        st.markdown(f"**Price:** ${most_expensive_coffee['price_per_ounce']:.2f} per ounce")

                    elif coffee_fact_type == "Most Affordable":
                        most_affordable_coffee = filtered_coffee_df.loc[filtered_coffee_df['price_per_ounce'].idxmin()]
                        st.markdown(f"**The Most Affordable {coffee_roast_type} Coffee Bean is...** 🤝💸")
                        time.sleep(1)
                        st.markdown(f"**Name:**\n\n💸 *{most_affordable_coffee['name']}* 💸")
                        time.sleep(1)
                        st.markdown(f"**Price:** ${most_affordable_coffee['price_per_ounce']:.2f} per ounce")


        # Roasters Selection
        st.subheader("🌟 Fun Facts about Roasters")
        roaster_fact_type = st.selectbox(
            "Select Roaster Fact:", 
            ("Select Fact","Best", "Worst", "Most Expensive", "Most Affordable")
        )

        # Get unique countries from the DataFrame
        unique_countries = df['country'].unique().tolist()
        roaster_location_type = st.selectbox(
            "Select Location:", 
            ["Select Location", "Worldwide"] + unique_countries,
            index=0
        )  # Default to "Select Location"

        # Generate Results button for Roasters
        generate_roaster = st.button("Generate Roaster Fact")

        if not generate_roaster:
            st.info("Let's find out the most ❓ roaster 🧑‍🌾!")
        else:  # Only run after this button is clicked
            if roaster_location_type == "Select Location" or roaster_fact_type == "Select Fact":
                st.info("Let's find out the most ❓ roaster 🧑‍🌾!")
            else:
                with st.spinner("Exploring in the mysterious dataset..."):
                    time.sleep(1)
                    if roaster_fact_type == "Best":
                        if roaster_location_type == "Worldwide":
                            best_roaster = df.groupby('roaster')['rating'].mean().idxmax()
                            highest_avg_rating = df.groupby('roaster')['rating'].mean().max()
                            st.markdown("**The Best Roaster Worldwide is...** 🌍🏆")
                            time.sleep(1)
                            st.markdown(f"**Name:**\n\n✨ *{best_roaster}* ✨")
                            time.sleep(1)
                            st.markdown(f"**Average Rating:** {highest_avg_rating:.2f}")
                        else:
                            best_roaster_country = df[df['country'] == roaster_location_type].groupby('roaster')['rating'].mean().idxmax()
                            highest_avg_rating_country = df[df['country'] == roaster_location_type].groupby('roaster')['rating'].mean().max()
                            st.markdown(f"**The Best Roaster in {roaster_location_type} is...** 🏆")
                            time.sleep(1)
                            st.markdown(f"**Name:**\n\n✨ *{best_roaster_country}* ✨")
                            time.sleep(1)
                            st.markdown(f"**Average Rating:** {highest_avg_rating_country:.2f}")

                    elif roaster_fact_type == "Worst":
                        if roaster_location_type == "Worldwide":
                            worst_roaster = df.groupby('roaster')['rating'].mean().idxmin()
                            lowest_avg_rating = df.groupby('roaster')['rating'].mean().min()
                            st.markdown("**The Worst Roaster Worldwide is...** 🌍💔")
                            time.sleep(1)
                            st.markdown(f"**Name:**\n\n💀 *{worst_roaster}* 💀")
                            time.sleep(1)
                            st.markdown(f"**Average Rating:** {lowest_avg_rating:.2f}")
                        else:
                            worst_roaster_country = df[df['country'] == roaster_location_type].groupby('roaster')['rating'].mean().idxmin()
                            lowest_avg_rating_country = df[df['country'] == roaster_location_type].groupby('roaster')['rating'].mean().min()
                            st.markdown(f"**The Worst Roaster in {roaster_location_type} is...** 💔")
                            time.sleep(1)
                            st.markdown(f"**Name:**\n\n💀 *{worst_roaster_country}* 💀")
                            time.sleep(1)
                            st.markdown(f"**Average Rating:** {lowest_avg_rating_country:.2f}")

                    elif roaster_fact_type == "Most Expensive":
                        if roaster_location_type == "Worldwide":
                            most_expensive_roaster = df.groupby('roaster')['price_per_ounce'].mean().idxmax()
                            highest_avg_price = df.groupby('roaster')['price_per_ounce'].mean().max()
                            st.markdown("**The Most Expensive Roaster Worldwide is...** 💎💲")
                            time.sleep(1)
                            st.markdown(f"**Name:**\n\n💲 *{most_expensive_roaster}* 💲")
                            time.sleep(1)
                            st.markdown(f"**Average Price:** ${highest_avg_price:.2f} per ounce")
                        else:
                            most_expensive_roaster_country = df[df['country'] == roaster_location_type].groupby('roaster')['price_per_ounce'].mean().idxmax()
                            highest_avg_price_country = df[df['country'] == roaster_location_type].groupby('roaster')['price_per_ounce'].mean().max()
                            st.markdown(f"**The Most Expensive Roaster in {roaster_location_type} is...** 💎💲")
                            time.sleep(1)
                            st.markdown(f"**Name:**\n\n💲 *{most_expensive_roaster_country}* 💲")
                            time.sleep(1)
                            st.markdown(f"**Average Price:** ${highest_avg_price_country:.2f} per ounce")

                    elif roaster_fact_type == "Most Affordable":
                        if roaster_location_type == "Worldwide":
                            cheapest_roaster = df.groupby('roaster')['price_per_ounce'].mean().idxmin()
                            lowest_avg_price = df.groupby('roaster')['price_per_ounce'].mean().min()
                            st.markdown("**The Most Affordable Roaster Worldwide is...** 🤝💸")
                            time.sleep(1)
                            st.markdown(f"**Name:**\n\n💸 *{cheapest_roaster}* 💸")
                            time.sleep(1)
                            st.markdown(f"**Average Price:** ${lowest_avg_price:.2f} per ounce")
                        else:
                            cheapest_roaster_country = df[df['country'] == roaster_location_type].groupby('roaster')['price_per_ounce'].mean().idxmin()
                            lowest_avg_price_country = df[df['country'] == roaster_location_type].groupby('roaster')['price_per_ounce'].mean().min()
                            st.markdown(f"**The Most Affordable Roaster in {roaster_location_type} is...** 🤝💸")
                            time.sleep(1)
                            st.markdown(f"**Name:**\n\n💸 *{cheapest_roaster_country}* 💸")
                            time.sleep(1)
                            st.markdown(f"**Average Price:** ${lowest_avg_price_country:.2f} per ounce")
    
    # Navigation button to recommendation page
    st.sidebar.title("Navigation")
    if st.sidebar.button("Go to Recommendation System", type="primary"):
        st.switch_page("pages/recommendation.py")

if __name__ == "__main__":
    run_dataset_explorer()