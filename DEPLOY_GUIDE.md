# SRT 字幕工具 - 部署和使用指南

## 🚀 快速开始（推荐）

### 在 Windows 上最简单的方式

1. **双击 `run.bat` 文件**
   - 自动检查 Python 环境
   - 自动安装依赖包
   - 直接启动 GUI 应用

2. **等待程序启动**
   - 第一次运行会安装依赖（可能需要 1-2 分钟）
   - 之后再运行就会立即启动

3. **开始使用**
   - 在 GUI 中选择字幕文件
   - 选择操作：翻译、矫正或合并
   - 查看结果

---

## 📋 系统要求

### 必要条件
- **操作系统**：Windows 7+ 或 Linux/Mac
- **Python**：3.7+ 版本
- **网络**：需要访问 DeepSeek API 或 OpenAI API

### 检查 Python 安装
```bash
# 打开命令行，输入以下命令
python --version  # 应该显示 Python 3.7+

# 或者
python -V
```

### 如果没有装 Python
去 https://www.python.org/downloads/ 下载安装 Python 3.9+

---

## 📦 部署步骤

### 方法 1：使用 run.bat（推荐 Windows 用户）

```
1. 下载整个项目文件夹到本地
2. 在文件夹中找到 run.bat 文件
3. 双击 run.bat 运行
4. 程序会自动：
   ✓ 检查 Python
   ✓ 安装依赖
   ✓ 启动 GUI
```

### 方法 2：手动安装（Linux/Mac）

```bash
# 1. 进入项目目录
cd /path/to/merge_audio

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动程序
python main.py
```

### 方法 3：使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动程序
python main.py
```

---

## 🔑 API 配置

### 必需的 API Key

应用需要 LLM API 来进行翻译和矫正。支持两种：

#### 选项 1：DeepSeek API（推荐，更便宜）
1. 访问 https://platform.deepseek.com
2. 注册账号
3. 生成 API Key
4. 在 GUI 中：
   - 点击"DeepSeek API"按钮
   - 或手动输入：
     - API Key：你的 Deep seek key
     - API URL：https://api.deepseek.com/chat/completions
     - Model：deepseek-chat

#### 选项 2：OpenAI API
1. 访问 https://platform.openai.com
2. 注册账号
3. 生成 API Key
4. 在 GUI 中：
   - 点击"OpenAI API"按钮
   - 或手动输入：
     - API Key：你的 OpenAI key
     - API URL：https://api.openai.com/v1/chat/completions
     - Model：gpt-3.5-turbo 或 gpt-4

---

## 📖 使用指南

### 功能 1：字幕翻译

**目的**：将字幕从一种语言翻译成另一种语言

**步骤**：
1. 点击"浏览"选择 SRT 字幕文件
2. 选择源语言（通常是英文 English）
3. 选择目标语言（比如 Chinese）
4. 点击"开始翻译"
5. 等待完成，输出文件为 `原文件_translated.srt`

---

### 功能 2：字幕矫正

**目的**：修正 Whisper 生成的字幕错误

**步骤**：
1. 点击"浏览"选择要矫正的 SRT 文件
2. 点击"字幕矫正"按钮
3. 日志中会显示每一行的修改对比：
   ```
   [第 5 行] 已修改:
     原文: 原始内容
     矫正: 修正后的内容
   ```
4. 完成后保存为 `原文件_polished.srt`

**矫正规则**：
- ✓ 去除多余标点符号
- ✓ 纠正同音异义字（如"在/再"）
- ✓ 修正听写错误
- ✓ 保留专业术语
- ✓ 保留完整时间轴

---

### 功能 3：字幕合并

**目的**：将两个语言的字幕合并为双语字幕

**使用场景**：
- 英文字幕 + 法文字幕 → 英法双语字幕

**步骤**：
1. 在"字幕合并"面板中：
   - 第一个 SRT：选择第一个语言的字幕（如英文）
   - 第二个 SRT：选择第二个语言的字幕（如法文）
   - 输出文件：设置合并后文件的保存位置

2. 点击"合并字幕"按钮

3. 查看预览（前 3 行）

4. 输出格式：
   ```
   1
   00:00:00,000 --> 00:00:03,440
   English subtitle line
   French subtitle line
   ```

**重要**：
- ⚠️ 两个文件的行数必须相等
- ⚠️ 时间轴必须完全一致
- ⚠️ 系统会自动验证，不匹配会报错

---

## 🐛 常见问题和解决方案

### 问题 1：双击 run.bat 没有反应

**原因**：可能 Python 没有安装或不在 PATH 中

**解决**：
```bash
# 1. 打开 PowerShell 或 CMD，输入：
python --version

