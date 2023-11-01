import tkinter as tk
from tkinter import ttk
import sqlite3


def perform_search():
    manufacturer_item_pattern = f"%{search_entry.get().strip()}%"
    perform_db_query(manufacturer_item_pattern, result_text1, result_text2)


def perform_batch_search():
    lines = batch_search_text.get("1.0", tk.END).strip().split("\n")
    for item in results_tree.get_children():
        results_tree.delete(item)
    for index, item in enumerate(lines, 1):
        item = item.strip()
        if item:
            manufacturer_item_pattern = f"%{item}%"
            component_pmd_pn, product_name = perform_db_query(manufacturer_item_pattern)
            results_tree.insert("", tk.END, values=(item, component_pmd_pn, product_name))


def perform_db_query(manufacturer_item_pattern):
    conn = sqlite3.connect('C:\\Davidlocal\\PMD_BOMsearch\\inventory.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_component.product_name, product_component.component_pmd_pn, component_item.manufacturer_item
        FROM product_component
        JOIN component_item ON product_component.component_pmd_pn = component_item.item
        WHERE component_item.manufacturer_item LIKE ?
        ORDER BY product_component.product_name ASC
    """, (manufacturer_item_pattern,))

    rows = cursor.fetchall()

    component_pmd_pn_set = set()
    product_name_set = set()

    for row in rows:
        component_pmd_pn_set.add(row[1])
        product_name_set.add(row[0])

    conn.close()
    return ", ".join(component_pmd_pn_set), ", ".join(product_name_set)


def copy_to_clipboard(event):
    selected_item = results_tree.selection()
    if selected_item:
        cell_value = results_tree.item(selected_item, "values")[results_tree.identify_column(event.x)[1] - 1]
        root.clipboard_clear()
        root.clipboard_append(cell_value)
        root.update()


root = tk.Tk()
root.title("Component Search")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Single search tab
single_search_tab = ttk.Frame(notebook)
notebook.add(single_search_tab, text="Single Search")

label = ttk.Label(single_search_tab, text="MFR P/N:")
label.pack(pady=10)

search_entry = ttk.Entry(single_search_tab)
search_entry.pack(pady=10)

# Load image
image_path = 'C:\\Davidlocal\\PMD_BOMsearch\\Convert\\Magellan-MC58000-144-pmdcorp.png'
search_image = tk.PhotoImage(file=image_path)

# Create search button and use image
search_button = ttk.Button(single_search_tab, image=search_image, command=perform_search)
search_button.pack(pady=10)

# Create the first results text box
label1 = ttk.Label(single_search_tab, text="Component PMD PN:")
label1.pack()
result_text1 = tk.Text(single_search_tab, wrap=tk.WORD, width=40, height=10)
result_text1.pack(padx=20, pady=5, side=tk.LEFT)


# Create the second results text box
label2 = ttk.Label(single_search_tab, text="Product Name:")
label2.pack()
result_text2 = tk.Text(single_search_tab, wrap=tk.WORD, width=40, height=10)
result_text2.pack(padx=20, pady=5, side=tk.RIGHT)

# Batch search tab
batch_search_tab = ttk.Frame(notebook)
notebook.add(batch_search_tab, text="Batch Search")

batch_search_text = tk.Text(batch_search_tab, wrap=tk.WORD, width=40, height=10)
batch_search_text.pack(pady=10)

batch_search_button = ttk.Button(batch_search_tab, text="Batch Search", command=perform_batch_search)
batch_search_button.pack(pady=10)

# Results tree
columns = ("Search Item", "Component PMD P/N", "Product Names")
results_tree = ttk.Treeview(batch_search_tab, columns=columns, show="headings")
for col in columns:
    results_tree.heading(col, text=col)
    results_tree.column(col, width=120)

results_tree.pack(expand=True, fill="both", padx=20, pady=10)

# Bind Control + C event to copy_to_clipboard function
results_tree.bind('<Control-c>', copy_to_clipboard)

# Start the window's main loop
root.mainloop()
