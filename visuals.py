import matplotlib.pyplot as plt
import streamlit as st

def plot_feature_comparison(input_coffees, recommended_coffee, df):
    """
    Plots a bar chart comparing the features of input coffees and the recommended coffee.

    Parameters:
        input_coffees (list): List of input coffee names.
        recommended_coffee (str): Name of the recommended coffee.
        df (DataFrame): Coffee dataset containing feature data.
    """
    # Extract feature data for input and recommended coffees
    input_features = []
    for coffee_name in input_coffees:
        coffee_data = df[df['name'] == coffee_name][['aroma', 'acid', 'body', 'flavor', 'aftertaste']]
        if not coffee_data.empty:
            input_features.append(coffee_data.iloc[0].values)  # First row's features as array

    recommended_data = df[df['name'] == recommended_coffee][['aroma', 'acid', 'body', 'flavor', 'aftertaste']]
    if not recommended_data.empty:
        recommended_features = recommended_data.iloc[0].values  # First row's features as array
    else:
        st.error("Recommended coffee not found in dataset.")
        return

    # Create the bar chart
    feature_labels = ['Aroma', 'Acid', 'Body', 'Flavor', 'Aftertaste']
    input_features.append(recommended_features)  # Add recommended coffee features for comparison

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2
    positions = list(range(len(feature_labels)))

    # Plot input coffee features
    for i, features in enumerate(input_features[:-1]):
        ax.bar(
            [p + i * bar_width for p in positions],
            features,
            bar_width,
            label=f"Input Coffee {i + 1}",
        )

    # Plot recommended coffee features
    ax.bar(
        [p + len(input_features[:-1]) * bar_width for p in positions],
        recommended_features,
        bar_width,
        label="Recommended Coffee",
        color="orange",
    )

    # Add labels and legend
    ax.set_xticks([p + bar_width * len(input_features[:-1]) / 2 for p in positions])
    ax.set_xticklabels(feature_labels)
    ax.set_ylabel("Feature Values")
    ax.set_title("Feature Comparison: Input vs. Recommended Coffee")
    ax.legend()

    st.pyplot(fig)




# visuals.py

import matplotlib.pyplot as plt
import streamlit as st

def plot_categorical_comparison(input_coffees, recommended_coffee, df, categorical_features):
    """
    Plots a grouped bar chart comparing categorical features of input coffees and the recommended coffee.

    Parameters:
        input_coffees (list): List of input coffee names.
        recommended_coffee (str): Name of the recommended coffee.
        df (DataFrame): Coffee dataset containing categorical data.
        categorical_features (list): List of categorical feature column names to compare.
    """
    # Extract data for input and recommended coffees
    input_data = []
    for coffee_name in input_coffees:
        coffee_row = df[df['name'] == coffee_name]
        if not coffee_row.empty:
            input_data.append(coffee_row.iloc[0][categorical_features])

    recommended_row = df[df['name'] == recommended_coffee]
    if not recommended_row.empty:
        recommended_data = recommended_row.iloc[0][categorical_features]
    else:
        st.error("Recommended coffee not found in dataset.")
        return

    # Combine data into a DataFrame for plotting
    data = input_data + [recommended_data]
    labels = [f"Input Coffee {i + 1}" for i in range(len(input_data))] + ["Recommended Coffee"]

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2
    positions = range(len(categorical_features))

    for i, row in enumerate(data):
        ax.bar(
            [p + i * bar_width for p in positions],
            [1 if value == row[feature] else 0 for feature, value in row.items()],
            bar_width,
            label=labels[i],
        )

    # Formatting
    ax.set_xticks([p + bar_width * len(data) / 2 for p in positions])
    ax.set_xticklabels(categorical_features, rotation=45, ha='right')
    ax.set_ylabel("Match (1=Yes, 0=No)")
    ax.set_title("Categorical Comparison: Input vs. Recommended Coffee")
    ax.legend()

    st.pyplot(fig)
