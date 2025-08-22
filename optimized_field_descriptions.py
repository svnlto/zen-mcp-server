"""
Optimized Field Descriptions for Schema Size Reduction

This module contains condensed, optimized field descriptions that maintain
all essential information while significantly reducing JSON schema bloat.

Optimization principles:
1. Remove redundant instructions repeated across fields
2. Condense verbose explanations into concise, clear directives
3. Eliminate unnecessary examples and repetitive warnings
4. Preserve all functional requirements and constraints
"""

# Common patterns that can be shared across fields to reduce repetition
COMMON_PATTERNS = {
    "file_paths": "Use full absolute paths, do not shorten",
    "continuation_note": "When continuing a conversation, adjust workflow accordingly",
    "no_large_code": "Reference files via relevant_files, not in text descriptions",
}

# Optimized CodeReview field descriptions (original total: ~6,916 chars)
CODEREVIEW_OPTIMIZED_DESCRIPTIONS = {
    "step": (
        f"Describe current code review investigation. Step 1: State review plan and pass initial files via relevant_files. "
        f"Examine code quality, security, performance, architecture. Consider complexity, scaling, abstractions. "
        f"Later steps: trace dependencies, verify assumptions. {COMMON_PATTERNS['no_large_code']}"
    ),  # Reduced from 1390 to ~290 chars
    "step_number": "Current step index, starting at 1. Each step builds on previous.",  # Reduced from 130 to 70 chars
    "total_steps": (
        f"Estimated steps to complete review. Adjust as needed. {COMMON_PATTERNS['continuation_note']}"
    ),  # Reduced from 265 to ~90 chars
    "next_step_required": (
        f"True to continue investigation, False when complete. {COMMON_PATTERNS['continuation_note']}"
    ),  # Reduced from 311 to ~90 chars
    "findings": (
        "Summarize discoveries: code quality, security, performance, architecture, bugs, patterns. "
        "Document both positive findings and concerns. Be specific, update in later steps."
    ),  # Reduced from 642 to ~170 chars
    "files_checked": f"All files examined during review. {COMMON_PATTERNS['file_paths']}",  # Reduced from 215 to ~70 chars
    "relevant_files": (
        f"Step 1: code files to review. Final step: files with key findings/issues. {COMMON_PATTERNS['file_paths']}"
    ),  # Reduced from 563 to ~110 chars
    "relevant_context": "Key methods/functions/classes central to findings (format: ClassName.method, functionName)",  # Reduced from 53 to 95 chars (acceptable)
    "issues_found": (
        "Issues identified: dict with 'severity' (critical/high/medium/low) and 'description'. "
        "Include security, performance, quality, architecture issues."
    ),  # Reduced from 334 to ~150 chars
    "confidence": (
        "Assessment confidence: 'exploring' (starting), 'low' (early), 'medium' (some evidence), "
        "'high' (strong evidence), 'very_high' (comprehensive analysis)"
    ),  # Reduced from 745 to ~180 chars
}

# Optimized Refactor field descriptions
REFACTOR_OPTIMIZED_DESCRIPTIONS = {
    "step": (
        f"Describe refactoring analysis. Step 1: State plan, pass files via relevant_files. "
        f"Examine code smells, complexity, maintainability. {COMMON_PATTERNS['no_large_code']}"
    ),  # Heavily reduced
    "findings": (
        "Summarize refactoring opportunities: code smells, complexity issues, improvement suggestions. "
        "Be specific about patterns and solutions."
    ),
    "confidence": ("Analysis confidence: 'exploring', 'low', 'medium', 'high', 'very_high'"),
}

# Optimized Debug field descriptions
DEBUG_OPTIMIZED_DESCRIPTIONS = {
    "step": (
        f"Describe debugging investigation. Step 1: State problem analysis plan, pass files via relevant_files. "
        f"Trace execution, identify root causes. {COMMON_PATTERNS['no_large_code']}"
    ),
    "findings": (
        "Debug discoveries: error analysis, root causes, execution flow issues, potential fixes. "
        "Include evidence and reasoning."
    ),
    "confidence": "Debug analysis confidence: 'exploring', 'low', 'medium', 'high', 'very_high'",
}

# Optimized SecAudit field descriptions
SECAUDIT_OPTIMIZED_DESCRIPTIONS = {
    "step": (
        f"Describe security audit investigation. Step 1: State audit plan, pass files via relevant_files. "
        f"Examine OWASP Top 10, authentication, data validation. {COMMON_PATTERNS['no_large_code']}"
    ),
    "findings": (
        "Security findings: vulnerabilities, compliance issues, attack vectors, security gaps. "
        "Include severity and impact assessment."
    ),
    "confidence": "Security assessment confidence: 'exploring', 'low', 'medium', 'high', 'very_high'",
}


def calculate_savings():
    """Calculate schema size savings from optimizations"""

    from tools import CodeReviewTool

    # Get original schema
    tool = CodeReviewTool()
    original_schema = tool.get_input_schema()

    # Calculate original description lengths
    original_desc_total = 0
    optimized_desc_total = 0

    for field_name, field_def in original_schema["properties"].items():
        original_desc = field_def.get("description", "")
        original_desc_total += len(original_desc)

        if field_name in CODEREVIEW_OPTIMIZED_DESCRIPTIONS:
            optimized_desc = CODEREVIEW_OPTIMIZED_DESCRIPTIONS[field_name]
            optimized_desc_total += len(optimized_desc)
        else:
            optimized_desc_total += len(original_desc)  # Keep unchanged fields

    savings = original_desc_total - optimized_desc_total
    percentage = (savings / original_desc_total) * 100

    print("CodeReview Optimization Analysis:")
    print(f"Original description total: {original_desc_total:,} chars")
    print(f"Optimized description total: {optimized_desc_total:,} chars")
    print(f"Savings: {savings:,} chars ({percentage:.1f}%)")

    return savings, percentage


if __name__ == "__main__":
    calculate_savings()
