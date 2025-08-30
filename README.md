# Commission → Policy Link Executor

This module handles linking commission records to policy records via the Kizen API. It's designed to be Step 5 in a workflow that processes commission and policy data.

## Features

- **Robust Input Handling**: Supports multiple input formats for step 4 data
- **Error Handling**: Comprehensive error handling with detailed error reporting
- **Validation**: Validates all required fields before making API calls
- **Modular Design**: Clean, testable code structure with proper separation of concerns
- **Flexible Deployment**: Works in workflow environments or as a standalone script

## Usage

### In a Workflow Environment

The code expects to find:
- `inputs.step4ResultJson`: The output from step 4 containing commission and policy linking plans
- `secrets`: Object containing API credentials
- `outputs`: Object to write the final result to

```python
# This runs automatically when the module is executed in a workflow context
# Results will be written to outputs.step5_result_json
```

### As a Standalone Script

Set environment variables and run:

```bash
# Set required environment variables
export STEP4_RESULT_JSON='{"ready_to_link": ["comm_001"], "planned_links": [{"commission_id": "comm_001", "commission_object_id": "obj_commission", "link_field_id_on_commission": "field_policy_link", "policy_object_id": "policy_001"}]}'
export KIZEN_API_KEY="your_api_key"
export X_BUSINESS_ID="your_business_id"
export X_USER_ID="your_user_id"

# Run the script
python step5_commission_policy_link.py
```

### As a Library

```python
from step5_commission_policy_link import CommissionPolicyLinker

linker = CommissionPolicyLinker(
    api_key="your_api_key",
    business_id="your_business_id", 
    user_id="your_user_id"
)

step4_data = {
    "ready_to_link": ["comm_001", "comm_002"],
    "planned_links": [
        {
            "commission_id": "comm_001",
            "commission_object_id": "obj_commission",
            "link_field_id_on_commission": "field_policy_link",
            "policy_object_id": "policy_001"
        }
    ]
}

result = linker.process_step4_data(step4_data)
print(result)
```

## Input Format

The step 4 data should contain:

```json
{
  "ready_to_link": ["commission_id_1", "commission_id_2"],
  "planned_links": [
    {
      "commission_id": "commission_id_1",
      "commission_object_id": "kizen_object_id",
      "link_field_id_on_commission": "field_id",
      "policy_object_id": "policy_object_id"
    }
  ]
}
```

## Output Format

Success:
```json
{
  "ok": true,
  "message": "Step 5 attempted 2 links. Success: 2, Errors: 0",
  "timestamp": "2025-08-30T07:45:05.175074",
  "user": "DevonWest",
  "attempted": 2,
  "linked": 2,
  "linked_commission_ids": ["comm_001", "comm_002"],
  "linked_pairs": [
    {
      "commission_id": "comm_001",
      "policy_id": "policy_001",
      "success": true,
      "result": "linked"
    }
  ],
  "errors": [],
  "input_ready_ids": ["comm_001", "comm_002"]
}
```

Error:
```json
{
  "ok": false,
  "message": "Step 5 failed.",
  "timestamp": "2025-08-30T07:45:05.175074",
  "user": "DevonWest",
  "error": "Error description",
  "trace": "Stack trace"
}
```

## API Requirements

The code makes PUT requests to the Kizen API:

- **Endpoint**: `https://app.go.kizen.com/api/records/{object_id}/{record_id}`
- **Headers**: 
  - `X-API-KEY`: Your Kizen API key
  - `X-BUSINESS-ID`: Your business ID
  - `X-USER-ID`: Your user ID
- **Payload**:
  ```json
  {
    "fields": [{
      "id": "field_id",
      "value": {"id": "related_object_id"}
    }]
  }
  ```

## Testing

Run the test suite:

```bash
python test_step5.py
```

The tests include:
- Input parsing and validation
- API call mocking
- Error handling scenarios
- Integration testing

## Error Handling

The code handles several types of errors:
- Missing or invalid input data
- Missing API credentials
- API request failures
- Network timeouts
- Validation errors

All errors are logged and returned in a structured format for debugging.

## Dependencies

- `requests`: For HTTP API calls
- `json`: For JSON parsing
- `ast`: For parsing Python dict strings
- `datetime`: For timestamps
- `traceback`: For error tracing

## Security Notes

- API credentials should be stored securely (in secrets management)
- The code uses `ast.literal_eval()` safely for parsing Python dict strings
- All API requests include proper timeout handling
- Error messages limit sensitive data exposure