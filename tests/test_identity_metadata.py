import json
from pathlib import Path
import subprocess
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class IdentityMetadataTests(unittest.TestCase):
    def test_catalog_entry_renders_the_connectors_path_based_did(self):
        entry = json.loads((ROOT / "application-catalog-entry.json").read_text())
        for tenant in ("research", "lab-two"):
            with self.subTest(tenant=tenant):
                host = f"{tenant}.example.org"
                values = entry["helm_values"].replace("{tenant_host}", host).replace("{tenant}", tenant)
                expected = f"did:web:dil-connector.{host}:identity"
                self.assertEqual(yaml.safe_load(values)["catalog"]["participantId"], expected)
                rendered = subprocess.run(
                    ["helm", "template", "gui", str(ROOT), "--values", "-"],
                    input=values, capture_output=True, text=True, check=True,
                )
                config = next(document for document in yaml.safe_load_all(rendered.stdout)
                    if document and document.get("kind") == "ConfigMap"
                    and document["metadata"]["name"] == "dil-connector-gui-config")
                self.assertEqual(config["data"]["CATALOG_PARTICIPANT_ID"], expected)
                self.assertEqual(config["data"]["CONNECTOR_PUBLIC_BASE_URL"], f"https://dil-connector.{host}")

    def test_chart_fallback_uses_the_same_identity_path(self):
        rendered = subprocess.run(
            ["helm", "template", "gui", str(ROOT), "--set", "connector.publicHost=connector.example.org",
             "--set", "catalog.participantId="],
            capture_output=True, text=True, check=True,
        )
        config = next(document for document in yaml.safe_load_all(rendered.stdout)
            if document and document.get("kind") == "ConfigMap"
            and document["metadata"]["name"] == "dil-connector-gui-config")
        self.assertEqual(config["data"]["CATALOG_PARTICIPANT_ID"], "did:web:connector.example.org:identity")
