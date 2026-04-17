#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 创建示例SRT文件和测试翻译功能
"""

import os
from srt_parser import SRTParser

def create_sample_srt():
    """创建示例SRT文件"""
    sample_content = """1
00:00:01,000 --> 00:00:04,000
Hello, welcome to this video tutorial.

2
00:00:05,000 --> 00:00:08,000
Today we will learn how to use this translation tool.

3
00:00:09,000 --> 00:00:12,000
First, you need to select your SRT file.

4
00:00:13,000 --> 00:00:16,000
Then configure your API settings.

5
00:00:17,000 --> 00:00:20,000
Finally, click the translate button to start.

6
00:00:21,000 --> 00:00:24,000
The tool will process your file batch by batch.

7
00:00:25,000 --> 00:00:28,000
You can see the progress in real time.

8
00:00:29,000 --> 00:00:32,000
The translated file will be saved automatically.

9
00:00:33,000 --> 00:00:36,000
Thank you for watching this tutorial.

10
00:00:37,000 --> 00:00:40,000
Please subscribe for more content.

11
00:00:41,000 --> 00:00:44,000
This tool supports multiple languages including French.

12
00:00:45,000 --> 00:00:48,000
Vous pouvez traduire en français facilement.
"""

    with open("sample.srt", "w", encoding="utf-8") as f:
        f.write(sample_content)

    print("示例SRT文件已创建: sample.srt")

def test_parser():
    """测试SRT解析器"""
    if not os.path.exists("sample.srt"):
        print("请先创建示例文件")
        return

    try:
        print("测试SRT解析器...")
        srt_data = SRTParser.parse_srt_file("sample.srt")

        print(f"解析成功，共 {len(srt_data)} 行")
        for i, item in enumerate(srt_data[:3]):
            print(f"第{i+1}行:")
            print(f"  索引: {item['index']}")
            print(f"  时间: {item['start_time']} --> {item['end_time']}")
            print(f"  原文: {item['original_text']}")

        # 测试批处理
        batches = SRTParser.batch_text(srt_data, batch_size=3)
        print(f"\n批处理测试: 共 {len(batches)} 批")
        for i, batch in enumerate(batches):
            print(f"第{i+1}批: {len(batch)} 行")

        print("解析器测试通过!")

    except Exception as e:
        print(f"解析器测试失败: {e}")

if __name__ == "__main__":
    print("=== SRT翻译工具测试 ===\n")

    # 创建示例文件
    create_sample_srt()
    print()

    # 测试解析器
    test_parser()
    print()

    print("=== 运行主程序 ===")
    print("执行 'python main.py' 启动GUI界面")