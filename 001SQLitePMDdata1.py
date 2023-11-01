#create a linked database*
import sqlite3
conn = sqlite3.connect('inventory.db')

#create a cursor
c = conn.cursor()

#create 2 major forms
c.execute('''
    CREATE TABLE product_component (
        product_name TEXT,
        component_pmd_pn TEXT,
        qty INTEGER,
        designator TEXT
    )
''')

c.execute('''
    CREATE TABLE component_item (
        item TEXT,
        manufacturer TEXT,
        manufacturer_item TEXT,
        item_description TEXT
    )
''')

#save the 2 tables
conn.commit()

#close the 2 table
conn.close()
