# 🤖 Intelligent Terraform Drift Detection & AI Remediation Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Terraform](https://img.shields.io/badge/Terraform-State_Parser-844FBA?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Azure](https://img.shields.io/badge/Azure_Resource_Graph-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge)](#license)

> **Autonomous AI-assisted SRE agent and Python engine that parses Terraform execution states, scans live Azure cloud inventories, detects out-of-band configuration drift, and generates corrective HCL pull requests.**

---

## 🏛️ Autonomous Drift Detection Workflow

```mermaid
flowchart TD
    TF_STATE["Terraform State File<br/>(terraform show -json)"] --> PARSER["Python State Parser<br/>(Extracts Declared Addresses)"]
    AZ_CLOUD["Live Azure Cloud API<br/>(Resource Graph & SDK)"] --> SCANNER["Live Cloud Scanner<br/>(Extracts Active Inventory)"]
    
    PARSER --> DIFF["AI Drift Detection Engine<br/>(Cross-References Deltas)"]
    SCANNER --> DIFF
    
    DIFF --> REPORT["Markdown Drift Scorecard<br/>(Detailed SRE Triage)"]
    DIFF --> HCL["Remediation Generator<br/>(Produces HCL Import / Fix Blocks)"]
    
    HCL --> PR["Automated GitHub PR<br/>(Zero-Touch Remediation)"]

    style DIFF fill:#1E293B,stroke:#00F2FE,stroke-width:2px,color:#FFFFFF
    style REPORT fill:#0F172A,stroke:#F43F5E,stroke-width:2px,color:#FFFFFF
    style PR fill:#0F172A,stroke:#10B981,stroke-width:2px,color:#FFFFFF
```

---

## 🚀 Key Capabilities

* **Cryptographic State Parsing:** Parses deep, multi-tier JSON modules and child modules from `terraform show -json` without external CLI dependencies.
* **Out-of-Band Change Detection:** Uncovers manually opened NSG inbound rules, modified storage public access settings, or deleted private endpoints.
* **Orphaned Asset Identification:** Pinpoints unattached Azure Managed Disks, disassociated Public IPs, and idle App Service plans costing unbudgeted cloud dollars.
* **Automated Corrective HCL Blocks:** Emits ready-to-merge `import { ... }` blocks and Terraform HCL patches to bring infrastructure back into 100% compliant code synchronization.

---

## 🛠️ Usage & Installation

```bash
# Clone the repository
git clone https://github.com/kumarsumanpriya/ai-terraform-drift-agent.git
cd ai-terraform-drift-agent

# Install dependencies
pip install -r requirements.txt

# Run drift inspection CLI
python -m drift_agent.cli analyze --state-file examples/sample_tfstate.json --report-output drift_report.md

# Run test suite
pytest -v
```

---

## 👨‍💻 Author

**Kumar Suman Priya**  
*Lead DevSecOps & Cloud Platform Engineer*  
GitHub: [@kumarsumanpriya](https://github.com/kumarsumanpriya)
