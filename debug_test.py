#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试脚本：测试 translator.py 是否有 NoneType len() 问题
"""

import logging
import traceback
from srt_parser import SRTParser
from translator import TranslationEngine, SRTTranslator

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_polish_with_file(srt_file_path):
    """测试字幕矫正功能"""
    print(f"\n=== 测试字幕矫正 ===")
    print(f"文件: {srt_file_path}")
    
    try:
        # 1. 解析 SRT 文件
        print("\n[1] 解析 SRT 文件...")
        srt_data = SRTParser.parse_srt_file(srt_file_path)
        print(f"    成功解析 {len(srt_data)} 行字幕")
        
        # 2. 初始化翻译引擎（使用演示 API key）
        print("\n[2] 初始化翻译引擎...")
        engine = TranslationEngine(
            api_key="sk-713da8e5186c4e83a63318c3ebc23423",
            api_url="https://api.deepseek.com/chat/completions",
            model="deepseek-chat"
        )
        print("    引擎初始化完成")
        
        # 3. 创建翻译器
        print("\n[3] 创建 SRT 翻译器...")
        translator = SRTTranslator(engine, batch_size=15)
        
        # 设置进度回调
        def progress_cb(msg):
            print(f"    [进度] {msg}")
        translator.set_progress_callback(progress_cb)
        print("    翻译器创建完成")
        
        # 4. 执行矫正
        print("\n[4] 执行字幕矫正...")
        result = translator.translate_srt(
            srt_data,
            source_lang="auto",
            target_lang="auto",
            task_mode="polish"
        )
        print(f"    矫正完成！返回 {len(result)} 行结果")
        
        # 验证结果
        if result is None:
            print("    [ERROR] 结果为 None！")
            return False
        
        if not isinstance(result, list):
            print(f"    [ERROR] 结果不是列表，而是 {type(result)}")
            return False
        
        print("    [SUCCESS] 矫正成功！")
        return True
        
    except Exception as e:
        print(f"\n    [ERROR] 发生异常: {str(e)}")
        print("\n    堆栈跟踪:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 测试文件路径
    test_file = "sample.srt"
    
    # 运行测试
    success = test_polish_with_file(test_file)
    
    # 输出结果
    print(f"\n\n{'='*50}")
    if success:
        print("✓ 测试成功！没有检测到 NoneType len() 错误")
    else:
        print("✗ 测试失败！请检查上面的错误信息")
    print(f"{'='*50}")
