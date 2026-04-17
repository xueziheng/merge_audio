import requests
import json
import time
from typing import List, Dict, Optional
import logging

TRANSLATE_SYSTEM_PROMPT = (
    "You are a professional subtitle translation assistant. Please accurately translate the given text "
    "content, maintaining the tone and style of the original text. Return only the translation results "
    "without any additional explanations or formatting."
)

POLISH_SYSTEM_PROMPT = (
    "你是一位专业的字幕矫正师 (Subtitle Polishing Editor)。你的任务是接收一份由机器（如 Whisper）生成的 SRT "
    "字幕原稿，优化其文本，使其符合人类阅读习惯，并修正关键信息错误。\n\n"
    "必须严格遵守：\n"
    "1. 绝对保持时间轴：严禁修改、删除、合并或重新计算任何一行的时间戳（Timestamp）和序号（Index）。你的操作仅限于修改字幕文本内容。\n"
    "2. 单行结构：保持原有的行数结构，不要合并行。\n"
    "3. 纠错重点：重点修正同音异义字（如\"在/再\"、\"做/作\"）、明显的机器听写错误以及专业术语。"
)


class TranslationEngine:
    """翻译引擎，支持多种翻译和矫正操作"""

    def __init__(self, api_key: str, api_url: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.session = requests.Session()

    def translate_batch(
        self,
        texts: List[str],
        source_lang: str = "auto",
        target_lang: str = "zh",
        task_mode: str = "translate"
    ) -> Optional[List[str]]:
        """处理字幕批次的翻译或矫正"""
        if not texts:
            return []

        if task_mode == "polish":
            system_prompt = POLISH_SYSTEM_PROMPT
            user_prompt = self._build_polish_prompt(texts)
        else:
            system_prompt = TRANSLATE_SYSTEM_PROMPT
            user_prompt = self._build_translation_prompt(texts, source_lang, target_lang)

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = self.session.post(
                self._resolve_api_endpoint(),
                json=payload,
                headers=headers,
                timeout=60,
            )
            response.raise_for_status()

            result = response.json()
            translated_text = result['choices'][0]['message']['content'].strip()
            return self._parse_translation_result(translated_text, len(texts))

        except requests.exceptions.RequestException as exc:
            logging.error(f"API请求错误: {exc}")
            return None
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            logging.error(f"API响应解析错误: {exc}")
            return None
        except Exception as exc:
            logging.error(f"处理中发生未知错误: {exc}")
            return None

    def _build_translation_prompt(self, texts: List[str], source_lang: str, target_lang: str) -> str:
        """构建翻译提示词"""
        lang_map = {
            "en": "English",
            "zh": "Chinese",
            "fr": "French",
            "ja": "Japanese",
            "ko": "Korean",
            "auto": "auto-detected language",
        }

        source_name = lang_map.get(source_lang, source_lang)
        target_name = lang_map.get(target_lang, target_lang)

        prompt = (
            f"Please translate the following {source_name} text to {target_name}, maintaining one-to-one correspondence "
            "for each line:\n\n"
        )

        for idx, text in enumerate(texts, 1):
            prompt += f"{idx}. {text}\n"

        prompt += (
            "\nPlease return the translation results in the same order, with each line containing only the translated content:"
        )
        return prompt

    def _build_polish_prompt(self, texts: List[str]) -> str:
        """构建矫正提示词"""
        prompt = (
            "请按照原始顺序矫正以下由机器生成的字幕文本。\n"
            "输入格式：每行一条字幕内容\n"
            "输出要求：仅返回矫正后的文本内容，不要加序号、不要加任何其他文字\n\n"
            "字幕文本如下：\n"
        )

        for text in texts:
            prompt += f"{text}\n"

        prompt += (
            "\n矫正后的字幕（仅返回矫正内容，一行一条，不加序号和标点）："
        )
        return prompt

    def _parse_translation_result(self, result: str, expected_count: int) -> List[str]:
        """解析LLM的返回结果"""
        lines = result.strip().split('\n')
        translations = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 提取序号和文本：检查多种格式 "1. text", "1) text", "1 text" 等
            text = line
            if '. ' in line:
                parts = line.split('. ', 1)
                if parts[0].isdigit():
                    text = parts[1]
            elif ') ' in line:
                parts = line.split(') ', 1)
                if parts[0].isdigit():
                    text = parts[1]
            elif line and line[0].isdigit():
                # 查找数字后的空格或其他分隔符
                for i, char in enumerate(line):
                    if not char.isdigit():
                        if char in ' )、.）':
                            text = line[i:].lstrip(' )、.）')
                        break

            translations.append(text.strip())

        if len(translations) != expected_count:
            # 如果数量不匹配，尝试不删除空行
            direct_lines = [line.strip() for line in lines]
            # 只保留非空行
            non_empty_lines = [l for l in direct_lines if l]
            
            # 如果非空行数量等于期望数量，使用这些行
            if len(non_empty_lines) == expected_count:
                return non_empty_lines
            
            # 如果解析后的翻译数量等于期望数量，返回解析结果
            if len(translations) == expected_count:
                return translations
            
            # 否则，尝试截取或填充到期望数量
            if len(translations) > expected_count:
                return translations[:expected_count]
            else:
                # 填充空字符串
                result_list = translations.copy()
                while len(result_list) < expected_count:
                    result_list.append("")
                return result_list

        return translations[:expected_count]

    def _resolve_api_endpoint(self) -> str:
        """确定正确的 chat completions 端点"""
        normalized = self.api_url.rstrip('/')
        if normalized.endswith('/chat/completions'):
            return normalized
        if normalized.endswith('/v1'):
            return f"{normalized}/chat/completions"
        return f"{normalized}/chat/completions"


class SRTTranslator:
    """SRT翻译/矫正处理器"""

    def __init__(self, translation_engine: TranslationEngine, batch_size: int = 15):
        self.translation_engine = translation_engine
        self.batch_size = batch_size
        self.progress_callback = None

    def set_progress_callback(self, callback):
        self.progress_callback = callback

    def translate_srt(
        self,
        srt_data: List[Dict],
        source_lang: str = "auto",
        target_lang: str = "zh",
        task_mode: str = "translate",
    ) -> List[Dict]:
        from srt_parser import SRTParser

        batches = SRTParser.batch_text(srt_data, self.batch_size)
        total_batches = len(batches)
        translated_data = srt_data.copy()
        action_label = "翻译" if task_mode == "translate" else "矫正"

        for batch_idx, batch in enumerate(batches):
            texts_to_translate = [item['original_text'] for item in batch]

            if self.progress_callback:
                self.progress_callback(
                    f"正在{action_label}第 {batch_idx + 1}/{total_batches} 批，共 {len(texts_to_translate)} 行"
                )

            translations = self.translation_engine.translate_batch(
                texts_to_translate,
                source_lang,
                target_lang,
                task_mode=task_mode,
            )

            logging.debug(f"Batch {batch_idx + 1}: translate_batch returned {type(translations)} = {translations is None}")
            if translations is None:
                if self.progress_callback:
                    self.progress_callback(f"第 {batch_idx + 1} 批{action_label}失败，正在重试...")

                translations = self._retry_batch(
                    texts_to_translate,
                    source_lang,
                    target_lang,
                    batch_idx + 1,
                    task_mode,
                )

                if translations is None:
                    if self.progress_callback:
                        self.progress_callback(f"第 {batch_idx + 1} 批{action_label}失败，使用原文本")
                    # 使用原文本而不是 continue，确保数据完整性
                    translations = [item['original_text'] for item in batch]

            # 检查返回的数据
            if translations is None:
                logging.error(f"Batch {batch_idx + 1}: translations is still None after retry!")
                logging.error(f"Batch {batch_idx + 1}: Using original text for {len(batch)} items")
                translations = [item['original_text'] for item in batch]
            elif not isinstance(translations, list):
                logging.error(f"Batch {batch_idx + 1}: translations is not a list, it's {type(translations)}")
                logging.error(f"Batch {batch_idx + 1}: Using original text for {len(batch)} items")
                translations = [item['original_text'] for item in batch]
            elif len(translations) != len(batch):
                if self.progress_callback:
                    self.progress_callback(
                        f"第 {batch_idx + 1} 批{action_label}数据不匹配（期望: {len(batch)}, 实际: {len(translations)}）"
                    )
                logging.warning(f"Batch {batch_idx + 1}: length mismatch, adjusting from {len(translations)} to {len(batch)}")
                translations = self._adjust_translation_count(translations, len(batch))

            for idx, item in enumerate(batch):
                original_index = item['index'] - 1
                # 确保 translations 不是 None 且是列表
                if translations is None or not isinstance(translations, list):
                    # 不应该发生，但如果发生了，使用原文本
                    translated_data[original_index]['translated_text'] = item['original_text']
                elif idx < len(translations) and translations[idx]:
                    translated_data[original_index]['translated_text'] = translations[idx]
                else:
                    translated_data[original_index]['translated_text'] = item['original_text']

            time.sleep(1)

        return translated_data

    def _retry_batch(
        self,
        texts: List[str],
        source_lang: str,
        target_lang: str,
        batch_num: int,
        task_mode: str,
        max_retries: int = 3,
    ) -> Optional[List[str]]:
        action_label = "翻译" if task_mode == "translate" else "矫正"
        for retry in range(max_retries):
            if self.progress_callback:
                self.progress_callback(f"正在对第 {batch_num} 批{action_label}进行重试 {retry + 1}/{max_retries} 次")

            translations = self.translation_engine.translate_batch(
                texts,
                source_lang,
                target_lang,
                task_mode=task_mode,
            )

            if translations is not None:
                if self.progress_callback:
                    self.progress_callback(f"第 {batch_num} 批{action_label}重试成功")
                return translations

            time.sleep(2)

        return None

    def _adjust_translation_count(self, translations: List[str], expected_count: int) -> List[str]:
        """调整翻译结果的数量以匹配预期值"""
        # 防御性检查
        if translations is None or not isinstance(translations, list):
            logging.error(f"_adjust_translation_count: translations is {type(translations)}, returning empty list")
            return [""] * expected_count
        
        if len(translations) > expected_count:
            return translations[:expected_count]
        if len(translations) < expected_count:
            result = translations.copy()
            while len(result) < expected_count:
                result.append("")
            return result
        return translations
