#在這兩張表中，第一張的'component_pmd_pn'是作為與第二張表中的'item'交互引所相關的關鍵。
#現在我想要查詢，第二張表中的 manufacturer_item 'OPA2348AIDCN' 是對應第二張表中的哪個item，並且使用第二張表中的item去對應到第一張表中的'product_name'，告訴我OPA2348AIDCN是用在那些product裡面。 且有時候查詢的零件名稱會有一點點不一樣，我可以使用模糊搜尋嗎，例如OPA2348AIDCN 有時候會以 POPA2348AIDCN, OPA2348AIDCNT, POPA2348AIDCNR, OPA2348AIDCNRT的樣子出現。 我希望查詢的結果依照 product name以升序的方式呈現


import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('C:\\Davidlocal\\PMD_BOMsearch\\inventory.db')
cursor = conn.cursor()

# Define the manufacturer_item pattern to search for
manufacturer_item_pattern = '%OPA2348AIDCN%'

# Execute the SQL query
cursor.execute("""
    SELECT product_component.product_name, component_item.manufacturer_item
    FROM product_component
    JOIN component_item ON product_component.component_pmd_pn = component_item.item
    WHERE component_item.manufacturer_item LIKE ?
    ORDER BY product_component.product_name ASC
""", (manufacturer_item_pattern,))

# Fetch the results
rows = cursor.fetchall()

# Print the results
print(f"Manufacturer Items matching pattern '{manufacturer_item_pattern}' are used in the following products (sorted by product name):")
for row in rows:
    print(f"Product Name: {row[0]}, Manufacturer Item: {row[1]}")

# Close connection
conn.close()
