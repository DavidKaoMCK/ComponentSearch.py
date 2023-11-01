import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

def on_drop(event):
    # 獲取拖放的文件路徑
    files = event.data
    print(f'Files dropped: {files}')
    # 在此處處理文件...

# 創建主窗口
root = TkinterDnD.Tk()

# 創建一個文本框，用於接收拖放的文件
text = tk.Text(root, wrap=tk.WORD, width=40, height=10)
text.pack(padx=20, pady=20)

# 配置拖放
text.drop_target_register(DND_FILES)
text.dnd_bind('<<Drop>>', on_drop)

# 運行主循環
root.mainloop()
