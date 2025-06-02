# AWS IAM Inspector

A simple Python script to list all IAM users in an AWS account along with their:

- Assigned IAM Groups
- Attached IAM Policies
- Inline IAM Policies

🔒 **Roles are intentionally excluded.**

---

## 🛠️ Requirements

- Python 3.x
- Boto3 (`pip install boto3`)
- AWS credentials configured (via `aws configure` or environment variables)
