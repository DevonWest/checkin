#!/usr/bin/env python3
"""
Step 5: Commission → Policy Link Executor

This module handles linking commission records to policy records via the Kizen API.
It processes results from step 4 and creates the necessary API calls to establish
the relationships between commissions and policies.
"""

import ast
import json
import os
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import requests


class CommissionPolicyLinker:
    """Handles linking commission records to policy records via Kizen API."""
    
    def __init__(self, api_key: str, business_id: str, user_id: str, 
                 api_base: str = "https://app.go.kizen.com/api"):
        """Initialize the linker with API credentials."""
        self.api_base = api_base
        self.api_key = api_key
        self.business_id = business_id
        self.user_id = user_id
    
    def _headers(self) -> Dict[str, str]:
        """Generate API headers."""
        return {
            "X-API-KEY": self.api_key,
            "X-BUSINESS-ID": self.business_id,
            "X-USER-ID": self.user_id,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    
    def _validate_plan(self, plan: Dict[str, Any], commission_id: str) -> List[str]:
        """Validate that a plan has all required fields."""
        errors = []
        required_fields = ['commission_object_id', 'link_field_id_on_commission', 'policy_object_id']
        
        for field in required_fields:
            if field not in plan:
                errors.append(f"Missing required field '{field}' in plan for commission {commission_id}")
            elif not plan[field]:
                errors.append(f"Empty value for required field '{field}' in plan for commission {commission_id}")
        
        return errors
    
    def link_commission_to_policy(self, commission_id: str, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Link a single commission to a policy."""
        # Validate plan
        validation_errors = self._validate_plan(plan, commission_id)
        if validation_errors:
            return {
                "commission_id": commission_id,
                "success": False,
                "error": "Validation failed",
                "details": validation_errors
            }
        
        try:
            # Build API URL - using PUT as specified in original code
            url = f"{self.api_base}/records/{plan['commission_object_id']}/{commission_id}"
            
            # Build payload
            payload = {
                "fields": [{
                    "id": plan['link_field_id_on_commission'],
                    "value": {"id": plan['policy_object_id']}
                }]
            }
            
            print(f"Linking commission {commission_id} to policy {plan['policy_object_id']}")
            print(f"URL: {url}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Make API call
            response = requests.put(url, headers=self._headers(), json=payload, timeout=15)
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                return {
                    "commission_id": commission_id,
                    "policy_id": plan['policy_object_id'],
                    "success": True,
                    "result": "linked"
                }
            else:
                return {
                    "commission_id": commission_id,
                    "success": False,
                    "error": f"HTTP_{response.status_code}",
                    "response_text": response.text[:500]
                }
        
        except Exception as e:
            return {
                "commission_id": commission_id,
                "success": False,
                "error": str(e),
                "trace": traceback.format_exc()[-1000:]
            }
    
    def process_step4_data(self, step4_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process step 4 data and link commissions to policies."""
        print("=== Processing Step 4 Data ===")
        print(f"Step 4 keys: {list(step4_data.keys()) if isinstance(step4_data, dict) else step4_data}")
        
        ready_ids = step4_data.get("ready_to_link", [])
        planned_links = step4_data.get("planned_links", [])
        
        print(f"Ready to link: {ready_ids}")
        print(f"Number of planned links: {len(planned_links)}")
        
        # Create mapping from commission_id to plan
        commission_id_to_plan = {
            p['commission_id']: p 
            for p in planned_links 
            if 'commission_id' in p
        }
        
        print(f"Commission ID to plan mapping keys: {list(commission_id_to_plan.keys())}")
        
        # Process each commission
        attempted = 0
        linked = 0
        link_errors = []
        linked_commission_ids = []
        linked_pairs = []
        
        for commission_id in ready_ids:
            attempted += 1
            plan = commission_id_to_plan.get(commission_id, {})
            
            if not plan:
                link_errors.append({
                    "commission_id": commission_id,
                    "error": "No plan found for commission ID",
                    "details": f"Commission {commission_id} not found in planned_links"
                })
                continue
            
            print(f"Processing commission_id: {commission_id}")
            result = self.link_commission_to_policy(commission_id, plan)
            
            if result["success"]:
                linked += 1
                linked_commission_ids.append(commission_id)
                linked_pairs.append(result)
            else:
                link_errors.append(result)
        
        # Build final result
        return {
            "ok": len(link_errors) == 0,
            "message": f"Step 5 attempted {attempted} links. Success: {linked}, Errors: {len(link_errors)}",
            "timestamp": datetime.utcnow().isoformat(),
            "user": "DevonWest",
            "attempted": attempted,
            "linked": linked,
            "linked_commission_ids": linked_commission_ids,
            "linked_pairs": linked_pairs,
            "errors": link_errors,
            "input_ready_ids": ready_ids,
        }


def extract_step4_data(step4_raw: Any) -> Optional[str]:
    """Robustly extract step 4 data from various input formats."""
    s4 = None
    if step4_raw is not None:
        if hasattr(step4_raw, "v"):
            s4 = step4_raw.v
        elif isinstance(step4_raw, dict) and "v" in step4_raw:
            s4 = step4_raw["v"]
        elif isinstance(step4_raw, str):
            s4 = step4_raw
    return s4


def parse_step4_data(s4: str) -> Dict[str, Any]:
    """Parse step 4 data string into a dictionary."""
    try:
        # Try JSON first (safer)
        return json.loads(s4)
    except (json.JSONDecodeError, TypeError):
        try:
            # Fall back to ast.literal_eval for Python dict strings
            return ast.literal_eval(s4)
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Could not parse step 4 data: {e}")


def main():
    """Main execution function - handles the workflow context."""
    print("=== STEP 5: Commission → Policy Link Executor ===")
    
    try:
        # Try to get inputs from workflow context, or use environment variables for testing
        try:
            step4_raw = getattr(inputs, "step4ResultJson", None)
        except NameError:
            # For testing, try to get from environment
            step4_raw = os.environ.get("STEP4_RESULT_JSON")
            if not step4_raw:
                raise ValueError("No inputs object found and STEP4_RESULT_JSON environment variable not set")
        
        # Extract step 4 data
        s4 = extract_step4_data(step4_raw)
        if not s4:
            raise ValueError("Step 4 input is missing or empty!")
        
        print("RAW step4 input:", repr(s4))
        
        # Parse step 4 data
        step4_data = parse_step4_data(s4)
        
        # Get API credentials
        try:
            api_key = secrets["kizen_api_key"]
            business_id = secrets["x_business_id"]
            user_id = secrets["x_user_id"]
        except NameError:
            # For testing, try environment variables
            api_key = os.environ.get("KIZEN_API_KEY")
            business_id = os.environ.get("X_BUSINESS_ID")
            user_id = os.environ.get("X_USER_ID")
            
            if not all([api_key, business_id, user_id]):
                raise ValueError("Missing required API credentials")
        
        # Create linker and process data
        linker = CommissionPolicyLinker(api_key, business_id, user_id)
        result = linker.process_step4_data(step4_data)
        
        print("Final result:", result)
        
        # Set outputs
        try:
            outputs.step5_result_json = json.dumps(result)
        except NameError:
            # For testing, just print the result
            print("RESULT JSON:", json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"💥 FATAL ERROR: {e}")
        fail = {
            "ok": False,
            "message": "Step 5 failed.",
            "timestamp": datetime.utcnow().isoformat(),
            "user": "DevonWest",
            "error": str(e)[:500],
            "trace": traceback.format_exc()[-2000:],
        }
        
        try:
            outputs.step5_result_json = json.dumps(fail)
        except NameError:
            print("FAILURE JSON:", json.dumps(fail, indent=2))
    
    print("=== END STEP 5 ===")


if __name__ == "__main__":
    main()