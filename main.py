import streamlit as st

def main():
    st.title("Coffee Analysis and Recommendation System")
    st.write("""
    Welcome to the Coffee Analysis and Recommendation System! 
    This application helps you explore coffee data and get personalized recommendations.
    """)
    
    st.header("Available Pages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Dataset Explorer"):
            st.switch_page("pages/dataset_explorer.py")
        st.write("Explore the coffee dataset, view statistics, and visualize distributions.")
            
    with col2:
        if st.button("Recommendation System"):
            st.switch_page("pages/recommendation.py")
        st.write("Get personalized coffee recommendations based on your preferences.")

if __name__ == "__main__":
    main()