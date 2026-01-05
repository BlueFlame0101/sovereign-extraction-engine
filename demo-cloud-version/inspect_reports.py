"""
Report Inspection Utility - Departmental Output Validation.

This module provides a diagnostic tool for inspecting raw departmental
reports prior to macro-council deliberation. Useful for validating
micro-agent output quality and inference latency.

Output:
    Formatted departmental reports with execution timing metrics.
"""

from micro_council import consult_finance, consult_growth, consult_tech
import time


def generate_official_reports():
    """
    Execute full micro-council inference and display formatted reports.
    
    Invokes all three departmental consultation functions and outputs
    the synthesized reports that will be forwarded to the macro-council
    debate phase. Includes execution duration metrics.
    """
    query = "Should we pause the AWS migration to save cash?"
    
    print(f"GENERATING DEPARTMENT REPORTS FOR QUERY: '{query}'")
    print("(Processing... awaiting worker inference completion)\n")
    
    start = time.time()

    # Finance Department Inference
    print("   [Finance] Consulting department...")
    report_finance = consult_finance(query)
    
    # Growth Department Inference
    print("   [Growth] Consulting department...")
    report_growth = consult_growth(query)
    
    # Tech Department Inference
    print("   [Tech] Consulting department...")
    report_tech = consult_tech(query)
    
    duration = time.time() - start

    # Formatted Report Output
    print("\n" + "="*80)
    print(f"OFFICIAL DEPARTMENT REPORTS (Generated in {duration:.1f}s)")
    print("="*80)

    print(f"\n[DEPARTMENT A: FINANCE]")
    print("-" * 40)
    print(report_finance)
    print("-" * 40)

    print(f"\n[DEPARTMENT B: GROWTH]")
    print("-" * 40)
    print(report_growth)
    print("-" * 40)

    print(f"\n[DEPARTMENT C: TECH]")
    print("-" * 40)
    print(report_tech)
    print("-" * 40)
    print("\nReports ready for macro-council deliberation.")


if __name__ == "__main__":
    generate_official_reports()
