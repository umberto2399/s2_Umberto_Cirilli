import dash
from dash import dcc, html, Input, Output, State
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import openai
from sklearn.preprocessing import MinMaxScaler

# Load the cleaned data
df = pd.read_csv('final_preprocessed_breakfast_products_with_health_score.csv')

# Min-Max Normalization
scaler = MinMaxScaler()
df[['sugars_value', 'fat_value', 'energy-kcal_value', 'fiber_value', 'proteins_value', 'salt_value']] = scaler.fit_transform(
    df[['sugars_value', 'fat_value', 'energy-kcal_value', 'fiber_value', 'proteins_value', 'salt_value']])

# Initialize the OpenAI API
client = openai.OpenAI(api_key='Your API Key Here')

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Health-Conscious Breakfast Product Dashboard", style={'text-align': 'center'}),
    html.P("Explore and compare the nutritional values of various breakfast products to make healthier choices.", style={'text-align': 'center'}),
    
    dcc.Tabs([
        dcc.Tab(label='Product Table', children=[
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='macro-category-dropdown',
                        options=[{'label': cat, 'value': cat} for cat in df['macro_category'].unique()],
                        placeholder='Select a macro category',
                        style={'margin-bottom': '10px'}
                    ),
                    dcc.Dropdown(
                        id='brand-dropdown',
                        placeholder='Select a brand',
                        style={'margin-bottom': '10px'}
                    ),
                    dcc.Dropdown(
                        id='row-dropdown',
                        options=[
                            {'label': '10', 'value': 10},
                            {'label': '25', 'value': 25},
                            {'label': '50', 'value': 50},
                            {'label': 'All', 'value': 'All'}
                        ],
                        value=10,
                        placeholder='Select number of rows to display',
                        style={'margin-bottom': '10px'}
                    ),
                    dash_table.DataTable(
                        id='product-table',
                        page_size=10,
                        style_table={'overflowX': 'auto'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'left', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([
                    dcc.Graph(id='nutritional-scatter')
                ], style={'width': '50%', 'display': 'inline-block'})
            ]),
            html.Div(id='clicked-product-info', style={'margin-top': '20px'})
        ]),
        dcc.Tab(label='Query Section', children=[
            html.Div([
                html.H2("Enter Your Query", style={'text-align': 'center'}),
                html.P("Ask for nutritional information or recommendations based on your preferences.", style={'text-align': 'center'}),
                dcc.Input(id='user-query', type='text', placeholder='Enter your query...', style={'width': '80%', 'margin': '0 auto', 'display': 'block'}),
                html.Button('Submit', id='query-button', style={'display': 'block', 'margin': '10px auto'}),
                html.Div(id='query-results', style={'margin-top': '20px'})
            ])
        ]),
        dcc.Tab(label='Single Product Analysis', children=[
            html.Div([
                html.H2("Single Product Analysis", style={'text-align': 'center'}),
                html.P("Select a macro category and a product to view detailed nutritional information.", style={'text-align': 'center'}),
                dcc.Dropdown(
                    id='macro-category-dropdown-single',
                    options=[{'label': category, 'value': category} for category in df['macro_category'].unique()],
                    placeholder='Select a macro category',
                    style={'margin': '10px auto', 'width': '80%'}
                ),
                dcc.Dropdown(id='product-dropdown-single', placeholder='Select a product', style={'margin': '10px auto', 'width': '80%'}),
                dcc.Graph(id='single-product-graph')
            ])
        ]),
        dcc.Tab(label='Compare Two Products', children=[
            html.Div([
                html.H2("Compare Two Products", style={'text-align': 'center'}),
                html.P("Select two products to compare their nutritional values.", style={'text-align': 'center'}),
                dcc.Dropdown(
                    id='macro-category-dropdown-compare',
                    options=[{'label': category, 'value': category} for category in df['macro_category'].unique()],
                    placeholder='Select a macro category',
                    style={'margin': '10px auto', 'width': '80%'}
                ),
                dcc.Dropdown(id='brand-dropdown-compare-1', placeholder='Select first brand', style={'margin': '10px auto', 'width': '80%'}),
                dcc.Dropdown(id='brand-dropdown-compare-2', placeholder='Select second brand', style={'margin': '10px auto', 'width': '80%'}),
                dcc.Dropdown(id='compare-product-1', placeholder='Select first product', style={'margin': '10px auto', 'width': '80%'}),
                dcc.Dropdown(id='compare-product-2', placeholder='Select second product', style={'margin': '10px auto', 'width': '80%'}),
                html.Button('Compare', id='compare-button', style={'display': 'block', 'margin': '10px auto'}),
                html.Div(id='comparison-results', style={'margin-top': '20px'}),
                html.Div(id='comparison-graph')
            ])
        ])
    ])
])

