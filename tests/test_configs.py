from pathlib import Path

import yaml

CONFIGS_DIR = Path(__file__).resolve().parent.parent / "configs"


def test_pipeline_yaml_parses():
    data = yaml.safe_load((CONFIGS_DIR / "pipeline.yaml").read_text())
    assert "variables" in data
    assert len(data["variables"]) == 7


def test_rules_yaml_parses():
    data = yaml.safe_load((CONFIGS_DIR / "rules.yaml").read_text())
    assert "reglas" in data
    assert isinstance(data["reglas"], list)
