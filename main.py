#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SRT字幕翻译工具
主程序入口文件

功能特点：
- 严格保持时间轴不变
- 批处理翻译提高效率
- 支持多种LLM API
- 完整的错误处理和重试机制
- 实时进度显示
- 多线程处理避免UI阻塞
"""

import tkinter as tk
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import SRTTranslatorGUI

def main():
    """主程序入口"""
    try:
        # 创建主窗口
        root = tk.Tk()

        # 设置窗口图标（如果有的话）
        try:
            # 可以在这里设置应用图标
            # root.iconbitmap("icon.ico")
            pass
        except:
            pass

        # 创建应用实例
        app = SRTTranslatorGUI(root)

        # 设置窗口最小尺寸
        root.minsize(800, 800)

        # 居中显示窗口
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')

        # 启动主循环
        root.mainloop()

    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()