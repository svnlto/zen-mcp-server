#!/usr/bin/env python3
"""
Schema Optimization Validation Test

This test validates that schema optimizations maintain functional compatibility
while achieving significant size reductions.
"""

import json
import tempfile
from pathlib import Path


def test_codereview_schema_optimization():
    """Test that CodeReview schema optimization preserves functionality"""
    from tools import CodeReviewTool

    tool = CodeReviewTool()
    schema = tool.get_input_schema()

    # Validate schema structure
    assert schema["type"] == "object"
    assert "properties" in schema
    assert "required" in schema

    # Check all required fields are preserved
    required_fields = {"step", "step_number", "total_steps", "next_step_required", "findings"}
    assert required_fields.issubset(set(schema["required"]))

    # Check all properties exist
    expected_properties = {
        "step",
        "step_number",
        "total_steps",
        "next_step_required",
        "findings",
        "files_checked",
        "relevant_files",
        "relevant_context",
        "issues_found",
        "confidence",
        "backtrack_from_step",
        "images",
        "review_type",
        "focus_on",
        "standards",
        "severity_filter",
        "use_assistant_model",
        "temperature",
        "thinking_mode",
        "use_websearch",
        "continuation_id",
        "model",
    }
    assert expected_properties.issubset(set(schema["properties"].keys()))

    # Validate schema size improvement
    schema_json = json.dumps(schema, separators=(",", ":"))
    schema_size = len(schema_json)

    # Should be significantly smaller than original (~8,789 chars)
    assert schema_size < 7000, f"Schema too large: {schema_size} chars"
    assert schema_size > 4000, f"Schema too small: {schema_size} chars (may be missing content)"

    print(f"✓ CodeReview schema optimized to {schema_size} chars")


def test_schema_functionality_preserved():
    """Test that schema optimization preserves tool functionality"""
    from tools import CodeReviewTool

    tool = CodeReviewTool()

    # Test valid request can be created
    test_request = {
        "step": "Test analysis of code quality",
        "step_number": 1,
        "total_steps": 3,
        "next_step_required": True,
        "findings": "Initial analysis shows good code structure",
        "relevant_files": ["/test/example.py"],
        "confidence": "medium",
        "model": "auto",  # Model field is typically required
    }

    # Validate against schema
    schema = tool.get_input_schema()

    # Check required fields
    for field in schema["required"]:
        assert field in test_request, f"Missing required field: {field}"

    # Check field types match schema expectations
    properties = schema["properties"]
    for field, value in test_request.items():
        if field in properties:
            field_schema = properties[field]
            if "type" in field_schema:
                expected_type = field_schema["type"]
                if expected_type == "string":
                    assert isinstance(value, str), f"{field} should be string"
                elif expected_type == "integer":
                    assert isinstance(value, int), f"{field} should be integer"
                elif expected_type == "boolean":
                    assert isinstance(value, bool), f"{field} should be boolean"
                elif expected_type == "array":
                    assert isinstance(value, list), f"{field} should be array"

    print("✓ Schema functionality preserved")


def test_multiple_tool_optimization_impact():
    """Test impact across multiple tools"""
    from tools import (
        AnalyzeTool,
        CodeReviewTool,
        DebugIssueTool,
        PrecommitTool,
        RefactorTool,
        SecauditTool,
        TestGenTool,
    )

    tools = {
        "codereview": CodeReviewTool(),
        "refactor": RefactorTool(),
        "debug": DebugIssueTool(),
        "secaudit": SecauditTool(),
        "precommit": PrecommitTool(),
        "analyze": AnalyzeTool(),
        "testgen": TestGenTool(),
    }

    total_original_estimate = {
        "codereview": 8789,
        "refactor": 8569,
        "debug": 7893,
        "secaudit": 9077,
        "precommit": 8634,
        "analyze": 6567,
        "testgen": 6374,
    }

    total_current = 0
    total_estimated_original = 0

    for name, tool in tools.items():
        schema = tool.get_input_schema()
        schema_json = json.dumps(schema, separators=(",", ":"))
        current_size = len(schema_json)
        estimated_original = total_original_estimate[name]

        total_current += current_size
        total_estimated_original += estimated_original

        print(f"{name}: {current_size} chars (was ~{estimated_original})")

    total_savings = total_estimated_original - total_current
    percentage_saved = (total_savings / total_estimated_original) * 100

    print(f"\nTotal savings: {total_savings:,} chars ({percentage_saved:.1f}%)")
    assert percentage_saved > 5, "Should achieve meaningful savings"

    return total_current, total_estimated_original, percentage_saved


def test_simulator_compatibility():
    """Test that optimized schemas work with simulator tests"""
    # Create a temporary test file for validation
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(
            """
def example_function():
    return "test"
        """
        )
        test_file = f.name

    try:
        from tools import CodeReviewTool

        tool = CodeReviewTool()

        # Test that tool can be instantiated and used
        assert tool.get_name() == "codereview"
        assert "code review" in tool.get_description().lower()

        # Test schema validation
        schema = tool.get_input_schema()
        assert "step" in schema["properties"]
        assert "step" in schema["required"]

        print("✓ Simulator compatibility maintained")

    finally:
        # Clean up
        Path(test_file).unlink(missing_ok=True)


def run_comprehensive_test():
    """Run all optimization tests"""
    print("Schema Optimization Validation")
    print("=" * 50)

    try:
        test_codereview_schema_optimization()
        test_schema_functionality_preserved()
        current, original, savings = test_multiple_tool_optimization_impact()
        test_simulator_compatibility()

        print("\n✅ All tests passed!")
        print(f"Schema optimization achieved {savings:.1f}% size reduction")
        print(f"Original total: ~{original:,} chars")
        print(f"Current total: {current:,} chars")
        print(f"Savings: {original - current:,} chars")

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)
