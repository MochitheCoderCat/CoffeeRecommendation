# Coffee Recommendation System

"""
To locally run this app, in your terminal:
> streamlit run main.py

"""

# Coffee Dataset Explorer

## Overview
This project is a Streamlit application for exploring coffee datasets, visualizing various features, and providing recommendations.

## Prerequisites
- Docker installed on your machine.

## Getting Started with Docker

### Build the Docker Image
1. Clone the repository or navigate to the project directory.
2. Ensure you have a `requirements.txt` file in the root of your project directory.
3. Open a terminal and run the following command to build the Docker image:
   ```bash
   docker build -t coffee-dataset-explorer .
   ```

### Run the Docker Container
After building the image, you can run the container with the following command:
    ```bash
   docker run -p 8501:8501 coffee-dataset-explorer
   ```

### Access the Application
Once the container is running, open your web browser and go to:
    ```
    http://localhost:8501
    ```
