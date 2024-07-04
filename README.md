# Health-Conscious Breakfast Product Dashboard

## Overview

The Health-Conscious Breakfast Product Dashboard is a web application designed to help users explore and compare the nutritional values of various breakfast products. The app provides interactive visualizations and the ability to query nutritional information and recommendations using the OpenAI GPT API.

[LINK TO THE IMPROVEMENTS](https://drive.google.com/drive/folders/1aXjUMYx8VTlIlIYtPOmRzY9vSETQMPgq?usp=drive_link)

## Features

1. **Category Filter and Product Table**: Filter breakfast products by category and brand, and display the filtered results in a table.
2. **Nutritional Analysis and Segmentation**: Visualize the nutritional content of breakfast products in a scatter plot.
3. **Query Section**: Enter a query to get nutritional recommendations and information based on user preferences.
4. **Single Product Analysis**: Select a product to view detailed nutritional information in a radar chart.
5. **Product Comparison**: Compare the nutritional values of two selected products using a detailed table with highlighted lower values.

## Files in the Repository

- `final_preprocessed_breakfast_products_with_health_score.csv`: The main dataset containing cleaned and preprocessed nutritional data for breakfast products.
- `requirements-3.txt`: A list of Python dependencies required to run the app.
- `app.py`: The main Dash application script.
- `categories/`: A folder containing individual CSV files for each breakfast product category.

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements-3.txt
   ```

4. **Add your OpenAI API key**:
   - Open `app.py` and replace `your_openai_api_key_here` with your actual OpenAI API key.

5. **Run the app**:
   ```bash
   python app.py
   ```

6. **Access the app**:
   - Open your web browser and navigate to `http://127.0.0.1:3000`.

## How to Use the App

1. **Category Filter and Product Table**:
   - Select a macro category from the dropdown menu.
   - Optionally, select a brand and the number of rows to display.
   - The filtered products will be displayed in the table below.

2. **Nutritional Analysis and Segmentation**:
   - A scatter plot will show the sugar vs. fat content of the products in the selected category.
   - Click on any point in the scatter plot to view detailed information about the selected product.

3. **Query Section**:
   - Enter a query in the input box (e.g., "I want a low-sugar cereal").
   - Click the "Submit" button to get recommendations and information based on your query.

4. **Single Product Analysis**:
   - Select a macro category and a product from the dropdown menus.
   - A radar chart will display the detailed nutritional information of the selected product.

5. **Product Comparison**:
   - Select a macro category and two products to compare.
   - Click the "Compare" button to view a detailed table comparing the nutritional values of the selected products with the lower values highlighted in green.

## Adjustments Made According to Feedback

1. **Normalization of Nutritional Values**:
   - Implemented Min-Max normalization for nutritional values (sugars, fat, calories, fiber, proteins, and salt) to scale all values to a common range, making direct comparison easier.

2. **Improved Visualization**:
   - Replaced the single product analysis bar chart with a radar chart to effectively visualize multiple nutritional variables on a common scale.
   - Updated the product comparison to use a detailed table for clearer visual representation of differences in nutritional values, highlighting the lower values in green.

3. **Interactive Plot Click Events**:
   - Added interactivity to the scatter plot by implementing callbacks that respond to plot click events. Detailed information about the clicked product is displayed when a point in the scatter plot is clicked.

4. **Enhanced Text Formatting for ChatGPT Recommendations**:
   - Successfully implemented `dcc.Markdown` to improve the formatting of the ChatGPT-generated text for better readability and structure.

5. **Division into Four Tabs**:
   - The app is now divided into four tabs: Product Table, Query Section, Single Product Analysis, and Product Comparison for better organization and navigation.

## Known Issues

- **None**: All previously known issues have been addressed.

## Conclusion

The Health-Conscious Breakfast Product Dashboard provides a comprehensive tool for exploring and comparing the nutritional values of breakfast products. The app leverages interactive visualizations and AI-powered recommendations to help users make informed choices about their breakfast options. Further improvements and iterations will continue to enhance the user experience and address any existing challenges.

---
