"""Автономная проверка документов; поведение продукта не подтверждает."""
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
        raise SystemExit("ОШИБКА: " + message)


def main():
    for name in REQUIRED:
        p = ROOT / "docs" / name
        require(p.is_file() and len(p.read_text().strip()) > 100, f"нет документа или он пуст: {name}")
    documents = list((ROOT / "docs").rglob("*.md")) + list((ROOT / ".github").rglob("*.md"))
    root_required = ["README.md", "ARCHITECTURE.md", "TECH-STACK.md", "INSTALL.md", "CONTRIBUTING.md",
                     "ROADMAP.md", "SECURITY.md", "CHANGELOG.md", "THREAT-MODEL.md", "CORE-CONTRACT.md",
                     "RUNBOOK.md", "CLOUD-DEVELOPMENT.md", "LOCAL-PC.md", "VERIFICATION.md",
                     "RELEASE-CHECKLIST.md", "RELEASE-NOTES.md", "AGENTS.md", "LICENSE.ru.md",
                     "EVIDENCE-POLICY.md", "SUPPLY-CHAIN.md", "SECURITY-TESTING.md"]
    for name in root_required:
        require((ROOT / name).is_file(), f"нет обязательного раздела: {name}")
    documents += list(ROOT.glob("*.md"))
    for p in documents:
        require(p.is_file(), f"нет документа: {p.name}")
        content = p.read_text()
        require(re.search(r"[А-Яа-яЁё]", content) is not None, f"нет русского текста: {p.name}")
        prose = re.sub(r"```.*?```", "", content, flags=re.S)
        prose = re.sub(r"`[^`]*`", "", prose, flags=re.S)
        for line in prose.splitlines():
            words = re.findall(r"[A-Za-z]{3,}", line)
            if len(words) >= 7 and "://" not in line and not re.search(r"[А-Яа-яЁё]", line):
                require(False, f"возможный непереведённый текст: {p.name}")
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", p.read_text()):
            if "://" in link:
                require(link.startswith("https://github.com/mejustbox-byte/vps-opsec-auditor/") or link == "https://opensource.org/license/mit", f"неожиданная внешняя ссылка: {p.name}")
                continue
            require((p.parent / link.split("#")[0]).is_file(), f"повреждённая ссылка: {link}")
    matrix = (ROOT / "docs/checks.md").read_text()
    require(set(re.findall(r"\b[A-Z]+-\d{2}\b", matrix)) == IDS, "ID матрицы не совпадают")
    data = json.loads((ROOT / "fixtures/synthetic-audit.json").read_text())
    require(data["synthetic"] is True, "пример должен быть синтетическим")
    for key, network in [("example_ipv4", "192.0.2.0/24"), ("example_ipv6", "2001:db8::/32")]:
        require(ipaddress.ip_address(data[key]) in ipaddress.ip_network(network), "адрес вне документационного диапазона")
    require(data["example_domain"].endswith(".invalid"), "несинтетический домен")
    findings = data["findings"]
    require(len(findings) == len(IDS) and {f["check_id"] for f in findings} == IDS, "охват примера не совпадает")
    require(all(f["status"] == "unverified" and f["reason"] for f in findings), "необоснованное утверждение об успешной проверке")
    print(f"УСПЕХ: {len(REQUIRED)} обязательных документов, ссылки, {len(IDS)} ID и синтетический пример; без сети")


if __name__ == "__main__":
    main()
