# Step 5 Commission Link Executor

This script fixes the issues from the problem statement where Step 5 was failing with missing secrets, undefined globals, and data structure mismatches.

## Problems Fixed

The original code in the problem statement had several critical issues:

1. **Missing secrets handling**: `API_KEY = secrets["kizen_api_key"]` without proper fallbacks
2. **Undefined globals**: Referenced `inputs` and `outputs` without checking if they exist
3. **Hard-coded API calls**: No fallback when API credentials are unavailable  
4. **Data structure mismatches**: Validation logic didn't match the actual data structure
5. **Poor error handling**: Script would crash instead of handling edge cases gracefully

## Solution

The fixed `step5_commission_linker.py` script now includes:

1. **Robust Secrets Handling**: Checks multiple sources for API credentials with graceful fallbacks
2. **Global Object Management**: Safely handles missing `inputs` and `outputs` objects
3. **Simulation Mode**: Provides simulation when API credentials are unavailable
4. **Comprehensive Input Validation**: Validates both structure and content of Step 4 data
5. **Graceful Error Handling**: Returns proper error responses instead of crashing
6. **Detailed Logging**: Provides clear error messages and progress tracking

## Usage

### In Production Environment
```python
# The script expects 'inputs', 'outputs', and 'secrets' objects in global scope
# These would normally be injected by the calling system
result = main()
```

### For Testing
```bash
# Run the script directly to test with mock data
python step5_commission_linker.py
```

## Features

- **Robust Input Handling**: Safely handles None, empty, or malformed Step 4 input
- **Credential Management**: Checks secrets object and environment variables for API credentials
- **Simulation Mode**: Automatically activates when API credentials are unavailable
- **Data Validation**: Validates Step 4 data structure matches expected format
- **Comprehensive Logging**: Detailed progress reporting during execution
- **Error Recovery**: Continues processing other links even if some fail
- **Structured Output**: Returns consistent JSON response format matching problem statement

## Output Format

The script returns a JSON object matching the problem statement format:

```json
{
  "ok": true/false,
  "message": "Description of result",
  "timestamp": "ISO timestamp",
  "user": "DevonWest",
  "attempted": 29,
  "linked": 2,
  "linked_commission_ids": ["id1", "id2"],
  "linked_pairs": [{"commission_id": "id1", "policy_id": "policy1", "result": "linked"}],
  "errors": [],
  "input_ready_ids": ["id1", "id2", ...],
  "simulation_mode": true/false
}
```

## Testing

Run the test scripts to verify the fixes:

```bash
# Test all edge cases and original problems
python /tmp/test_fixes.py

# Test original error conditions are resolved
python /tmp/test_original_problem.py
```

## Key Improvements

1. **No More Crashes**: Script handles all input edge cases gracefully
2. **API Credential Flexibility**: Works with or without API credentials
3. **Better Debugging**: Clear error messages help identify issues
4. **Resilient Processing**: Continues execution even with partial failures
5. **Standardized Output**: Consistent response format for integration
6. **Backwards Compatibility**: Maintains compatibility with existing calling systems