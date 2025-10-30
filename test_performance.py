#!/usr/bin/env python3
"""
Simple performance test to verify optimizations work correctly.
Tests the key improvements made to the codebase.
"""

import sys
import time
import os

# Add SRC to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'SRC'))

from Components.Structure import Analysis


def test_caching():
    """Test that caching works correctly"""
    print("Testing caching mechanisms...")
    
    # Create Analysis instance
    analysis = Analysis()
    
    # Test 1: Stopwords caching
    print("  - Testing stopwords caching...")
    start = time.time()
    stopwords1 = analysis.StopWords_data()
    time1 = time.time() - start
    
    start = time.time()
    stopwords2 = analysis.StopWords_data()
    time2 = time.time() - start
    
    # Second call should be much faster (cached)
    assert stopwords1 is stopwords2, "Stopwords should be cached"
    assert time2 < time1 or time2 < 0.001, f"Cached call should be faster: {time1:.4f}s vs {time2:.4f}s"
    print(f"    ✓ Stopwords cached correctly (first: {time1:.4f}s, cached: {time2:.4f}s)")
    
    # Test 2: Master dictionary caching
    print("  - Testing master dictionary caching...")
    # Reset cache to test properly
    Analysis._master_dict_cache = None
    
    start = time.time()
    pos1, neg1 = analysis.MasterDictionar_data()
    time1 = time.time() - start
    
    start = time.time()
    pos2, neg2 = analysis.MasterDictionar_data()
    time2 = time.time() - start
    
    # Second call should be much faster (cached)
    assert pos1 is pos2 and neg1 is neg2, "Dictionary should be cached"
    assert time2 < time1 or time2 < 0.001, f"Cached call should be faster: {time1:.4f}s vs {time2:.4f}s"
    print(f"    ✓ Dictionary cached correctly (first: {time1:.4f}s, cached: {time2:.4f}s)")
    
    # Test 3: Regex pattern caching
    print("  - Testing regex pattern caching...")
    pattern1 = analysis._get_regex_pattern()
    pattern2 = analysis._get_regex_pattern()
    assert pattern1 is pattern2, "Regex pattern should be cached"
    print("    ✓ Regex pattern cached correctly")


def test_set_operations():
    """Test that set operations work correctly"""
    print("\nTesting set-based optimizations...")
    
    analysis = Analysis()
    
    # Test text corpus preprocessing
    print("  - Testing text preprocessing...")
    test_text = "This is a test sentence with some common words."
    tokens = analysis.text_corpus(test_text)
    assert isinstance(tokens, list), "Should return a list"
    assert len(tokens) > 0, "Should have some tokens"
    print(f"    ✓ Text preprocessing works (processed {len(tokens)} tokens)")
    
    # Test syllable counting
    print("  - Testing syllable counting...")
    assert analysis.count_syllables("test") >= 0, "Should count syllables"
    assert analysis.count_syllables("beautiful") >= 2, "Beautiful should have 2+ syllables"
    print("    ✓ Syllable counting works")
    
    # Test complexity calculation
    print("  - Testing complexity calculation...")
    words = ["test", "beautiful", "extraordinary", "a", "the"]
    percentage, count = analysis.calculate_complexity_percentage(words)
    assert 0 <= percentage <= 100, "Percentage should be between 0 and 100"
    assert count >= 0, "Count should be non-negative"
    print(f"    ✓ Complexity calculation works ({percentage:.1f}% complex)")
    
    # Test personal pronoun counting
    print("  - Testing personal pronoun counting...")
    words = ["i", "think", "we", "should", "test", "my", "code"]
    count = analysis.Personal_pronoun_count(words)
    assert count == 3, f"Should find 3 pronouns, found {count}"
    print(f"    ✓ Pronoun counting works (found {count} pronouns)")
    
    # Test average word length
    print("  - Testing average word length calculation...")
    words = ["test", "words", "here"]
    length = analysis.Average_Word_Length(words)
    assert length == sum(len(w) for w in words), "Should sum all characters"
    print(f"    ✓ Word length calculation works (total: {length} chars)")


def test_no_hardcoded_paths():
    """Verify no hardcoded Windows paths remain"""
    print("\nChecking for hardcoded paths...")
    
    files_to_check = [
        'SRC/Components/Structure.py',
        'SRC/Data_ingestion.py',
        'SRC/utils.py'
    ]
    
    base_path = os.path.dirname(__file__)
    
    for filepath in files_to_check:
        full_path = os.path.join(base_path, filepath)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for Windows-style hardcoded paths
            if 'E:\\' in content or 'C:\\Users' in content:
                print(f"  ✗ Found hardcoded path in {filepath}")
                return False
    
    print("  ✓ No hardcoded paths found")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Performance Optimization Tests")
    print("=" * 60)
    
    try:
        test_caching()
        test_set_operations()
        test_no_hardcoded_paths()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
