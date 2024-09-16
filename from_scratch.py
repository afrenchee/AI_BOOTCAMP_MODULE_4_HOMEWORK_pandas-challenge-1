import pandas as pd



import os, sys
windows_is_the_OS = False # This variable is set by the main programmer to ensure that Terminal / Command Prompt commands are correctly executed in clear_screen() and end_program()



def clear_screen(): # You best be usin a terminal or powershell for this code!!!
	if windows_is_the_OS:
		os.system('cls')
	else:
		os.system('clear')



if __name__ == "__main__":
	clear_screen()
	print("Pandas Challange 1!!!\n")



	# PART 1
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


