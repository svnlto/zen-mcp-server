#!/usr/bin/env python3
"""
Schema Size Analysis and Validation Test

This script analyzes tool schema sizes and validates that optimizations
maintain the same functionality while reducing JSON schema bloat.
"""

import json
from typing import Any


def get_all_tools():
    """Get all available tools for testing"""
    from tools import (
        AnalyzeTool,
        ChallengeTool,
        ChatTool,
        CodeReviewTool,
        ConsensusTool,
        DebugIssueTool,
        DocgenTool,
        ListModelsTool,
        PlannerTool,
        PrecommitTool,
        RefactorTool,
        SecauditTool,
        TestGenTool,
        ThinkDeepTool,
        TracerTool,
        VersionTool,
    )

    return {
        "analyze": AnalyzeTool(),
        "challenge": ChallengeTool(),
        "chat": ChatTool(),
        "codereview": CodeReviewTool(),
        "consensus": ConsensusTool(),
        "debug": DebugIssueTool(),
        "docgen": DocgenTool(),
        "listmodels": ListModelsTool(),
        "planner": PlannerTool(),
        "precommit": PrecommitTool(),
        "refactor": RefactorTool(),
        "secaudit": SecauditTool(),
        "testgen": TestGenTool(),
        "thinkdeep": ThinkDeepTool(),
        "tracer": TracerTool(),
        "version": VersionTool(),
    }


def analyze_schema_size(tool_name: str, tool: Any) -> dict[str, Any]:
    """Analyze schema size and complexity for a tool"""
    schema = tool.get_input_schema()
    schema_json = json.dumps(schema, separators=(",", ":"))

    properties = schema.get("properties", {})
    required = schema.get("required", [])

    # Calculate description lengths
    desc_lengths = {}
    total_desc_length = 0
    max_desc_length = 0
    max_desc_field = ""

    for prop_name, prop_def in properties.items():
        desc = prop_def.get("description", "")
        desc_length = len(desc)
        desc_lengths[prop_name] = desc_length
        total_desc_length += desc_length

        if desc_length > max_desc_length:
            max_desc_length = desc_length
            max_desc_field = prop_name

    return {
        "tool_name": tool_name,
        "schema_size": len(schema_json),
        "property_count": len(properties),
        "required_count": len(required),
        "total_description_length": total_desc_length,
        "max_description_length": max_desc_length,
        "max_description_field": max_desc_field,
        "description_lengths": desc_lengths,
    }


def print_schema_analysis():
    """Print comprehensive schema analysis"""
    tools = get_all_tools()
    analyses = []

    print("=" * 80)
    print("SCHEMA SIZE ANALYSIS")
    print("=" * 80)

    for tool_name, tool in tools.items():
        analysis = analyze_schema_size(tool_name, tool)
        analyses.append(analysis)

    # Sort by schema size (largest first)
    analyses.sort(key=lambda x: x["schema_size"], reverse=True)

    print(f"{'Tool':<15} {'Schema':<8} {'Props':<6} {'Req':<4} {'Total Desc':<11} {'Max Desc':<9} {'Field'}")
    print("-" * 80)

    for analysis in analyses:
        print(
            f"{analysis['tool_name']:<15} "
            f"{analysis['schema_size']:<8} "
            f"{analysis['property_count']:<6} "
            f"{analysis['required_count']:<4} "
            f"{analysis['total_description_length']:<11} "
            f"{analysis['max_description_length']:<9} "
            f"{analysis['max_description_field']}"
        )

    # Show top 3 largest schemas in detail
    print("\n" + "=" * 80)
    print("TOP 3 LARGEST SCHEMAS - FIELD BREAKDOWN")
    print("=" * 80)

    for analysis in analyses[:3]:
        print(f"\n{analysis['tool_name'].upper()} ({analysis['schema_size']} chars total)")
        print("-" * 60)

        # Sort fields by description length
        sorted_fields = sorted(analysis["description_lengths"].items(), key=lambda x: x[1], reverse=True)

        for field_name, desc_length in sorted_fields[:10]:  # Top 10 fields
            print(f"  {field_name:<25} {desc_length:>4} chars")

    return analyses


def validate_schema_functionality(tool_name: str, original_schema: dict, optimized_schema: dict):
    """Validate that schema optimization maintains functionality"""
    errors = []

    # Check that all required fields are preserved
    orig_required = set(original_schema.get("required", []))
    opt_required = set(optimized_schema.get("required", []))

    if orig_required != opt_required:
        errors.append(f"Required fields changed: {orig_required} vs {opt_required}")

    # Check that all properties are preserved
    orig_props = set(original_schema.get("properties", {}).keys())
    opt_props = set(optimized_schema.get("properties", {}).keys())

    if orig_props != opt_props:
        errors.append(f"Properties changed: {orig_props} vs {opt_props}")

    # Check property types are preserved
    for prop_name in orig_props & opt_props:
        orig_type = original_schema["properties"][prop_name].get("type")
        opt_type = optimized_schema["properties"][prop_name].get("type")

        if orig_type != opt_type:
            errors.append(f"Type changed for {prop_name}: {orig_type} vs {opt_type}")

    return errors


if __name__ == "__main__":
    print_schema_analysis()
