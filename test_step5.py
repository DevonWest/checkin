#!/usr/bin/env python3
"""
Test script for the Commission → Policy Link Executor

This script tests the functionality without making actual API calls.
"""

import json
import os
import sys
from unittest.mock import Mock, patch
from step5_commission_policy_link import CommissionPolicyLinker, extract_step4_data, parse_step4_data


def test_extract_step4_data():
    """Test the step4 data extraction function."""
    print("Testing extract_step4_data...")
    
    # Test with string input
    assert extract_step4_data("test_string") == "test_string"
    
    # Test with object having 'v' attribute
    mock_obj = Mock()
    mock_obj.v = "test_value"
    assert extract_step4_data(mock_obj) == "test_value"
    
    # Test with dict having 'v' key
    dict_input = {"v": "dict_value"}
    assert extract_step4_data(dict_input) == "dict_value"
    
    # Test with None
    assert extract_step4_data(None) is None
    
    print("✓ extract_step4_data tests passed")


def test_parse_step4_data():
    """Test the step4 data parsing function."""
    print("Testing parse_step4_data...")
    
    # Test JSON parsing
    json_data = '{"ready_to_link": [1, 2, 3], "planned_links": []}'
    result = parse_step4_data(json_data)
    assert result == {"ready_to_link": [1, 2, 3], "planned_links": []}
    
    # Test Python dict string parsing
    dict_str = "{'ready_to_link': [1, 2, 3], 'planned_links': []}"
    result = parse_step4_data(dict_str)
    assert result == {"ready_to_link": [1, 2, 3], "planned_links": []}
    
    print("✓ parse_step4_data tests passed")


def test_commission_policy_linker():
    """Test the CommissionPolicyLinker class."""
    print("Testing CommissionPolicyLinker...")
    
    # Create a linker instance
    linker = CommissionPolicyLinker(
        api_key="test_key",
        business_id="test_business",
        user_id="test_user"
    )
    
    # Test headers generation
    headers = linker._headers()
    expected_headers = {
        "X-API-KEY": "test_key",
        "X-BUSINESS-ID": "test_business", 
        "X-USER-ID": "test_user",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    assert headers == expected_headers
    
    # Test plan validation
    valid_plan = {
        "commission_object_id": "obj123",
        "link_field_id_on_commission": "field456",
        "policy_object_id": "policy789"
    }
    errors = linker._validate_plan(valid_plan, "commission123")
    assert errors == []
    
    # Test invalid plan
    invalid_plan = {"commission_object_id": "obj123"}
    errors = linker._validate_plan(invalid_plan, "commission123")
    assert len(errors) == 2  # Missing 2 required fields
    
    print("✓ CommissionPolicyLinker tests passed")


def create_sample_step4_data():
    """Create sample step4 data for testing."""
    return {
        "ready_to_link": ["comm_001", "comm_002", "comm_003"],
        "planned_links": [
            {
                "commission_id": "comm_001",
                "commission_object_id": "obj_commission",
                "link_field_id_on_commission": "field_policy_link",
                "policy_object_id": "policy_001"
            },
            {
                "commission_id": "comm_002", 
                "commission_object_id": "obj_commission",
                "link_field_id_on_commission": "field_policy_link",
                "policy_object_id": "policy_002"
            },
            {
                "commission_id": "comm_003",
                "commission_object_id": "obj_commission",
                "link_field_id_on_commission": "field_policy_link",
                "policy_object_id": "policy_003"
            }
        ]
    }


@patch('requests.put')
def test_process_step4_data_success(mock_put):
    """Test successful processing of step4 data."""
    print("Testing process_step4_data with successful API calls...")
    
    # Mock successful API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_put.return_value = mock_response
    
    linker = CommissionPolicyLinker(
        api_key="test_key",
        business_id="test_business",
        user_id="test_user"
    )
    
    step4_data = create_sample_step4_data()
    result = linker.process_step4_data(step4_data)
    
    # Verify results
    assert result["ok"] is True
    assert result["attempted"] == 3
    assert result["linked"] == 3
    assert len(result["linked_commission_ids"]) == 3
    assert len(result["errors"]) == 0
    
    print("✓ process_step4_data success test passed")


@patch('requests.put')
def test_process_step4_data_with_errors(mock_put):
    """Test processing of step4 data with API errors."""
    print("Testing process_step4_data with API errors...")
    
    # Mock failed API response
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_put.return_value = mock_response
    
    linker = CommissionPolicyLinker(
        api_key="test_key",
        business_id="test_business", 
        user_id="test_user"
    )
    
    step4_data = create_sample_step4_data()
    result = linker.process_step4_data(step4_data)
    
    # Verify results
    assert result["ok"] is False
    assert result["attempted"] == 3
    assert result["linked"] == 0
    assert len(result["errors"]) == 3
    
    print("✓ process_step4_data error test passed")


def test_main_function_dry_run():
    """Test the main function in dry run mode."""
    print("Testing main function (dry run)...")
    
    # Set environment variables for testing
    os.environ["STEP4_RESULT_JSON"] = json.dumps(create_sample_step4_data())
    os.environ["KIZEN_API_KEY"] = "test_key"
    os.environ["X_BUSINESS_ID"] = "test_business"
    os.environ["X_USER_ID"] = "test_user"
    
    # Mock requests to avoid actual API calls
    with patch('requests.put') as mock_put:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response
        
        # Import and run main (this will use our mocked environment)
        from step5_commission_policy_link import main
        main()
    
    print("✓ main function dry run test passed")


def main():
    """Run all tests."""
    print("Running tests for Commission → Policy Link Executor...\n")
    
    try:
        test_extract_step4_data()
        test_parse_step4_data() 
        test_commission_policy_linker()
        test_process_step4_data_success()
        test_process_step4_data_with_errors()
        test_main_function_dry_run()
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()