import sqlite3
import csv

# Connect to SQLite database
conn = sqlite3.connect('C:\\Davidlocal\\PMD_BOMsearch\\inventory.db')
cursor = conn.cursor()

# Reading and inserting data from the first CSV file
with open('C:\\Davidlocal\\PMD_BOMsearch\\Convert\\CSV_PMD total BOM.csv', 'r', encoding='utf-8-sig') as file:
    dr = csv.DictReader(file)
    
    to_db = [(i['product_name'], i['component_pmd_pn'], i['qty'], i['designator']) for i in dr]
    cursor.executemany("INSERT INTO product_component (product_name, component_pmd_pn, qty, designator) VALUES (?, ?, ?, ?);", to_db)

# Reading and inserting data from the second CSV file
with open('C:\\Davidlocal\\PMD_BOMsearch\\Convert\\CSV_ToExcel_ItemManufacturers.csv', 'r', encoding='utf-8-sig') as file:
    dr = csv.DictReader(file)
    
    to_db = [(i['item'], i['manufacturer'], i['manufacturer_item'], i['item_description']) for i in dr]
    cursor.executemany("INSERT INTO component_item (item, manufacturer, manufacturer_item, item_description) VALUES (?, ?, ?, ?);", to_db)

# Commit changes
conn.commit()

# Close connection
conn.close()
