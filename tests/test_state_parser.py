import os
from drift_agent.state_parser import TerraformStateParser
from drift_agent.drift_analyzer import DriftAnalyzer

def test_extract_resources():
    sample_path = os.path.join(os.path.dirname(__file__), "..", "examples", "sample_tfstate.json")
    parser = TerraformStateParser(sample_path)
    resources = parser.extract_resources()

    assert len(resources) == 2
    assert "module.vnet.azurerm_virtual_network.vnet" in resources
    assert "module.aks.azurerm_kubernetes_cluster.aks" in resources

def test_drift_analyzer_unmanaged():
    declared = {
        "res.1": {"type": "azurerm_subnet", "name": "snet1", "values": {"id": "/sub/1"}}
    }
    live = {
        "/sub/1": {"type": "azurerm_subnet", "name": "snet1"},
        "/sub/2": {"type": "azurerm_public_ip", "name": "rogue-ip", "resource_group": "rg-prod"}
    }
    analyzer = DriftAnalyzer(declared, live)
    result = analyzer.analyze()

    assert result["unmanaged_count"] == 1
    assert result["unmanaged_resources"][0]["name"] == "rogue-ip"
