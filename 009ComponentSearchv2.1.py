import os
import sys
import tkinter as tk
from tkinter import ttk
import sqlite3

def perform_search():
    # Get the part name entered by the user in the text box and remove leading and trailing spaces
    manufacturer_item_pattern = f"%{search_entry.get().strip()}%"
    
    # Connect to the database
    conn = sqlite3.connect(os.path.join(script_dir, 'inventory.db'))
    cursor = conn.cursor()

    # Execute SQL query
    cursor.execute("""
        SELECT product_component.product_name, product_component.component_pmd_pn, product_component.designator, component_item.manufacturer_item
        FROM product_component
        JOIN component_item ON product_component.component_pmd_pn = component_item.item
        WHERE component_item.manufacturer_item LIKE ?
        ORDER BY product_component.product_name ASC
    """, (manufacturer_item_pattern,))

    # Get results
    rows = cursor.fetchall()

    # Use a set to track already added results to prevent duplicates
    unique_results = set()

    # Clear the result text boxes
    result_text1.delete(1.0, tk.END)
    result_text2.delete(1.0, tk.END)

    # Display results in the result text boxes and filter duplicates
    for row in rows:
        result = f"{row[0]} - {row[2]}"
        if result not in unique_results:
            result_text1.insert(tk.END, f"{row[1]}\n")
            result_text2.insert(tk.END, f"{result}\n")
            unique_results.add(result)

    # Close the database connection
    conn.close()

# Get the script's running directory
if getattr(sys, 'frozen', False):
    # When running in PyInstaller
    script_dir = sys._MEIPASS
else:
    # When running as a ".py" script
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the main window
root = tk.Tk()
root.title("Component Search")

# Create a Notebook widget to manage tabs
notebook = ttk.Notebook(root)
notebook.pack()

# First Tab - MFR Search
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="MFR Search")

# Create a label and place it in front of the search box
label = ttk.Label(tab1, text="MFR P/N:")
label.grid(row=0, column=0, padx=5, sticky="w")

# Create a search text box
search_entry = ttk.Entry(tab1)
search_entry.grid(row=0, column=1, padx=5, sticky="w")

# Load an image
image_path = os.path.join(script_dir, 'Convert', 'Magellan-MC58000-144-pmdcorp.png')
search_image = tk.PhotoImage(file=image_path)

# Create a search button and use the image
search_button = ttk.Button(tab1, image=search_image, command=perform_search)
search_button.grid(row=0, column=2, padx=5, sticky="w", rowspan=2)

# Create the first result text box
label1 = ttk.Label(tab1, text="Component PMD P/N:")
label1.grid(row=1, column=0, padx=5, sticky="w")
result_text1 = tk.Text(tab1, wrap=tk.WORD, width=25, height=3)
result_text1.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# Create the second result text box
label2 = ttk.Label(tab1, text="ProductName and Designator:", anchor="center")
label2.grid(row=3, column=0, columnspan=3, padx=5, sticky="nsew")
result_text2 = tk.Text(tab1, wrap=tk.WORD, width=50, height=10)
result_text2.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# Second Tab - ALT Search
tab2 = ttk.Frame(notebook, width=tab1.winfo_width())
notebook.add(tab2, text="ALT Search")

# Create labels and input boxes for item input
label_item = ttk.Label(tab2, text="Item:")
label_item.grid(row=0, column=0, padx=5, sticky="w")

search_entry_item = ttk.Entry(tab2)
search_entry_item.grid(row=0, column=1, padx=5, sticky="w")

# Create a result text box to display query results
result_text_alt = tk.Text(tab2, wrap=tk.WORD, width=100, height=20)
result_text_alt.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Create a function to perform the alternate search
def perform_alt_search():
    # Get the item entered by the user in the text box and remove leading and trailing spaces
    item_pattern = f"%{search_entry_item.get().strip()}%"
    
    # Clear the result text box
    result_text_alt.delete(1.0, tk.END)
    
    # Connect to the database
    conn = sqlite3.connect(os.path.join(script_dir, 'inventory.db'))
    cursor = conn.cursor()

    # Execute SQL query
    cursor.execute("""
        SELECT item, manufacturer_item, manufacturer, item_description
        FROM component_item
        WHERE item LIKE ?
        ORDER BY manufacturer_item ASC
    """, (item_pattern,))

    # Get results
    rows = cursor.fetchall()

    # Display results in the result text box
    for row in rows:
        result_text_alt.insert(tk.END, f"Item: {row[0]}\n")
        result_text_alt.insert(tk.END, f"Manufacturer Item: {row[1]}\n")
        result_text_alt.insert(tk.END, f"Manufacturer: {row[2]}\n")
        result_text_alt.insert(tk.END, f"Item Description: {row[3]}\n\n")

    # Close the database connection
    conn.close()

# Create a button to execute the alternate search
search_button_alt = ttk.Button(tab2, text="Search", command=perform_alt_search)
search_button_alt.grid(row=0, column=2, padx=5, sticky="w")

# Adjust the width of the "ALT Search" tab in the tab switch event
def adjust_tab2_width(event):
    tab2['width'] = tab1.winfo_width()

# Bind the event to the tab switch event
notebook.bind("<<NotebookTabChanged>>", adjust_tab2_width)

# Third Tab - About
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="About")

# Create a Text widget to display the user manual
about_text = tk.Text(tab3, wrap=tk.WORD, width=50, height=10)
about_text.pack(padx=20, pady=20)

# Read the contents of the text file and insert them into the about_text widget
with open("C:\\Davidlocal\\PMD_BOMsearch\\Component_search_user_manual.txt", "r") as file:
    manual_contents = file.read()

about_text.insert(tk.END, manual_contents)

# Disable text widget editing
about_text.config(state=tk.DISABLED)

# Start the main loop of the window
root.mainloop()
