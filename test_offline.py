#!/usr/bin/env python3
"""
Test script to verify the text analysis pipeline works in offline mode
"""

import pandas as pd
import os
from SRC.Data_ingestion import data_ingestion
from SRC.utils import Col_Structure

def test_offline_mode():
    """Test the pipeline in offline mode with sample data"""
    
    print("Testing Text Analysis Pipeline in Offline Mode")
    print("=" * 50)
    
    # Test data ingestion class initialization
    try:
        obj = data_ingestion()
        print("✓ Data ingestion class initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize data ingestion: {e}")
        return False
    
    # Test primary data loading
    try:
        input_data = obj.primary()
        if input_data is not None:
            print(f"✓ Primary data loaded successfully: {len(input_data)} rows")
        else:
            print("✗ Failed to load primary data")
            return False
    except Exception as e:
        print(f"✗ Error loading primary data: {e}")
        return False
    
    # Test utils class initialization
    try:
        str_obj = Col_Structure()
        print("✓ Column structure class initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize column structure: {e}")
        return False
    
    # Test with sample text for analysis
    try:
        sample_data = pd.DataFrame({
            'URL_ID': ['test001'],
            'URL': ['https://example.com/test'],
            'article_words': ['This is a test article about technology and innovation. It contains positive words like excellent and amazing, and also some negative words like bad and terrible.']
        })
        
        result = str_obj.Col_Structure_Primary(sample_data)
        print("✓ Text analysis completed successfully")
        print(f"  Sample analysis result shape: {result.shape if result is not None else 'None'}")
        
    except Exception as e:
        print(f"✗ Error in text analysis: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All offline tests passed! Pipeline is ready for main branch.")
    return True

if __name__ == "__main__":
    test_offline_mode()