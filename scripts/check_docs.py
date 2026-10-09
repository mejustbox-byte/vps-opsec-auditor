"""Offline documentation readiness check; no product behavior is tested."""
import ipaddress
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["README.md", "requirements.md", "threat-model.md", "architecture.md",
            "checks.md", "lab.md", "adr/0001-stack.md", "environment.md",
            "mvp.md", "input.md", "release-notes.md"]
IDS = {"NET-01", "SSH-01", "FW-01", "IAM-01", "MFA-01", "META-01",
       "DNS-01", "TLS-01", "BAK-01", "REC-01"}


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def main():
    for name in REQUIRED:
        p = ROOT / "docs" / name
        require(p.is_file() and len(p.read_text().strip()) > 100, f"missing/empty {name}")
    for p in (ROOT / "docs").rglob("*.md"):
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", p.read_text()):
            if "://" in link:
                require(link.startswith("https://github.com/mejustbox-byte/vps-opsec-auditor/"), f"unexpected external link: {p.name}")
                continue
            require((p.parent / link.split("#")[0]).is_file(), f"broken link: {link}")
    matrix = (ROOT / "docs/checks.md").read_text()
    require(set(re.findall(r"\b[A-Z]+-\d{2}\b", matrix)) == IDS, "matrix IDs mismatch")
    data = json.loads((ROOT / "fixtures/synthetic-audit.json").read_text())
    require(data["synthetic"] is True, "fixture must be synthetic")
    for key, network in [("example_ipv4", "192.0.2.0/24"), ("example_ipv6", "2001:db8::/32")]:
        require(ipaddress.ip_address(data[key]) in ipaddress.ip_network(network), "non-documentation address")
    require(data["example_domain"].endswith(".invalid"), "non-synthetic domain")
    findings = data["findings"]
    require(len(findings) == len(IDS) and {f["check_id"] for f in findings} == IDS, "fixture coverage mismatch")
    require(all(f["status"] == "unverified" and f["reason"] for f in findings), "unsupported verified claim")
    print(f"PASS: {len(REQUIRED)} required documents, local links, {len(IDS)} matrix IDs and synthetic fixture; no network")


if __name__ == "__main__":
    main()
