"""Evaluate Python code and check against expected results."""
import io
import sys
import contextlib
import random
from typing import Dict, Any, Optional, List


class EvaluationResult:
    """Result of code evaluation."""
    
    def __init__(self, success: bool, output: str, error: Optional[str] = None):
        self.success = success
        self.output = output.strip()
        self.error = error


class CodeEvaluator:
    """Evaluates user code and checks against level requirements."""
    
    def __init__(self):
        pass
    
    def execute_code(self, code: str, required_file: Optional[Dict] = None) -> EvaluationResult:
        """
        Execute Python code safely and capture output.
        
        Args:
            code: The Python code to execute
            required_file: Optional dict with 'filename' and 'content' to create before execution
        
        Returns:
            EvaluationResult with success status, output, and any error
        """
        # Create temporary file if required
        if required_file:
            try:
                with open(required_file["filename"], "w", encoding="utf-8") as f:
                    f.write(required_file["content"])
            except Exception as e:
                return EvaluationResult(False, "", f"Error creating file: {e}")
        
        # Capture stdout
        output_buffer = io.StringIO()
        error_msg = None
        success = False
        
        try:
            # Execute the code with captured stdout
            with contextlib.redirect_stdout(output_buffer):
                # Create a restricted namespace
                namespace = {
                    '__builtins__': __builtins__,
                    'random': random,  # Allow random module
                }
                exec(code, namespace)
            success = True
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
        
        output = output_buffer.getvalue()
        return EvaluationResult(success, output, error_msg)
    
    def check_result(self, result: EvaluationResult, checker: Dict[str, Any]) -> bool:
        """
        Check if the result matches the expected output.
        
        Args:
            result: The execution result
            checker: The checker configuration from level JSON
        
        Returns:
            True if the result passes the check, False otherwise
        """
        if not result.success:
            return False
        
        checker_type = checker.get("type")
        
        if checker_type == "output_contains":
            expected = checker["expected"]
            case_sensitive = checker.get("case_sensitive", False)
            output = result.output if case_sensitive else result.output.lower()
            expected = expected if case_sensitive else expected.lower()
            return expected in output
        
        elif checker_type == "output_lines":
            expected_lines = checker["expected"]
            output_lines = [line.strip() for line in result.output.split('\n') if line.strip()]
            return output_lines == expected_lines
        
        elif checker_type == "output_range":
            try:
                output_num = int(result.output.strip())
                min_val = checker["min"]
                max_val = checker["max"]
                return min_val <= output_num <= max_val
            except ValueError:
                return False
        
        elif checker_type == "multi_test":
            # This requires running multiple test cases
            # For now, return True if the code executed successfully
            # This will be handled by the game loop running multiple tests
            return True
        
        return False
    
    def evaluate_level(self, code: str, level) -> tuple[bool, str]:
        """
        Evaluate code for a specific level.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Handle multi-test cases specially
        if level.checker.get("type") == "multi_test":
            tests = level.checker.get("tests", [])
            for i, test in enumerate(tests):
                # Replace the security_level line with test value
                test_code = code
                if "code_modification" in test:
                    lines = code.split('\n')
                    modified_lines = []
                    for line in lines:
                        if 'security_level' in line and '=' in line:
                            modified_lines.append(test["code_modification"])
                        else:
                            modified_lines.append(line)
                    test_code = '\n'.join(modified_lines)
                
                result = self.execute_code(test_code, level.requires_file)
                
                if not result.success:
                    return False, f"Test {i+1} failed: {result.error}"
                
                expected = test["expected_output"]
                if expected.lower() not in result.output.lower():
                    return False, f"Test {i+1} failed: Expected '{expected}', got '{result.output}'"
            
            return True, "All tests passed!"
        
        # Regular single test
        result = self.execute_code(code, level.requires_file)
        
        if not result.success:
            return False, f"Error: {result.error}"
        
        if self.check_result(result, level.checker):
            return True, f"Success! Output: {result.output}"
        else:
            return False, f"Output doesn't match expected. Got: {result.output}"
