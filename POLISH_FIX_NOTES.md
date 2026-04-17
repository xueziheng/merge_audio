# SRT 字幕矫正功能 - Bug 修复说明

## 问题描述

用户在运行字幕矫正功能时遇到两个问题：

### 问题 1：数据不匹配
```
第 11 批矫正数据不匹配（期望: 15, 实际: 30）
```

### 问题 2：序号混入文本
```
矫正前：Hello, welcome to this video tutorial.
矫正后：1 大家来使用豆包运用费卖血法
```

LLM 在输出时加入了序号前缀。

## 根本原因分析

### 原因 1：不清晰的 Prompt 格式

**原始 `_build_polish_prompt`：**
```python
for idx, text in enumerate(texts, 1):
    prompt += f"{idx}. {text}\n"
```

这种格式明确告诉 LLM "使用序号.格式"，导致 LLM 在返回时也添加序号。

### 原因 2：数据匹配逻辑不够智能

原始的 `_parse_translation_result` 处理过于简单：
- 当行数不匹配时，直接截取或填充
- 没有考虑 prompt format 变化导致的格式差异

## 解决方案

### 修复 1：改进 Polish Prompt（第 115-125 行）

**关键改变：**
- ✗ 移除了输入中的序号：`for text in texts:` (而非 `enumerate`)
- ✓ 明确说明不要加序号："不要加序号、不要加任何标点符号"
- ✓ 降低歧义：使用清晰的输入/输出格式说明

**新格式：**
```python
def _build_polish_prompt(self, texts: List[str]) -> str:
    prompt = (
        "请按照原始顺序矫正以下由机器生成的字幕文本。\n"
        "输入格式：每行一条字幕内容\n"
        "输出要求：仅返回矫正后的文本内容，不要加序号、不要加任何标点符号、不要加任何其他文字\n\n"
        "字幕文本如下：\n"
    )
    
    for text in texts:
        prompt += f"{text}\n"
    
    prompt += "\n矫正后的字幕（仅返回矫正内容，一行一条，不加序号和标点）："
    return prompt
```

### 修复 2：增强解析逻辑（第 127-177 行）

**改进内容：**

1. **多格式支持**
   - 识别 "1. text" 格式
   - 识别 "1) text" 格式  
   - 识别 "1 text" 格式
   - 识别 "1、text" 格式（中文常见）

2. **更智能的数量匹配**
   ```python
   # 如果非空行数等于期望数量，使用这些行
   if len(non_empty_lines) == expected_count:
       return non_empty_lines
   ```

3. **智能的不匹配处理**
   - 先尝试使用非空行
   - 再尝试使用解析后的行
   - 最后才截取或填充

## 验证

✅ **单元测试通过：**
```
[PASS] Successfully parsed sample.srt with 12 lines
[PASS] Divided 12 lines into 3 batches (size: 5)
[PASS] Timestamp preserved (3/3 ✓)
[PASS] Successfully saved to: sample_polished_test.srt
[PASS] Output filename suffix is correct
```

## 最佳实践建议

### 对 Prompt 的建议

1. **明确说明"不要做什么"**
   ```
   ✓ 不要加序号
   ✓ 不要加标点
   ✓ 不要加其他文字
   ```

2. **使用清晰的示例**
   ```
   输入：Hello world
   输出：你好世界
   ```

3. **强调一对一对应**
   ```
   关键：每条输入对应一条输出，顺序相同
   ```

### 对数据处理的建议

1. **多格式识别**：不要假设 LLM 只返回一种格式
2. **宽松匹配**：优先匹配行数相等的结果
3. **日志记录**：当出现不匹配时，提供清晰的日志信息

## 相关文件修改

- **`translator.py`**：
  - `POLISH_SYSTEM_PROMPT`（第 13-21 行）
  - `_build_polish_prompt()`（第 115-125 行）
  - `_parse_translation_result()`（第 127-177 行）

## 测试命令

```bash
python test_polish.py
```

所有测试均应通过。