# Callback to update brand dropdown based on selected macro category
@app.callback(
    Output('brand-dropdown', 'options'),
    [Input('macro-category-dropdown', 'value')]
)
def update_brand_options(selected_macro_category):
    if selected_macro_category:
        filtered_df = df[df['macro_category'] == selected_macro_category]
        brands = filtered_df['brands'].unique()
        return [{'label': brand, 'value': brand} for brand in brands]
    return []

# Callback to update product table based on selected category and brand
@app.callback(
    Output('product-table', 'data'),
    [Input('macro-category-dropdown', 'value'), Input('brand-dropdown', 'value'), Input('row-dropdown', 'value')]
)
def update_table(selected_macro_category, selected_brand, num_rows):
    filtered_df = df.copy()
    if selected_macro_category:
        filtered_df = filtered_df[filtered_df['macro_category'] == selected_macro_category]
    if selected_brand:
        filtered_df = filtered_df[filtered_df['brands'] == selected_brand]
    if num_rows != 'All':
        filtered_df = filtered_df.head(num_rows)
    return filtered_df.to_dict('records')

# Callback to update nutritional scatter plot based on selected category
@app.callback(
    Output('nutritional-scatter', 'figure'),
    [Input('macro-category-dropdown', 'value')]
)
def update_scatter(selected_macro_category):
    if selected_macro_category:
        filtered_df = df[df['macro_category'] == selected_macro_category]
    else:
        filtered_df = df
    fig = px.scatter(filtered_df, x='sugars_value', y='fat_value', color='macro_category',
                     title='Sugar vs Fat Content (Normalized)',
                     hover_data={'product_name_es': True, 'sugars_value': True, 'fat_value': True, 'macro_category': True})
    return fig

