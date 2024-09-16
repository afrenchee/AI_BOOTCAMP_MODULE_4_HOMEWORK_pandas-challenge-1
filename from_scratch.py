import pandas as pd



import os, sys, math
windows_is_the_OS = False # This variable is set by the main programmer to ensure that Terminal / Command Prompt commands are correctly executed in clear_screen() and end_program()



def clear_screen(): # You best be usin a terminal or powershell for this code!!!
	if windows_is_the_OS:
		os.system('cls')
	else:
		os.system('clear')



if __name__ == "__main__":
	clear_screen()
	print("\n\n\nPandas Challange 1 BEGINS!!!\n")



	# PART 1: Explore the Data
	# Import the data from the CSV file.
	df = pd.read_csv('Resources/client_dataset.csv')

	# View the column names
	print("Colums:\n", df.columns)
	print("") # Add some empty space between print statement

	# Use the describe function to gather some basic statistics.
	print("Description:\n", df.describe())

	# Identify the three item categories with the most entries
	top_3_categories = df['category'].value_counts().head(3)
	print("\nTop 3 categories with the most entries:")
	for category, count in top_3_categories.items(): # For loop used to avoid printing "category" above listed items and "Name: count, dtype: int64" below
		print(f"{category}: {count}")
	print("")

	# Identify the category with the most entries from the top 3
	top_category = top_3_categories.idxmax()
	print(f"The category with the most entries among the top 3 is: {top_category}\n")

	# For the category with the most entries, correctly identify the subcategory with the most entries.
	top_subcategory = df[df['category'] == top_category]['subcategory'].value_counts().idxmax()
	print(f"The subcategory with the most entries in {top_category} is: {top_subcategory}\n")

	# Correctly identify the 5 clients with the most entries in the data.
	top_5_clients = df['client_id'].value_counts().head(5)
	top_5_client_names = df[df['client_id'].isin(top_5_clients.index)][['client_id', 'first', 'last']].drop_duplicates()
	top_5_client_info = pd.merge(top_5_client_names, top_5_clients, on='client_id')
	top_5_client_info_sorted = top_5_client_info.sort_values(by='count', ascending=False)
	print("Top 5 clients with the most entries:")
	number = 0
	for index, row in top_5_client_info_sorted.iterrows():
		number += 1
		print(f"{number}. {row['first']} {row['last']} (ID: {row['client_id']}): {row['count']} entries")
	print("")

	# Store the client ids of those top 5 clients in a list.
	top_5_client_ids = top_5_clients.index.tolist()
	print(f"Top 5 client IDs: {top_5_client_ids}\n")

	# Display the total units (the qty column) that the client with the most entries ordered.
	total_qty_top_client = df[df['client_id'] == top_5_client_ids[0]]['qty'].sum()
	print(f"Total units ordered by the top client: {total_qty_top_client}\n")



	# PART 2: Transform the Data
	# Create a column that calculates the subtotal for each line using the unit_price and qty.
	df['line_subtotal'] = df['unit_price'] * df['qty']
	print(f"Added 'line_subtotal' column:\n{df[['unit_price', 'qty', 'line_subtotal']].head()}\n")

	# Create a column for shipping price
	# Assume $7 per pound for orders over 50 pounds and $10 per pound for orders 50 pounds or under.
	df['total_weight'] = df['unit_weight'] * df['qty']
	df['shipping_price'] = df['total_weight'].apply(lambda x: 7 * x if x > 50 else 10 * x)
	print(f"Added 'shipping_price' column:\n{df[['total_weight', 'shipping_price']].head()}\n")

	# Create a column for the total price
	# Total price = line_subtotal + shipping_price + sales tax (9.25%)
	df['line_price'] = df['line_subtotal'] + df['shipping_price']
	df['line_price_with_tax'] = df['line_price'] * 1.0925
	print(f"Added 'line_price_with_tax' column:\n{df[['line_price', 'line_price_with_tax']].head()}\n")

	# Create a column for the cost of each line using unit cost, qty, and shipping price
	df['line_cost'] = (df['unit_cost'] * df['qty']) + df['shipping_price']
	print(f"Added 'line_cost' column:\n{df[['unit_cost', 'qty', 'line_cost']].head()}\n")

	# Create a column for the profit of each line using line price and line cost
	df['line_profit'] = df['line_price_with_tax'] - df['line_cost']
	print(f"Added 'line_profit' column:\n{df[['line_price_with_tax', 'line_cost', 'line_profit']].head()}\n")



	# PART 3: Confirm Your Work

	# Confirm that Order ID 2742071 had a total price of $152,811.89.
	# Confirm that Order ID 2173913 had a total price of $162,388.71.
	# Confirm that Order ID 6128929 had a total price of $923,441.25.

	# Define the orders and their expected total prices
	order_totals = {
		2742071: 152811.89,
		2173913: 162388.71,
		6128929: 923441.25
	}

	# Loop through each order ID, filter the DataFrame, and calculate the sum of line_price_with_tax
	for order_id, expected_total in order_totals.items():
		# Filter the DataFrame for the specific order_id
		order_data = df[df['order_id'] == order_id].copy()  # Use .copy() to avoid SettingWithCopyWarning

		# Apply rounding to the line_price_with_tax at the individual line level
		order_data.loc[:, 'line_price_with_tax_rounded'] = (order_data['line_price'] * 1.0925).round(2)  # Line-level rounding

		# Calculate the total price for the order using the rounded column
		calculated_total = order_data['line_price_with_tax_rounded'].sum()

		# Print the result and compare with the expected total
		print(f"Order {order_id} calculated total: ${calculated_total:.2f}")
		print(f"Expected total: ${expected_total}")

		# Use math.isclose to compare with a tolerance
		if math.isclose(calculated_total, expected_total, rel_tol=1e-2):  # Allowing a small relative tolerance of 0.01
			print(f"Match: True\n")
		else:
			print(f"Match: False\n")



	# PART 4: Summarize and Analyze

	# Step 1: Calculate total revenue, total units, total shipping, and total profit for each of the top 5 clients.
	summary_data = df[df['client_id'].isin(top_5_client_ids)].groupby('client_id').agg(
		total_units=pd.NamedAgg(column='qty', aggfunc='sum'),
		total_shipping=pd.NamedAgg(column='shipping_price', aggfunc='sum'),
		total_revenue=pd.NamedAgg(column='line_price_with_tax', aggfunc='sum'),
		total_profit=pd.NamedAgg(column='line_profit', aggfunc='sum')
	).reset_index()

	print("Summary data for top 5 clients (before formatting):")
	print(summary_data)

	# Step 2: Function to convert to millions for presentation purposes
	def to_millions(x):
		return round(x / 1e6, 2)

	# Step 3: Apply formatting to the relevant columns
	summary_data['total_revenue_millions'] = summary_data['total_revenue'].apply(to_millions)
	summary_data['total_shipping_millions'] = summary_data['total_shipping'].apply(to_millions)
	summary_data['total_profit_millions'] = summary_data['total_profit'].apply(to_millions)

	# Step 4: Rename columns for presentation
	summary_data_formatted = summary_data[['client_id', 'total_units', 'total_shipping_millions', 'total_revenue_millions', 'total_profit_millions']].copy()
	summary_data_formatted.columns = ['Client ID', 'Total Units', 'Shipping (millions)', 'Revenue (millions)', 'Profit (millions)']

	# Step 5: Sort the summary DataFrame by total profit in descending order
	summary_data_formatted_sorted = summary_data_formatted.sort_values(by='Profit (millions)', ascending=False)

	# Step 6: Print the final sorted summary DataFrame
	print("\nFormatted summary of top 5 clients (sorted by profit):")
	print(summary_data_formatted_sorted)

	# Write a brief summary
	print("\nSummary of Findings:")
	print("The top client by total profit is Client ID", summary_data_formatted_sorted.iloc[0]['Client ID'], "with a profit of", summary_data_formatted_sorted.iloc[0]['Profit (millions)'], "million dollars.")
	print("The second highest is Client ID", summary_data_formatted_sorted.iloc[1]['Client ID'], "with a profit of", summary_data_formatted_sorted.iloc[1]['Profit (millions)'], "million dollars.")




