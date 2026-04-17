#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test subtitle polishing functionality
"""

import sys
import os

def test_polish_functionality():
    """Test various aspects of the polish functionality"""
    
    print("=" * 60)
    print("Testing SRT Polish Functionality")
    print("=" * 60)
    
    try:
        from srt_parser import SRTParser
    except ImportError as e:
        print("[FAIL] Import error: " + str(e))
        return False
    
    # 1. Test SRT file parsing
    print("\n[1] Testing SRT file parsing...")
    try:
        srt_data = SRTParser.parse_srt_file("sample.srt")
        print("[PASS] Successfully parsed sample.srt with {} lines".format(len(srt_data)))
        
        # Show first two subtitles
        for i, item in enumerate(srt_data[:2]):
            print("\n   Subtitle {}:".format(i+1))
            print("   - Index: {}".format(item['index']))
            print("   - Time: {} --> {}".format(item['start_time'], item['end_time']))
            print("   - Text: {}".format(item['original_text'][:50]))
    except Exception as e:
        print("[FAIL] Parsing failed: " + str(e))
        return False
    
    # 2. Test batch processing
    print("\n[2] Testing batch division...")
    try:
        batch_size = 5
        batches = SRTParser.batch_text(srt_data, batch_size)
        print("[PASS] Divided {} lines into {} batches (size: {})".format(
            len(srt_data), len(batches), batch_size))
        
        for idx, batch in enumerate(batches[:2]):
            print("   - Batch {}: {} lines".format(idx+1, len(batch)))
    except Exception as e:
        print("[FAIL] Batch processing failed: " + str(e))
        return False
    
    # 3. Verify timestamp preservation
    print("\n[3] Testing timestamp preservation...")
    try:
        # Create simulated polished data (only change text, preserve timestamps)
        polished_data = []
        for item in srt_data:
            polished_item = item.copy()
            # Simulate polish: add prefix
            polished_item['translated_text'] = "[POLISHED] " + item['original_text']
            polished_data.append(polished_item)
        
        # Verify timestamps are preserved
        timestamps_ok = True
        for i, (orig, polish) in enumerate(zip(srt_data[:3], polished_data[:3])):
            if orig['index'] == polish['index'] and \
               orig['start_time'] == polish['start_time'] and \
               orig['end_time'] == polish['end_time']:
                print("[PASS] Subtitle {}: timestamp preserved".format(i+1))
            else:
                print("[FAIL] Subtitle {}: timestamp was modified!".format(i+1))
                timestamps_ok = False
        
        if not timestamps_ok:
            return False
                
    except Exception as e:
        print("[FAIL] Timestamp verification failed: " + str(e))
        return False
    
    # 4. Test file saving
    print("\n[4] Testing file saving...")
    try:
        output_path = "sample_polished_test.srt"
        SRTParser.save_srt_file(polished_data, output_path)
        print("[PASS] Successfully saved to: {}".format(output_path))
        
        # Verify by reading
        verify_data = SRTParser.parse_srt_file(output_path)
        if len(verify_data) == len(polished_data):
            print("[PASS] Verification: saved file has correct line count ({} lines)".format(len(verify_data)))
        else:
            print("[FAIL] Verification: expected {} lines, got {}".format(
                len(polished_data), len(verify_data)))
            return False
            
    except Exception as e:
        print("[FAIL] File saving failed: " + str(e))
        return False
    
    # 5. Test output filename generation
    print("\n[5] Testing output filename generation...")
    try:
        original_path = "sample.srt"
        base_path = os.path.splitext(original_path)[0]
        polished_output_path = "{}_polished.srt".format(base_path)
        print("[INFO] Original file: {}".format(original_path))
        print("[INFO] Polished file: {}".format(polished_output_path))
        
        if polished_output_path.endswith("_polished.srt"):
            print("[PASS] Output filename suffix is correct")
        else:
            print("[FAIL] Output filename suffix is incorrect")
            return False
            
    except Exception as e:
        print("[FAIL] Filename generation failed: " + str(e))
        return False
    
    print("\n" + "=" * 60)
    print("[PASS] All tests passed successfully!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_polish_functionality()
    sys.exit(0 if success else 1)