# Combined callback for query processing and plot click events
@app.callback(
    [Output('query-results', 'children'), Output('clicked-product-info', 'children')],
    [Input('query-button', 'n_clicks'), Input('nutritional-scatter', 'clickData')],
    [State('user-query', 'value')]
)
def handle_query_and_click(n_clicks, clickData, user_query):
    ctx = dash.callback_context

    query_results = "Submit a query or click on a point in the scatter plot to see details."
    clicked_product_info = ""

    if not ctx.triggered:
        return query_results, clicked_product_info

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'query-button' and n_clicks and user_query:
        prompt = f"You need to extract the following information from a short text and I will provide to you: macro_category. For the macro_category you can choose only from this values without altering them (do not change the way they are written cause I am going to use them to make a query hence I need exactly those names): milk, muffins, croissants, honey, jam, peanut_butter, fresh_fruit, fruit_juice, hot_drink, yogurt, cereals, cereal_bars. Example: User Input: 'I want cereal with milk for breakfast' Example of Output: ['cereals', 'milk']. As you can see the output must be a list in which you can put all the categories that you detect inside the user input. User Input: '{user_query}'"
        
        response_extraction = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts information from text."},
                {"role": "user", "content": prompt}
            ]
        )
        
        categories = eval(response_extraction.choices[0].message.content.strip())
        
        recommendations = ""
        for category in categories:
            category_df = df[(df['macro_category'] == category) & (df['sugars_value'] > 0) & (df['fat_value'] > 0) & (df['energy-kcal_value'] > 0)]
            if category_df.empty:
                continue
                
            lowest_sugar = category_df.nsmallest(1, 'sugars_value').to_dict('records')[0]
            lowest_fat = category_df.nsmallest(1, 'fat_value').to_dict('records')[0]
            lowest_calories = category_df.nsmallest(1, 'energy-kcal_value').to_dict('records')[0]
            
            options = [lowest_sugar, lowest_fat, lowest_calories]
            prompt = (
                f"We need you to decide for the category '{category}' which one is the healthiest product since our user wants this '{user_query}'. "
                f"Those are the products you have to choose from:\n"
                f"Product 1:\n{lowest_sugar}\n\n"
                f"Product 2:\n{lowest_fat}\n\n"
                f"Product 3:\n{lowest_calories}\n\n"
                f"Please be synthetic and provide the name of the product for each category that you think is the healthiest and a couple of motivations for why."
            )
            
            response_decision = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides nutritional recommendations."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = response_decision.choices[0].message.content.strip()
            # Format the title and motivations
            title = f"### Healthiest Options - {category.capitalize()}"
            lines = response_text.split("**Motivations:**")
            description = lines[0].replace("###", "").strip()
            motivations = lines[1].strip() if len(lines) > 1 else ""

            # Combine parts
            recommendations += f"{title}\n\n{description}\n\n**Motivations:**\n{motivations}\n\n"

        query_results = dcc.Markdown(recommendations)

    elif trigger_id == 'nutritional-scatter' and clickData:
        point = clickData['points'][0]
        product_name = point['customdata'][0]
        clicked_product = df[df['product_name_es'] == product_name].iloc[0]
        clicked_product_info = html.Div([
            html.H3(f"Product Name: {clicked_product['product_name_es']}"),
            html.P(f"Sugar Value: {clicked_product['sugars_value']}"),
            html.P(f"Fat Value: {clicked_product['fat_value']}"),
            html.P(f"Energy (kcal): {clicked_product['energy-kcal_value']}"),
            html.P(f"Fiber Value: {clicked_product['fiber_value']}"),
            html.P(f"Proteins Value: {clicked_product['proteins_value']}"),
            html.P(f"Salt Value: {clicked_product['salt_value']}")
        ])

    return query_results, clicked_product_info

# Callback to update product dropdown in single product section based on selected macro category
@app.callback(
    Output('product-dropdown-single', 'options'),
    [Input('macro-category-dropdown-single', 'value')]
)
def update_product_options_single(selected_macro_category):
    if selected_macro_category:
        filtered_df = df[df['macro_category'] == selected_macro_category]
        return [{'label': product, 'value': product} for product in filtered_df['product_name_es'].unique()]
    return []

# Callback to update single product graph based on selected product
@app.callback(
    Output('single-product-graph', 'figure'),
    [Input('product-dropdown-single', 'value')]
)
def update_single_product_graph(selected_product):
    if selected_product:
        product_details = df[df['product_name_es'] == selected_product].iloc[0]
        product_data = product_details[['sugars_value', 'fat_value', 'energy-kcal_value', 'fiber_value', 'proteins_value', 'salt_value']]
        product_data = product_data[product_data > 0]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=product_data.values,
            theta=product_data.index,
            fill='toself'
        ))
        fig.update_layout(title=f'Nutritional Information for {selected_product}', hovermode='closest')
        return fig
    return {}

# Callback to update brand dropdown in comparison section based on selected macro category
@app.callback(
    [Output('brand-dropdown-compare-1', 'options'),
     Output('brand-dropdown-compare-2', 'options')],
    [Input('macro-category-dropdown-compare', 'value')]
)
def update_brand_options_compare(selected_macro_category):
    if selected_macro_category:
        filtered_df = df[df['macro_category'] == selected_macro_category]
        brands = filtered_df['brands'].unique()
        return ([{'label': brand, 'value': brand} for brand in brands], 
                [{'label': brand, 'value': brand} for brand in brands])
    return ([], [])

# Callback to update first product dropdown in comparison section based on selected macro category and brand
@app.callback(
    Output('compare-product-1', 'options'),
    [Input('macro-category-dropdown-compare', 'value'), Input('brand-dropdown-compare-1', 'value')]
)
def update_product1_options_compare(selected_macro_category, selected_brand_1):
    filtered_df = df.copy()
    if selected_macro_category:
        filtered_df = filtered_df[filtered_df['macro_category'] == selected_macro_category]
    if selected_brand_1:
        filtered_df = filtered_df[filtered_df['brands'] == selected_brand_1]
    return [{'label': product, 'value': product} for product in filtered_df['product_name_es'].unique()]

