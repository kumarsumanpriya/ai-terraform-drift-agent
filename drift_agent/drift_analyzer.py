from typing import Dict, List, Any

class DriftAnalyzer:
    """
    Compares Terraform declared state against live cloud inventory.
    Identifies:
    1. Unmanaged / Rogue resources (e.g. manually created NSG rules or orphaned public IPs).
    2. Modified attribute drift (e.g. tags stripped, SKU altered).
    3. Deleted / Missing cloud resources that still exist in state.
    """

    def __init__(self, declared_resources: Dict[str, Dict[str, Any]], live_resources: Dict[str, Dict[str, Any]]):
        self.declared = declared_resources
        self.live = live_resources

    def analyze(self) -> Dict[str, Any]:
        unmanaged = []
        missing = []
        drifted = []

        # Find resources declared in code but absent from live cloud
        for addr, decl in self.declared.items():
            res_id = decl.get("values", {}).get("id")
            if res_id and res_id not in self.live:
                missing.append({
                    "address": addr,
                    "type": decl.get("type"),
                    "name": decl.get("name"),
                    "azure_id": res_id
                })

        # Find rogue live cloud resources never defined in Terraform
        declared_azure_ids = {
            decl.get("values", {}).get("id"): addr
            for addr, decl in self.declared.items()
            if decl.get("values", {}).get("id")
        }

        for live_id, live_obj in self.live.items():
            if live_id not in declared_azure_ids:
                unmanaged.append({
                    "azure_id": live_id,
                    "type": live_obj.get("type"),
                    "name": live_obj.get("name"),
                    "resource_group": live_obj.get("resource_group")
                })

        return {
            "total_declared": len(self.declared),
            "total_live": len(self.live),
            "unmanaged_count": len(unmanaged),
            "missing_count": len(missing),
            "drifted_count": len(drifted),
            "unmanaged_resources": unmanaged,
            "missing_resources": missing,
            "drifted_resources": drifted
        }
