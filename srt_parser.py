import re
import chardet
from typing import List, Dict

class SRTParser:
    """SRT文件解析器，严格保持时间轴不变"""

    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """检测文件编码"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'

    @staticmethod
    def parse_srt_file(file_path: str) -> List[Dict]:
        """
        解析SRT文件，返回包含index, start_time, end_time, original_text的列表
        严格保持时间轴不变
        """
        encoding = SRTParser.detect_encoding(file_path)

        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            # 如果检测失败，尝试常见编码
            for enc in ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin1']:
                try:
                    with open(file_path, 'r', encoding=enc) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError(f"无法解码文件 {file_path}")

        # 确保文件使用UTF-8格式
        content = content.encode('utf-8', errors='ignore').decode('utf-8')

        # SRT正则表达式模式
        pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)'

        matches = re.findall(pattern, content, re.DOTALL)

        srt_data = []
        for match in matches:
            index = int(match[0])
            start_time = match[1]
            end_time = match[2]
            original_text = match[3].strip()

            srt_data.append({
                'index': index,
                'start_time': start_time,
                'end_time': end_time,
                'original_text': original_text,
                'translated_text': ''  # 初始为空，后续填充
            })

        return srt_data

    @staticmethod
    def save_srt_file(srt_data: List[Dict], output_path: str):
        """保存翻译后的SRT文件，保持原有时间轴"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in srt_data:
                f.write(f"{item['index']}\n")
                f.write(f"{item['start_time']} --> {item['end_time']}\n")
                f.write(f"{item['translated_text']}\n\n")

    @staticmethod
    def batch_text(srt_data: List[Dict], batch_size: int = 15) -> List[List[Dict]]:
        """将SRT数据分批处理，每批包含指定数量的条目"""
        batches = []
        for i in range(0, len(srt_data), batch_size):
            batch = srt_data[i:i + batch_size]
            batches.append(batch)
        return batches

    @staticmethod
    def merge_srt_files(srt_file1: str, srt_file2: str, output_path: str) -> bool:
        """
        合并两个SRT文件，将两个字幕的文本内容合到一起（一行一条）
        
        输入：
            srt_file1：第一个SRT文件路径
            srt_file2：第二个SRT文件路径
            output_path：输出合并后的SRT文件路径
            
        输出格式：
            1
            00:00:00,000 --> 00:00:03,440
            English subtitle
            French subtitle
            
        返回：成功返回 True，失败返回 False
        """
        try:
            # 解析两个文件
            srt_data1 = SRTParser.parse_srt_file(srt_file1)
            srt_data2 = SRTParser.parse_srt_file(srt_file2)
            
            # 检查行数是否相同
            if len(srt_data1) != len(srt_data2):
                raise ValueError(f"两个SRT文件的字幕行数不相等: {len(srt_data1)} vs {len(srt_data2)}")
            
            # 检查时间轴是否相同
            for i, (item1, item2) in enumerate(zip(srt_data1, srt_data2)):
                if item1['start_time'] != item2['start_time'] or item1['end_time'] != item2['end_time']:
                    raise ValueError(f"第 {i+1} 行的时间轴不相等")
            
            # 合并数据：使用第一个文件的时间轴，合并两个文件的文本
            merged_data = []
            for i, (item1, item2) in enumerate(zip(srt_data1, srt_data2)):
                # 确定文本内容：使用 translated_text 如果有，否则用 original_text
                text1 = item1.get('translated_text') or item1['original_text']
                text2 = item2.get('translated_text') or item2['original_text']
                
                merged_item = {
                    'index': item1['index'],
                    'start_time': item1['start_time'],
                    'end_time': item1['end_time'],
                    'original_text': f"{text1}\n{text2}",  # 两行合一
                    'translated_text': f"{text1}\n{text2}"
                }
                merged_data.append(merged_item)
            
            # 保存合并后的文件
            with open(output_path, 'w', encoding='utf-8') as f:
                for item in merged_data:
                    f.write(f"{item['index']}\n")
                    f.write(f"{item['start_time']} --> {item['end_time']}\n")
                    f.write(f"{item['original_text']}\n\n")
            
            return True
            
        except Exception as e:
            raise Exception(f"字幕合并失败: {str(e)}")

        return batches