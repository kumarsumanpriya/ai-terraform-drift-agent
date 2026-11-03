import json
from typing import Dict, List, Any, Optional

class TerraformStateParser:
    """
    Parses Terraform JSON state representations (from `terraform show -json` or state files).
    Extracts managed resources, addresses, types, and configured attributes.
    """

    def __init__(self, state_json_path: str):
        self.state_json_path = state_json_path
        self.raw_data = self._load_json()

    def _load_json(self) -> Dict[str, Any]:
        with open(self.state_json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def extract_resources(self) -> Dict[str, Dict[str, Any]]:
        """
        Extracts all managed resources keyed by their unique Terraform resource address.
        """
        resources = {}
        
        # Check values.root_module (standard terraform show -json format)
        root_module = self.raw_data.get("values", {}).get("root_module", {})
        self._traverse_module(root_module, resources)

        # Fallback for raw terraform.tfstate format
        if not resources and "resources" in self.raw_data:
            for res in self.raw_data.get("resources", []):
                mode = res.get("mode")
                if mode == "managed":
                    res_type = res.get("type")
                    res_name = res.get("name")
                    addr = f"{res_type}.{res_name}"
                    instances = res.get("instances", [])
                    attrs = instances[0].get("attributes", {}) if instances else {}
                    resources[addr] = {
                        "address": addr,
                        "type": res_type,
                        "name": res_name,
                        "values": attrs
                    }

        return resources

    def _traverse_module(self, module: Dict[str, Any], resources: Dict[str, Dict[str, Any]]):
        for res in module.get("resources", []):
            addr = res.get("address")
            resources[addr] = {
                "address": addr,
                "type": res.get("type"),
                "name": res.get("name"),
                "values": res.get("values", {})
            }

        for child in module.get("child_modules", []):
            self._traverse_module(child, resources)
