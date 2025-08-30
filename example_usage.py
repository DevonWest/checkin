#!/usr/bin/env python3
"""
Example usage of the Commission → Policy Link Executor

This script demonstrates how to use the commission-policy linker
with sample data.
"""

import json
from step5_commission_policy_link import CommissionPolicyLinker


def create_example_data():
    """Create example step 4 data."""
    return {
        "ready_to_link": ["COMM_2024_001", "COMM_2024_002", "COMM_2024_003"],
        "planned_links": [
            {
                "commission_id": "COMM_2024_001",
                "commission_object_id": "commission_object",
                "link_field_id_on_commission": "policy_reference_field",
                "policy_object_id": "POLICY_2024_001"
            },
            {
                "commission_id": "COMM_2024_002",
                "commission_object_id": "commission_object",
                "link_field_id_on_commission": "policy_reference_field", 
                "policy_object_id": "POLICY_2024_002"
            },
            {
                "commission_id": "COMM_2024_003",
                "commission_object_id": "commission_object",
                "link_field_id_on_commission": "policy_reference_field",
                "policy_object_id": "POLICY_2024_003"
            }
        ]
    }


def example_usage():
    """Demonstrate usage of the CommissionPolicyLinker."""
    print("=== Commission Policy Linker Example ===\n")
    
    # Example API credentials (replace with real ones)
    api_credentials = {
        "api_key": "your_kizen_api_key_here",
        "business_id": "your_business_id_here", 
        "user_id": "your_user_id_here"
    }
    
    # Create the linker
    linker = CommissionPolicyLinker(**api_credentials)
    
    # Create example data
    step4_data = create_example_data()
    
    print("Example Step 4 Data:")
    print(json.dumps(step4_data, indent=2))
    print()
    
    # NOTE: This would make actual API calls if you have real credentials
    # For demonstration, we'll just show what would happen
    print("This would process the following links:")
    for link in step4_data["planned_links"]:
        print(f"  • Commission {link['commission_id']} → Policy {link['policy_object_id']}")
    
    print()
    print("To run with real API calls:")
    print("1. Replace the API credentials above with real values")
    print("2. Ensure you have network access to app.go.kizen.com")
    print("3. Uncomment the process_step4_data call below")
    print()
    
    # Uncomment this line to make actual API calls:
    # result = linker.process_step4_data(step4_data)
    # print("Result:")
    # print(json.dumps(result, indent=2))


def workflow_simulation():
    """Simulate how this would work in a workflow environment."""
    print("=== Workflow Environment Simulation ===\n")
    
    # Simulate workflow inputs/outputs/secrets
    class MockInputs:
        step4ResultJson = json.dumps(create_example_data())
    
    class MockOutputs:
        step5_result_json = None
    
    class MockSecrets:
        def __getitem__(self, key):
            mock_secrets = {
                "kizen_api_key": "mock_api_key",
                "x_business_id": "mock_business_id",
                "x_user_id": "mock_user_id"
            }
            return mock_secrets[key]
    
    # Monkey patch the globals
    import step5_commission_policy_link
    step5_commission_policy_link.inputs = MockInputs()
    step5_commission_policy_link.outputs = MockOutputs()
    step5_commission_policy_link.secrets = MockSecrets()
    
    print("Simulated workflow environment set up.")
    print("In a real workflow, the main() function would:")
    print("1. Read from inputs.step4ResultJson")
    print("2. Get API credentials from secrets")
    print("3. Process the commission-policy links")
    print("4. Write results to outputs.step5_result_json")
    print()
    print("Input data would be:")
    print(step5_commission_policy_link.inputs.step4ResultJson)


if __name__ == "__main__":
    example_usage()
    print("\n" + "="*50 + "\n")
    workflow_simulation()