# Callback to update second product dropdown in comparison section based on selected macro category and brand
@app.callback(
    Output('compare-product-2', 'options'),
    [Input('macro-category-dropdown-compare', 'value'), Input('brand-dropdown-compare-2', 'value')]
)
def update_product2_options_compare(selected_macro_category, selected_brand_2):
    filtered_df = df.copy()
    if selected_macro_category:
        filtered_df = filtered_df[filtered_df['macro_category'] == selected_macro_category]
    if selected_brand_2:
        filtered_df = filtered_df[filtered_df['brands'] == selected_brand_2]
    return [{'label': product, 'value': product} for product in filtered_df['product_name_es'].unique()]

# Callback to update the product comparison based on selected products
@app.callback(
    Output('comparison-results', 'children'),
    [Input('compare-button', 'n_clicks')],
    [State('compare-product-1', 'value'), State('compare-product-2', 'value')]
)
def compare_products(n_clicks, product1, product2):
    if n_clicks and product1 and product2:
        product1_details = df[df['product_name_es'] == product1].iloc[0].to_dict()
        product2_details = df[df['product_name_es'] == product2].iloc[0].to_dict()
        
        prompt = (
            f"We need you to decide which one is the healthiest product. "
            f"Those are the products you have to choose from:\n"
            f"Product 1:\n{product1_details}\n\n"
            f"Product 2:\n{product2_details}\n\n"
            f"Please be synthetic and provide the name of the product that you think is the healthiest and a couple of motivations for why."
            f"Take into account that when an attribute is equal to zero it could be just for the strategy we used to impute missing values hence use also common sense (I mean if one of the product is a twix it is not possible it doesn't have any sugar/flat/salt)."
        )
        
        response_comparison = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides nutritional recommendations."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Formatting the comparison results
        comparison_results = response_comparison.choices[0].message.content.strip()
        comparison_results = dcc.Markdown(comparison_results)
        return comparison_results
    return ""

@app.callback(
    Output('comparison-graph', 'children'),
    [Input('compare-button', 'n_clicks')],
    [State('compare-product-1', 'value'), State('compare-product-2', 'value')]
)
def update_comparison_graph(n_clicks, product1, product2):
    if n_clicks and product1 and product2:
        product1_details = df[df['product_name_es'] == product1].iloc[0]
        product2_details = df[df['product_name_es'] == product2].iloc[0]
        
        nutritional_values = ['sugars_value', 'fat_value', 'energy-kcal_value', 'fiber_value', 'proteins_value', 'salt_value']
        
        data = []
        for nutrient in nutritional_values:
            product1_value = product1_details[nutrient]
            product2_value = product2_details[nutrient]
            lower_value = ''
            if product1_value < product2_value and product1_value != 0:
                lower_value = 'Product 1'
            elif product2_value < product1_value and product2_value != 0:
                lower_value = 'Product 2'
            data.append({
                'Nutritional Value': nutrient,
                'Product 1': product1_value,
                'Product 2': product2_value,
                'Lower Value': lower_value
            })
        
        columns = [
            {'name': 'Nutritional Value', 'id': 'Nutritional Value'},
            {'name': product1_details['product_name_es'], 'id': 'Product 1'},
            {'name': product2_details['product_name_es'], 'id': 'Product 2'},
            {'name': 'Lower Value', 'id': 'Lower Value', 'hideable': True}
        ]
        
        style_data_conditional = [
            {
                'if': {
                    'filter_query': '{Lower Value} = "Product 1"',
                    'column_id': 'Product 1'
                },
                'backgroundColor': 'green',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{Lower Value} = "Product 2"',
                    'column_id': 'Product 2'
                },
                'backgroundColor': 'green',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{Lower Value} = ""',
                },
                'backgroundColor': 'white',
                'color': 'black'
            }
        ]
        
        table = dash_table.DataTable(
            data=data,
            columns=columns,
            style_data_conditional=style_data_conditional,
            style_cell={'textAlign': 'center'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )
        
        return table
    return html.Div()

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
