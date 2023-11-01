import os
import sys
import tkinter as tk
from tkinter import ttk
import sqlite3

def perform_search():
    # 获取用户在文本框中输入的零件名称并删除前导和尾随空格
    manufacturer_item_pattern = f"%{search_entry.get().strip()}%"
    
    # 连接到数据库
    conn = sqlite3.connect(os.path.join(script_dir, 'inventory.db'))
    cursor = conn.cursor()

    # 执行SQL查询
    cursor.execute("""
        SELECT product_component.product_name, product_component.component_pmd_pn, product_component.designator, component_item.manufacturer_item
        FROM product_component
        JOIN component_item ON product_component.component_pmd_pn = component_item.item
        WHERE component_item.manufacturer_item LIKE ?
        ORDER BY product_component.product_name ASC
    """, (manufacturer_item_pattern,))

    # 获取结果
    rows = cursor.fetchall()

    # 使用集合来跟踪已经添加的结果，防止重复
    unique_results = set()

    # 清空结果文本框
    result_text1.delete(1.0, tk.END)
    result_text2.delete(1.0, tk.END)

    # 将结果显示在结果文本框中，并过滤重复项
    for row in rows:
        result = f"{row[0]} - {row[2]}"
        if result not in unique_results:
            result_text1.insert(tk.END, f"{row[1]}\n")
            result_text2.insert(tk.END, f"{result}\n")
            unique_results.add(result)

    # 关闭数据库连接
    conn.close()

# 获取脚本的运行目录
script_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# 创建主窗口
root = tk.Tk()
root.title("Component Search")

# Create a Notebook widget to manage tabs
notebook = ttk.Notebook(root)
notebook.pack()

# First Tab - MFR Search
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="MFR Search")

# 创建标签并放置在搜索框前
label = ttk.Label(tab1, text="MFR P/N:")
label.grid(row=0, column=0, padx=5, sticky="w")

# 创建搜索文本框
search_entry = ttk.Entry(tab1)
search_entry.grid(row=0, column=1, padx=5, sticky="w")

# 加载图片
image_path = os.path.join(script_dir, 'Convert', 'Magellan-MC58000-144-pmdcorp.png')
search_image = tk.PhotoImage(file=image_path)

# 创建搜索按钮并使用图片
search_button = ttk.Button(tab1, image=search_image, command=perform_search)
search_button.grid(row=0, column=2, padx=5, sticky="w", rowspan=2)

# 创建第一个结果文本框
label1 = ttk.Label(tab1, text="Component PMD P/N:")
label1.grid(row=1, column=0, padx=5, sticky="w")
result_text1 = tk.Text(tab1, wrap=tk.WORD, width=25, height=3)
result_text1.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# 创建第二个结果文本框
label2 = ttk.Label(tab1, text="ProductName and Designator:", anchor="center")
label2.grid(row=3, column=0, columnspan=3, padx=5, sticky="nsew")
result_text2 = tk.Text(tab1, wrap=tk.WORD, width=50, height=10)
result_text2.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# Second Tab - ALT Search
tab2 = ttk.Frame(notebook, width=tab1.winfo_width())
notebook.add(tab2, text="ALT Search")

# 创建标签和输入框用于输入item
label_item = ttk.Label(tab2, text="Item:")
label_item.grid(row=0, column=0, padx=5, sticky="w")

search_entry_item = ttk.Entry(tab2)
search_entry_item.grid(row=0, column=1, padx=5, sticky="w")

# 创建结果文本框用于显示查询结果
result_text_alt = tk.Text(tab2, wrap=tk.WORD, width=100, height=20)
result_text_alt.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# 创建执行查询的函数
def perform_alt_search():
    # 获取用户在文本框中输入的item并删除前导和尾随空格
    item_pattern = f"%{search_entry_item.get().strip()}%"
    
    # 清空结果文本框
    result_text_alt.delete(1.0, tk.END)
    
    # 连接到数据库
    conn = sqlite3.connect(os.path.join(script_dir, 'inventory.db'))
    cursor = conn.cursor()

    # 执行SQL查询
    cursor.execute("""
        SELECT item, manufacturer_item, manufacturer, item_description
        FROM component_item
        WHERE item LIKE ?
        ORDER BY manufacturer_item ASC
    """, (item_pattern,))

    # 获取结果
    rows = cursor.fetchall()

    # 将结果显示在结果文本框中
    for row in rows:
        result_text_alt.insert(tk.END, f"Item: {row[0]}\n")
        result_text_alt.insert(tk.END, f"Manufacturer Item: {row[1]}\n")
        result_text_alt.insert(tk.END, f"Manufacturer: {row[2]}\n")
        result_text_alt.insert(tk.END, f"Item Description: {row[3]}\n\n")

    # 关闭数据库连接
    conn.close()

# 创建执行查询的按钮
search_button_alt = ttk.Button(tab2, text="Search", command=perform_alt_search)
search_button_alt.grid(row=0, column=2, padx=5, sticky="w")

# 在标签页切换事件中调整 "ALT Search" 标签页的宽度
def adjust_tab2_width(event):
    tab2['width'] = tab1.winfo_width()

# 将事件绑定到标签页切换事件
notebook.bind("<<NotebookTabChanged>>", adjust_tab2_width)


# Third Tab - About
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="About")

# Create a Text widget to display the user manual
about_text = tk.Text(tab3, wrap=tk.WORD, width=50, height=10)
about_text.pack(padx=20, pady=20)

# Read the contents of the text file and insert them into the about_text widget
with open(os.path.join(script_dir, 'Component_search_user_manual.txt'), "r") as file:
    manual_contents = file.read()

about_text.insert(tk.END, manual_contents)

# Disable text widget editing
about_text.config(state=tk.DISABLED)

# 启动窗口的主循环
root.mainloop()
