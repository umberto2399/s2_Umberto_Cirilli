import pandas as pd
import glob

# List of relevant columns to keep
relevant_columns = [
    'product_name_en', 'product_name_es', 'brands', 'categories', 'quantity', 'serving_size',
    'energy-kcal_value', 'sugars_value', 'fat_value', 'saturated-fat_value',
    'proteins_value', 'salt_value', 'fiber_value', 'ingredients_text_es'
]

# List of all CSV files in the current directory
csv_files = glob.glob("*.csv")

# Function to read and clean each CSV
def read_and_clean_csv(file):
    try:
        df = pd.read_csv(file, delimiter='\t', on_bad_lines='skip', low_memory=False)
        # Select only the relevant columns if they exist in the dataframe
        df = df[[col for col in relevant_columns if col in df.columns]]
        # Add the macro_category column
        df['macro_category'] = file.split('.')[0]
        return df
    except Exception as e:
        print(f"Error reading {file}: {e}")
        return pd.DataFrame()  # Return empty dataframe on error

# Read, clean, and combine all CSV files
all_dfs = [read_and_clean_csv(file) for file in csv_files]
combined_df = pd.concat(all_dfs, ignore_index=True)

print(f'Combined dataframe shape: {combined_df.shape}')


# Save the cleaned dataframe to a new CSV file
combined_df.to_csv('final_cleaned_breakfast_products_with_macro_category.csv', index=False)

print("Data extraction and preparation completed. Combined data saved to 'final_cleaned_breakfast_products_with_macro_category.csv'.")
