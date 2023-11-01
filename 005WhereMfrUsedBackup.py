import tkinter as tk
from tkinter import ttk
import sqlite3


def perform_search():
    # 获取用户在文本框中输入的零件名称并删除前导和尾随空格
    manufacturer_item_pattern = f"%{search_entry.get().strip()}%"
    
    # 连接到数据库
    conn = sqlite3.connect('C:\\Davidlocal\\PMD_BOMsearch\\inventory.db')
    cursor = conn.cursor()

    # 执行SQL查询
    cursor.execute("""
        SELECT product_component.product_name, product_component.component_pmd_pn, component_item.manufacturer_item
        FROM product_component
        JOIN component_item ON product_component.component_pmd_pn = component_item.item
        WHERE component_item.manufacturer_item LIKE ?
        ORDER BY product_component.product_name ASC
    """, (manufacturer_item_pattern,))

    # 获取结果
    rows = cursor.fetchall()

    # 清空结果文本框
    result_text1.delete(1.0, tk.END)
    result_text2.delete(1.0, tk.END)

    # 使用集合收集component_pmd_pn和product_name
    component_pmd_pn_set = set()
    product_name_set = set()

    # 将结果显示在结果文本框中
    for row in rows:
        component_pmd_pn_set.add(row[1])
        product_name_set.add(row[0])

    # 插入文本框中
    for component_pmd_pn in component_pmd_pn_set:
        result_text1.insert(tk.END, f"{component_pmd_pn}\n")
    for product_name in product_name_set:
        result_text2.insert(tk.END, f"{product_name}\n")

    # 关闭数据库连接
    conn.close()


# 创建主窗口
root = tk.Tk()
root.title("Component Search")

# 创建标签并放置在搜索框前
label = ttk.Label(root, text="MFR P/N:")
label.grid(row=0, column=0, padx=5, sticky="w")

# 创建搜索文本框
search_entry = ttk.Entry(root)
search_entry.grid(row=0, column=1, padx=5, sticky="w")

# 加载图片
image_path = 'C:\\Davidlocal\\PMD_BOMsearch\\Convert\\Magellan-MC58000-144-pmdcorp.png'
search_image = tk.PhotoImage(file=image_path)

# 创建搜索按钮并使用图片
search_button = ttk.Button(root, image=search_image, command=perform_search)
search_button.grid(row=0, column=2, padx=5, sticky="w", rowspan=2)

# 创建第一个结果文本框
label1 = ttk.Label(root, text="Component PMD P/N:")
label1.grid(row=1, column=0, padx=5, sticky="w")
result_text1 = tk.Text(root, wrap=tk.WORD, width=25, height=3)
result_text1.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# 创建第二个结果文本框
label2 = ttk.Label(root, text="Product Name:", anchor="center")
label2.grid(row=3, column=0, columnspan=3, padx=5, sticky="nsew")
result_text2 = tk.Text(root, wrap=tk.WORD, width=50, height=10)
result_text2.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# 启动窗口的主循环
root.mainloop()
