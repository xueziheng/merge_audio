#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test SRT subtitle merging functionality
"""

import sys
import os
from srt_parser import SRTParser

def create_test_srt1(filename):
    """Create test SRT file 1 (English)"""
    content = """1
00:00:00,000 --> 00:00:03,440
Hello, welcome to this video.

2
00:00:04,000 --> 00:00:07,500
Let's learn subtitle merging.

3
00:00:08,000 --> 00:00:10,640
This is the last line.
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def create_test_srt2(filename):
    """Create test SRT file 2 (French)"""
    content = """1
00:00:00,000 --> 00:00:03,440
Bonjour, bienvenue dans cette video.

2
00:00:04,000 --> 00:00:07,500
Apprenons la fusion des sous-titres.

3
00:00:08,000 --> 00:00:10,640
C'est la derniere ligne.
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def test_merge_functionality():
    """Test SRT merging functionality"""
    
    print("=" * 60)
    print("Testing SRT Merge Functionality")
    print("=" * 60)
    
    # Create test files
    print("\n[1] Creating test SRT files...")
    try:
        create_test_srt1("test_en.srt")
        create_test_srt2("test_fr.srt")
        print("[PASS] Test SRT files created")
    except Exception as e:
        print("[FAIL] Failed to create test files: " + str(e))
        return False
    
    # Test merging
    print("\n[2] Testing SRT merge...")
    try:
        output_file = "test_merged.srt"
        SRTParser.merge_srt_files("test_en.srt", "test_fr.srt", output_file)
        print("[PASS] Successfully merged SRT files")
    except Exception as e:
        print("[FAIL] Failed to merge: " + str(e))
        return False
    
    # Verify merged file
    print("\n[3] Verifying merged file...")
    try:
        merged_data = SRTParser.parse_srt_file(output_file)
        
        if len(merged_data) != 3:
            print("[FAIL] Expected 3 lines, got {}".format(len(merged_data)))
            return False
        
        print("[PASS] Merged file has correct line count (3 lines)")
        
        # Check content structure
        for i, item in enumerate(merged_data, 1):
            text_lines = item['original_text'].split('\n')
            if len(text_lines) != 2:
                print("[FAIL] Line {} should have 2 text lines, got {}".format(
                    i, len(text_lines)))
                return False
        
        print("[PASS] All lines have correct bilingual structure")
        
    except Exception as e:
        print("[FAIL] Verification failed: " + str(e))
        return False
    
    # Display merged content
    print("\n[4] Merged content preview:")
    try:
        for item in merged_data[:2]:
            print("\nLine {}:".format(item['index']))
            print("  Time: {} --> {}".format(item['start_time'], item['end_time']))
            for line in item['original_text'].split('\n'):
                print("  {}".format(line))
        print("[PASS] Content display successful")
    except Exception as e:
        print("[FAIL] Content display failed: " + str(e))
        return False
    
    # Cleanup
    print("\n[5] Cleaning up test files...")
    try:
        for f in ["test_en.srt", "test_fr.srt", "test_merged.srt"]:
            if os.path.exists(f):
                os.remove(f)
        print("[PASS] Cleanup complete")
    except Exception as e:
        print("[WARNING] Cleanup failed: " + str(e))
    
    print("\n" + "=" * 60)
    print("[PASS] All tests passed successfully!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_merge_functionality()
    sys.exit(0 if success else 1)
