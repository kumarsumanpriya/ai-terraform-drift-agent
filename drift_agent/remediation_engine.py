from typing import Dict, Any

class RemediationEngine:
    """
    Generates actionable remediation plans and HCL import blocks for detected drift.
    """

    @staticmethod
    def generate_markdown_report(analysis_results: Dict[str, Any]) -> str:
        lines = [
            "# 🤖 AI Drift Analysis & SRE Remediation Report",
            "",
            f"**Total Declared Resources:** {analysis_results['total_declared']}",
            f"**Total Live Cloud Assets:** {analysis_results['total_live']}",
            f"**Unmanaged / Rogue Assets:** {analysis_results['unmanaged_count']}",
            f"**Missing Resources:** {analysis_results['missing_count']}",
            "",
            "## 🚨 Detected Unmanaged Cloud Resources",
            "These resources exist in Azure but have no corresponding Terraform code declaration:",
            ""
        ]

        if not analysis_results["unmanaged_resources"]:
            lines.append("✅ No unmanaged or orphaned resources detected. Infrastructure is in pristine synchronization.")
        else:
            lines.append("| Resource Name | Azure Resource Type | Resource Group |")
            lines.append("|---|---|---|")
            for r in analysis_results["unmanaged_resources"]:
                lines.append(f"| `{r['name']}` | `{r['type']}` | `{r['resource_group']}` |")

        lines.extend([
            "",
            "## 🛠️ Automated Remediation Actions",
            "1. Run `terraform plan -refresh-only` to reconcile in-flight state discrepancies.",
            "2. Import rogue production assets using `import` blocks or initiate automated teardown ticket.",
            ""
        ])

        return "\n".join(lines)

    @staticmethod
    def generate_hcl_import_block(resource_type: str, resource_name: str, azure_id: str) -> str:
        return f"""import {{
  to = {resource_type}.{resource_name}
  id = "{azure_id}"
}}
"""