# 2. 如果显示已安装，说明路径没有问题
# 3. 如果显示 "不是内部命令"，需要重新安装 Python
#    - 下载 Python 安装程序
#    - 安装时勾选 "Add Python to PATH"
#    - 重启电脑
```

### 问题 2：依赖安装失败

**原因**：网络问题或 pip 镜像不可用

**解决**：
```bash
# 使用 Aliyun 镜像（中国用户）
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 或使用清华镜像
pip install -r requirements.txt -i https://pypi.tsinghua.edu.cn/simple
```

### 问题 3：API Key 不工作

**排查步骤**：
1. 确认 API Key 正确复制（没有多余空格）
2. 确认 API Key 没有过期
3. 确认网络连接正常
4. 确认 API URL 正确
5. 检查账户余额（如果使用付费 API）

### 问题 4：字幕合并显示"时间轴不相等"

**原因**：两个文件的时间戳不同

**解决**：
- 确保两个文件对应同一段视频
- 两个文件的字幕单元数必须相等
- 时间戳精确到毫秒必须完全相同

---

## 📊 批量处理建议

### 处理大量字幕
1. **翻译**：默认批大小 15 行，可在 GUI 中调整
2. **矫正**：同样支持批处理，会显示进度
3. **合并**：一次只能合并两个文件

### 优化性能
- 增加 Batch Size（更快但更消耗 API 额度）
- 减少 Batch Size（更稳定但更慢）
- 建议值：10-20 行

---

## 🔍 日志和调试

### 在状态框中查看日志

所有操作都会在 GUI 的"状态"框中显示详细日志：

```
正在解析SRT文件: /path/to/file.srt
解析完成，共 100 行字幕
正在初始化矫正引擎...
正在矫正第 1/7 批，共 15 行

============================================================
矫正结果详情
============================================================

[第 5 行] 已修改:
  原文: 原始文本
  矫正: 修正后文本

共修改 5/100 行字幕
```

### 查看错误日志

如果发生错误，错误信息会显示在状态框中，通常会告诉你：
- 哪一行出错
- 错误类型
- 解决建议

---

## 📂 文件结构说明

```
merge_audio/
├── main.py                 # 应用入口
├── gui.py                  # GUI 界面（包含矫正、合并功能）
├── translator.py           # 翻译/矫正引擎
├── srt_parser.py          # SRT 文件解析和合并
├── run.bat                # Windows 一键启动
├── requirements.txt       # 依赖列表
├── sample.srt             # 示例字幕文件
├── test_polish.py         # 矫正功能测试
├── test_merge.py          # 合并功能测试
├── CLAUDE.md              # 项目文档
├── DEPLOY_GUIDE.md        # 本文件 - 部署指南
└── POLISH_FIX_NOTES.md    # Bug 修复说明
```

---

## 🎯 工作流程示例

### 完整的字幕处理流程

```
原始 Whisper 字幕（中文）
    ↓
1. [矫正] 使用"字幕矫正"功能修正错误
    ↓
2. [翻译] 出现 sample_polished.srt，用它翻译成英文
    ↓
3. [翻译] 再翻译成法文
    ↓
4. [合并] 使用"字幕合并"功能
    - 第一个：英文翻译后的字幕
    - 第二个：法文翻译后的字幕
    ↓
最终输出：英法双语字幕
```

---

## ✅ 验证安装成功

### 测试命令

```bash
# 测试矫正功能
python test_polish.py

# 测试合并功能
python test_merge.py

# 检查依赖
pip list | grep -E "requests|chardet"
```

### 预期输出

```
[PASS] All tests passed successfully!
```

---

## 💡 最佳实践

### 1. API 费用控制
- 使用 DeepSeek 更便宜（约 $0.10 per 1M tokens）
- 调整 Batch Size 找到速度和成本的平衡
- 矫正功能比翻译消耗的 token 更少

### 2. 字幕质量
- 先用"矫正"修正原始字幕
- 再用"翻译"翻译到其他语言
- 这样输出质量最高

### 3. 合并建议
- 字幕来源必须相同（同一个视频）
- 时间轴必须完全一致
- 建议先验证两个文件再合并

---

## 🆘 获取帮助

### 常见错误代码

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `API请求错误` | 网络问题或 API 不可用 | 检查网络和 API Key |
| `API响应解析错误` | API 返回格式异常 | 检查 Model 是否支持 |
| `字幕合并失败：行数不相等` | 两个文件行数不同 | 确保来源于同一视频 |
| `字幕合并失败：时间轴不相等` | 时间戳不匹配 | 检查文件的时间戳 |

---

## 📞 技术支持

如果遇到问题：

1. **查看日志** - 状态框中的错误信息通常会指出问题
2. **检查配置** - 确认 API Key 和 URL 正确
3. **重新安装依赖** - `pip install -r requirements.txt --upgrade`
4. **清空缓存** - 删除 `*.pyc` 文件后重新运行

---

**祝你使用愉快！** 🎉
