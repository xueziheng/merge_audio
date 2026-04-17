# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an SRT subtitle translation tool that maintains strict timestamp preservation while translating subtitles using various LLM APIs. The application features a Tkinter-based GUI for user-friendly operation.

## Architecture

### Core Components

- **main.py**: Entry point that initializes the Tkinter GUI application
- **gui.py**: Complete GUI implementation with threading for non-blocking translation operations
- **srt_parser.py**: SRT file parsing with intelligent encoding detection and strict timestamp preservation
- **translator.py**: Translation engine supporting multiple LLM APIs (OpenAI, DeepSeek, and compatible services)

### Key Design Patterns

- **Batch Processing**: Translates subtitles in configurable batches (default 15 lines) to optimize API usage
- **Thread Separation**: GUI operations run on main thread, translation runs on background thread to prevent UI blocking
- **Encoding Detection**: Automatic file encoding detection with fallback to common encodings
- **Timestamp Integrity**: Time axis data is strictly preserved throughout the translation process

## Development Commands

### Running the Application
```bash
# Primary method - starts GUI
python main.py

# Alternative - batch file with dependency checking
run.bat
```

### Testing
```bash
# Create sample SRT file and test parser
python test_example.py
```

### Dependency Management
```bash
# Install dependencies
pip install -r requirements.txt
```

## Translation Engine Architecture

The translation system follows this flow:
1. **Parse SRT**: Extract text while preserving timestamps using regex pattern matching
2. **Batch Creation**: Group subtitles into configurable batches for API efficiency
3. **API Communication**: Send only text content to LLM (no timestamp interference)
4. **Result Processing**: Parse translation results and validate line count matching
5. **File Output**: Reconstruct SRT with original timestamps and translated text

## API Configuration

Default configuration uses DeepSeek API:
- URL: https://api.deepseek.com/v1
- Models: deepseek-chat, deepseek-coder

Supports any OpenAI-compatible API by changing URL and model parameters.

## File Structure Notes

- All text processing preserves UTF-8 encoding
- SRT parsing uses regex: `(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)`
- Threading prevents GUI blocking during translation operations
- Error handling includes automatic retry for API failures

## Testing Strategy

- test_example.py creates sample.srt with multilingual content for testing
- Parser testing validates timestamp preservation and batch creation
- No automated test framework - manual testing via GUI and test script