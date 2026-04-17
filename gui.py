import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, Spinbox
import threading
import os
from typing import Optional
from srt_parser import SRTParser
from translator import TranslationEngine, SRTTranslator

class SRTTranslatorGUI:
    """SRT翻译工具GUI界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("SRT字幕翻译工具")
        self.root.geometry("800x600")

        # 变量
        self.srt_file_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.api_key = tk.StringVar(value="sk-713da8e5186c4e83a63318c3ebc23423")
        self.api_url = tk.StringVar(value="https://api.deepseek.com/chat/completions")
        self.model = tk.StringVar(value="deepseek-chat")
        self.source_lang = tk.StringVar(value="Auto Detect")
        self.target_lang = tk.StringVar(value="Chinese")
        self.batch_size = tk.IntVar(value=15)

        # 翻译相关变量
        self.translator_thread: Optional[threading.Thread] = None
        self.is_translating = False
        self.current_srt_data = None

        self.create_widgets()

    def create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 1. 输入文件选择
        ttk.Label(main_frame, text="SRT文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.srt_file_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="浏览", command=self.select_srt_file).grid(row=0, column=2, padx=5)

        # 2. API设置框架
        api_frame = ttk.LabelFrame(main_frame, text="API设置", padding="10")
        api_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        api_frame.columnconfigure(1, weight=1)

        # API Key
        ttk.Label(api_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(api_frame, textvariable=self.api_key, show="*", width=60).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        # API URL
        ttk.Label(api_frame, text="API URL:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(api_frame, textvariable=self.api_url, width=60).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)

        # Model
        ttk.Label(api_frame, text="Model:").grid(row=2, column=0, sticky=tk.W, pady=2)
        model_combo = ttk.Combobox(api_frame, textvariable=self.model, width=57)
        model_combo['values'] = ('deepseek-chat', 'deepseek-coder', 'gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo', 'claude-3-sonnet', 'claude-3-opus')
        model_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)

        # API Quick Select Buttons
        button_frame = ttk.Frame(api_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(button_frame, text="DeepSeek API", command=lambda: self.set_api_config("deepseek")).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="OpenAI API", command=lambda: self.set_api_config("openai")).pack(side=tk.LEFT, padx=2)

        # 3. 翻译设置框架
        trans_frame = ttk.LabelFrame(main_frame, text="翻译设置", padding="10")
        trans_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        trans_frame.columnconfigure(1, weight=1)

        # 源语言
        ttk.Label(trans_frame, text="Source Language:").grid(row=0, column=0, sticky=tk.W, pady=2)
        source_combo = ttk.Combobox(trans_frame, textvariable=self.source_lang, width=15)
        source_combo['values'] = ('Auto Detect', 'English', 'Chinese', 'Japanese', 'Korean', 'French')
        source_combo.grid(row=0, column=1, sticky=tk.W, padx=5)

        # 目标语言
        ttk.Label(trans_frame, text="Target Language:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=(20, 0))
        target_combo = ttk.Combobox(trans_frame, textvariable=self.target_lang, width=15)
        target_combo['values'] = ('Chinese', 'English', 'French', 'Japanese', 'Korean')
        target_combo.grid(row=0, column=3, sticky=tk.W, padx=5)

        # 批处理大小
        ttk.Label(trans_frame, text="Batch Size:").grid(row=0, column=4, sticky=tk.W, pady=2, padx=(20, 0))
        Spinbox(trans_frame, from_=5, to=50, textvariable=self.batch_size, width=10).grid(row=0, column=5, sticky=tk.W, padx=5)

        # 4. 输出设置
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        output_frame.columnconfigure(1, weight=1)

        ttk.Label(output_frame, text="输出文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(output_frame, text="浏览", command=self.select_output_file).grid(row=0, column=2, padx=5)

        # 4.5. 字幕合并框架
        merge_frame = ttk.LabelFrame(main_frame, text="字幕合并", padding="10")
        merge_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        merge_frame.columnconfigure(1, weight=1)

        ttk.Label(merge_frame, text="第一个SRT:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.merge_file1 = tk.StringVar()
        ttk.Entry(merge_frame, textvariable=self.merge_file1, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(merge_frame, text="浏览", command=self.select_merge_file1).grid(row=0, column=2, padx=5)

        ttk.Label(merge_frame, text="第二个SRT:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.merge_file2 = tk.StringVar()
        ttk.Entry(merge_frame, textvariable=self.merge_file2, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(merge_frame, text="浏览", command=self.select_merge_file2).grid(row=1, column=2, padx=5)

        ttk.Label(merge_frame, text="输出文件:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.merge_output = tk.StringVar()
        ttk.Entry(merge_frame, textvariable=self.merge_output, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(merge_frame, text="浏览", command=self.select_merge_output).grid(row=2, column=2, padx=5)

        # 5. 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)

        self.translate_button = ttk.Button(button_frame, text="开始翻译", command=self.start_translation)
        self.translate_button.pack(side=tk.LEFT, padx=5)

        self.polish_button = ttk.Button(button_frame, text="字幕矫正", command=self.start_polish)
        self.polish_button.pack(side=tk.LEFT, padx=5)

        self.merge_button = ttk.Button(button_frame, text="合并字幕", command=self.start_merge)
        self.merge_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="停止处理", command=self.stop_translation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="预览原文", command=self.preview_original).pack(side=tk.LEFT, padx=5)

        # 6. 状态框架
        status_frame = ttk.LabelFrame(main_frame, text="状态", padding="10")
        status_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        # 文本日志框
        self.log_text = scrolledtext.ScrolledText(status_frame, height=10, wrap=tk.WORD)
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def select_srt_file(self):
        """选择SRT文件"""
        file_path = filedialog.askopenfilename(
            title="选择SRT文件",
            filetypes=[("SRT文件", "*.srt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.srt_file_path.set(file_path)
            # 自动设置输出文件名
            base_name = os.path.splitext(file_path)[0]
            self.output_path.set(f"{base_name}_translated.srt")

    def select_output_file(self):
        """选择输出文件"""
        file_path = filedialog.asksaveasfilename(
            title="保存翻译结果",
            defaultextension=".srt",
            filetypes=[("SRT文件", "*.srt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.output_path.set(file_path)

    def log_message(self, message: str):
        """在日志框中显示消息"""
        def update_log():
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.see(tk.END)
            self.root.update_idletasks()

        if threading.current_thread() == threading.main_thread():
            update_log()
        else:
            self.root.after(0, update_log)

    def update_progress(self, current: int, total: int):
        """更新进度条"""
        def update():
            if total > 0:
                progress = (current / total) * 100
                self.progress_var.set(progress)
            self.root.update_idletasks()

        if threading.current_thread() == threading.main_thread():
            update()
        else:
            self.root.after(0, update)

    def validate_inputs(self) -> bool:
        """验证输入参数"""
        if not self.srt_file_path.get():
            messagebox.showerror("错误", "请选择SRT文件")
            return False

        if not os.path.exists(self.srt_file_path.get()):
            messagebox.showerror("错误", "SRT文件不存在")
            return False

        if not self.output_path.get():
            messagebox.showerror("错误", "请设置输出文件路径")
            return False

        if not self.api_key.get():
            messagebox.showerror("错误", "请输入API Key")
            return False

        if not self.api_url.get():
            messagebox.showerror("错误", "请输入API URL")
            return False

        return True

    def start_translation(self):
        """开始翻译"""
        if not self.validate_inputs():
            return

        if self.is_translating:
            messagebox.showwarning("警告", "翻译正在进行中")
            return

        # 禁用按钮
        self.translate_button.config(state=tk.DISABLED)
        self.polish_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # 清空日志
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set(0)

        # 启动翻译线程
        self.translator_thread = threading.Thread(target=self.translate_worker)
        self.translator_thread.daemon = True
        self.translator_thread.start()

    def stop_translation(self):
        """停止翻译或矫正"""
        self.is_translating = False
        self.log_message("正在停止处理...")

        # 启用按钮
        self.translate_button.config(state=tk.NORMAL)
        self.polish_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def translate_worker(self):
        """翻译工作线程"""
        try:
            self.is_translating = True
            self.log_message("开始翻译...")

            # 1. 解析SRT文件
            self.log_message(f"正在解析SRT文件: {self.srt_file_path.get()}")
            try:
                srt_data = SRTParser.parse_srt_file(self.srt_file_path.get())
                self.current_srt_data = srt_data
                self.log_message(f"解析完成，共 {len(srt_data)} 行字幕")
            except Exception as e:
                self.log_message(f"SRT文件解析失败: {str(e)}")
                return

            if not self.is_translating:
                return

            # 2. 初始化翻译引擎
            self.log_message("正在初始化翻译引擎...")
            try:
                translation_engine = TranslationEngine(
                    api_key=self.api_key.get(),
                    api_url=self.api_url.get(),
                    model=self.model.get()
                )
            except Exception as e:
                self.log_message(f"翻译引擎初始化失败: {str(e)}")
                return

            if not self.is_translating:
                return

            # 3. 创建翻译器并设置回调
            translator = SRTTranslator(translation_engine, batch_size=self.batch_size.get())
            translator.set_progress_callback(self.log_message)

            # 4. 开始翻译
            self.log_message("开始翻译处理...")
            try:
                # 转换语言名称为代码
                source_lang_code = self._convert_language_to_code(self.source_lang.get())
                target_lang_code = self._convert_language_to_code(self.target_lang.get())

                translated_data = translator.translate_srt(
                    srt_data,
                    source_lang=source_lang_code,
                    target_lang=target_lang_code
                )

                if not self.is_translating:
                    return

                # 5. 保存结果
                self.log_message(f"正在保存到: {self.output_path.get()}")
                SRTParser.save_srt_file(translated_data, self.output_path.get())
                self.log_message("翻译完成！")

                # 更新进度条到100%
                self.update_progress(100, 100)

            except Exception as e:
                import traceback
                error_msg = f"翻译过程中发生错误: {str(e)}\n堆栈跟踪:\n{traceback.format_exc()}"
                self.log_message(error_msg)

        except Exception as e:
            self.log_message(f"发生未知错误: {str(e)}")

        finally:
            # 恢复按钮状态
            self.is_translating = False
            self.translate_button.config(state=tk.NORMAL)
            self.polish_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def start_polish(self):
        """开始字幕矫正"""
        if not self.validate_inputs():
            return

        if self.is_translating:
            messagebox.showwarning("警告", "处理正在进行中")
            return

        # 禁用按钮
        self.translate_button.config(state=tk.DISABLED)
        self.polish_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # 清空日志
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set(0)

        # 启动矫正线程
        self.translator_thread = threading.Thread(target=self.polish_worker)
        self.translator_thread.daemon = True
        self.translator_thread.start()

    def polish_worker(self):
        """矫正工作线程"""
        try:
            self.is_translating = True
            self.log_message("开始字幕矫正...")

            # 1. 解析SRT文件
            self.log_message(f"正在解析SRT文件: {self.srt_file_path.get()}")
            try:
                srt_data = SRTParser.parse_srt_file(self.srt_file_path.get())
                self.current_srt_data = srt_data
                self.log_message(f"解析完成，共 {len(srt_data)} 行字幕")
            except Exception as e:
                self.log_message(f"SRT文件解析失败: {str(e)}")
                return

            if not self.is_translating:
                return

            # 2. 初始化翻译引擎
            self.log_message("正在初始化矫正引擎...")
            try:
                translation_engine = TranslationEngine(
                    api_key=self.api_key.get(),
                    api_url=self.api_url.get(),
                    model=self.model.get()
                )
            except Exception as e:
                self.log_message(f"矫正引擎初始化失败: {str(e)}")
                return

            if not self.is_translating:
                return

            # 3. 创建翻译器并设置回调
            translator = SRTTranslator(translation_engine, batch_size=self.batch_size.get())
            translator.set_progress_callback(self.log_message)

            # 4. 开始矫正
            self.log_message("开始矫正处理...")
            try:
                polished_data = translator.translate_srt(
                    srt_data,
                    source_lang="auto",
                    target_lang="auto",
                    task_mode="polish"
                )

                if not self.is_translating:
                    return

                # 4.5. 显示矫正详情
                self.log_message("\n" + "="*60)
                self.log_message("矫正结果详情")
                self.log_message("="*60)
                
                modified_count = 0
                for i, (original, polished) in enumerate(zip(srt_data, polished_data), 1):
                    original_text = original['original_text']
                    polished_text = polished.get('translated_text', original_text)
                    
                    # 检查是否被修改
                    if original_text != polished_text:
                        modified_count += 1
                        self.log_message(f"\n[第 {i} 行] 已修改:")
                        self.log_message(f"  原文: {original_text}")
                        self.log_message(f"  矫正: {polished_text}")
                
                self.log_message("\n" + "="*60)
                self.log_message(f"共修改 {modified_count}/{len(srt_data)} 行字幕")
                self.log_message("="*60 + "\n")



                # 5. 生成输出文件名（添加 _polished 后缀）
                base_path = os.path.splitext(self.srt_file_path.get())[0]
                polished_output_path = f"{base_path}_polished.srt"

                # 6. 保存结果
                self.log_message(f"正在保存到: {polished_output_path}")
                SRTParser.save_srt_file(polished_data, polished_output_path)
                self.log_message("矫正完成！")

                # 更新进度条到100%
                self.update_progress(100, 100)

            except Exception as e:
                import traceback
                error_msg = f"矫正过程中发生错误: {str(e)}\n堆栈跟踪:\n{traceback.format_exc()}"
                self.log_message(error_msg)

        except Exception as e:
            self.log_message(f"发生未知错误: {str(e)}")

        finally:
            # 恢复按钮状态
            self.is_translating = False
            self.translate_button.config(state=tk.NORMAL)
            self.polish_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def set_api_config(self, api_type: str):
        """快速设置API配置"""
        if api_type == "deepseek":
            self.api_url.set("https://api.deepseek.com/chat/completions")
            self.model.set("deepseek-chat")
        elif api_type == "openai":
            self.api_url.set("https://api.openai.com/v1/chat/completions")
            self.model.set("gpt-3.5-turbo")

    def _convert_language_to_code(self, language_name: str) -> str:
        """将语言名称转换为语言代码"""
        language_map = {
            'Auto Detect': 'auto',
            'English': 'en',
            'Chinese': 'zh',
            'French': 'fr',
            'Japanese': 'ja',
            'Korean': 'ko'
        }
        return language_map.get(language_name, language_name.lower())

    def preview_original(self):
        """预览原文内容"""
        if not self.srt_file_path.get() or not os.path.exists(self.srt_file_path.get()):
            messagebox.showwarning("警告", "请先选择有效的SRT文件")
            return

        try:
            srt_data = SRTParser.parse_srt_file(self.srt_file_path.get())

            # 创建预览窗口
            preview_window = tk.Toplevel(self.root)
            preview_window.title("原文预览")
            preview_window.geometry("600x400")

            text_widget = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # 显示前20行内容
            preview_text = ""
            for i, item in enumerate(srt_data[:20]):
                preview_text += f"{item['index']}\n"
                preview_text += f"{item['start_time']} --> {item['end_time']}\n"
                preview_text += f"{item['original_text']}\n\n"

            if len(srt_data) > 20:
                preview_text += f"... (共 {len(srt_data)} 行，仅显示前20行)"

            text_widget.insert(tk.END, preview_text)
            text_widget.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("错误", f"预览失败: {str(e)}")


    def select_merge_file1(self):
        """选择第一个SRT文件"""
        file_path = filedialog.askopenfilename(
            title="选择第一个SRT文件",
            filetypes=[("SRT文件", "*.srt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.merge_file1.set(file_path)

    def select_merge_file2(self):
        """选择第二个SRT文件"""
        file_path = filedialog.askopenfilename(
            title="选择第二个SRT文件",
            filetypes=[("SRT文件", "*.srt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.merge_file2.set(file_path)

    def select_merge_output(self):
        """选择合并后的输出文件"""
        file_path = filedialog.asksaveasfilename(
            title="保存合并后的字幕文件",
            defaultextension=".srt",
            filetypes=[("SRT文件", "*.srt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.merge_output.set(file_path)

    def start_merge(self):
        """开始合并字幕"""
        # 验证输入
        if not self.merge_file1.get():
            messagebox.showerror("错误", "请选择第一个SRT文件")
            return
        
        if not self.merge_file2.get():
            messagebox.showerror("错误", "请选择第二个SRT文件")
            return
        
        if not self.merge_output.get():
            messagebox.showerror("错误", "请设置输出文件路径")
            return
        
        if not os.path.exists(self.merge_file1.get()):
            messagebox.showerror("错误", "第一个SRT文件不存在")
            return
        
        if not os.path.exists(self.merge_file2.get()):
            messagebox.showerror("错误", "第二个SRT文件不存在")
            return
        
        if self.is_translating:
            messagebox.showwarning("警告", "处理正在进行中")
            return
        
        # 禁用按钮
        self.translate_button.config(state=tk.DISABLED)
        self.polish_button.config(state=tk.DISABLED)
        self.merge_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        
        # 启动合并线程
        self.translator_thread = threading.Thread(target=self.merge_worker)
        self.translator_thread.daemon = True
        self.translator_thread.start()

    def merge_worker(self):
        """合并字幕的工作线程"""
        try:
            self.is_translating = True
            self.log_message("开始合并字幕...")
            
            file1 = self.merge_file1.get()
            file2 = self.merge_file2.get()
            output_path = self.merge_output.get()
            
            self.log_message(f"正在加载第一个文件: {file1}")
            self.log_message(f"正在加载第二个文件: {file2}")
            
            # 进行合并
            SRTParser.merge_srt_files(file1, file2, output_path)
            
            # 验证合并结果
            merged_data = SRTParser.parse_srt_file(output_path)
            self.log_message(f"\n合并成功: 共 {len(merged_data)} 行字幕")
            
            # 显示合并结果示例（前3行）
            self.log_message("\n合并结果示例（前3行）:")
            for i, item in enumerate(merged_data[:3], 1):
                self.log_message(f"\n第 {item['index']} 行:")
                self.log_message(f"  {item['start_time']} --> {item['end_time']}")
                # 显示合并后的文本（含换行）
                for line in item['original_text'].split('\n'):
                    self.log_message(f"  {line}")
            
            self.log_message(f"\n合并完成! 保存到: {output_path}")
            self.update_progress(100, 100)
            
        except Exception as e:
            self.log_message(f"合并失败: {str(e)}")
        
        finally:
            # 恢复按钮状态
            self.is_translating = False
            self.translate_button.config(state=tk.NORMAL)
            self.polish_button.config(state=tk.NORMAL)
            self.merge_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
