README: Assignment 2

Name: Umberto Cirilli

LINK TO THE RECORDING:

Recording Link: https://esade.zoom.us/rec/share/6avIJ3X3x2BUhvrkYsRExT9ucdZAr9hiA8BJQOUoHGOAkbwHoL82a-YHdBUrsFrB.TFmSuj8HeSKLLFdW  Codice d’accesso: CA6@^m!=


Description of the app:

Health-Conscious Breakfast Product Dashboard
Overview

The Health-Conscious Breakfast Product Dashboard is a web application designed to help users explore and compare the nutritional values of various breakfast products. This tool aims to assist users in making healthier choices by providing detailed nutritional information and personalised recommendations based on user queries.

Features

Category Filter and Product Table: Allows users to filter products by macro category and brand, and view the filtered products in a table format.
Nutritional Analysis and Segmentation: Displays a scatter plot of sugar versus fat content for the selected macro category.
User Queries and Recommendations: Users can input their queries to get personalised nutritional recommendations using OpenAI's GPT model.
Single Product Analysis: Provides detailed nutritional information for a selected product.
Product Comparison: Allows users to compare the nutritional values of two selected products.
Needed Libraries

Python 3.7+
Dash
pandas
plotly
openai
Application Structure and Logic

Layout
The layout of the app is defined using Dash's HTML and core components. It includes headers, dropdowns for filtering, input fields for queries, tables for displaying data, and graphs for visual representation.

Callbacks
Callbacks are used to make the app interactive. They update the app's components in response to user inputs. The key callbacks in this app are:

update_brand_options: Updates the brand dropdown based on the selected macro category.
update_table: Updates the product table based on the selected category, brand, and number of rows.
update_scatter: Updates the scatter plot based on the selected macro category.
process_query: Processes user queries and provides nutritional recommendations using the OpenAI API.
update_product_options_single: Updates the product dropdown in the single product section based on the selected macro category.
update_single_product_graph: Updates the graph showing detailed nutritional information for the selected product.
update_brand_options_compare: Updates the brand dropdowns in the comparison section based on the selected macro category.
update_product1_options_compare: Updates the first product dropdown in the comparison section based on the selected macro category and brand.
update_product2_options_compare: Updates the second product dropdown in the comparison section based on the selected macro category and brand.
compare_products: Compares the selected products and provides a summary of the comparison.
update_comparison_graph: Updates the graph showing the comparison of the selected products.
API Calls and Logic
The app uses OpenAI's GPT 4o model to handle user queries and provide recommendations. Here is a breakdown of how the API calls and logic work:

Processing User Queries:

When a user submits a query, the process_query callback is triggered.
The user's query is sent to the OpenAI API with a prompt designed to extract relevant macro categories.
The response is parsed to get the list of categories.
For each category, the app selects the products with the lowest sugar, fat, and calorie values.
These options are sent to the OpenAI API to determine the healthiest product based on the user's query.
The API's response is displayed to the user as recommendations.
Single Product Analysis:

When a user selects a product, the update_single_product_graph callback is triggered.
The detailed nutritional information for the selected product is extracted and displayed in a bar chart.
Product Comparison:

When users select two products to compare, the compare_products and update_comparison_graph callbacks are triggered.
The detailed nutritional information for both products is extracted.
The OpenAI API is used to determine which product is healthier based on the comparison.
A bar chart is generated to visually compare the nutritional values of the two products.
Tools Used

Dash: For building the interactive web application.
pandas: For data manipulation and analysis.
plotly: For creating interactive graphs and plots.
openai: For generating personalized nutritional recommendations based on user queries.
