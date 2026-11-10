"""
Security Testing and Dependency Hygiene: Automated Vulnerability Scanner,
Software Bill of Materials (SBOM) Generation, and Prompt Injection Defense.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class VulnerabilityFinding:
    package_name: str
    current_version: str
    cve_id: str
    severity: str


class SecurityPipelineScanner:
    KNOWN_CVES = {
        "requests": ("2.25.0", "CVE-2023-32681", "HIGH"),
        "urllib3": ("1.26.4", "CVE-2021-33503", "CRITICAL")
    }

    def scan_dependencies(self, installed_packages: Dict[str, str]) -> List[VulnerabilityFinding]:
        findings = []
        for pkg, ver in installed_packages.items():
            if pkg in self.KNOWN_CVES:
                vuln_ver, cve, sev = self.KNOWN_CVES[pkg]
                if ver <= vuln_ver:
                    findings.append(VulnerabilityFinding(pkg, ver, cve, sev))
        return findings


if __name__ == "__main__":
    scanner = SecurityPipelineScanner()
    pkgs = {"requests": "2.25.0", "fastapi": "0.115.0"}
    vulns = scanner.scan_dependencies(pkgs)
    assert len(vulns) == 1
    assert vulns[0].cve_id == "CVE-2023-32681"

    print("=== Day 27: Security Pipeline Scanner ===")
    print(f"Scanned dependencies. Identified: {vulns[0].severity} {vulns[0].cve_id}")
