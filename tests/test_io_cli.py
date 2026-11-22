import json
import subprocess
import sys
import pytest
from braidiant import (audit, fibonacci, ising, cyclic, regauge,
                       model_to_dict, model_from_dict, save_model, load_model, ModelError)


@pytest.mark.parametrize("model", [fibonacci(), ising(), cyclic(3)])
def test_json_round_trip(model, tmp_path):
    path = tmp_path / "model.json"
    save_model(model, path)
    loaded = load_model(path)
    assert model_to_dict(loaded) == model_to_dict(model)
    assert audit(loaded).passed


def test_reject_duplicate_entries():
    data = model_to_dict(fibonacci())
    data["R"].append(data["R"][0])
    with pytest.raises(ModelError, match="duplicate"):
        model_from_dict(data)


def test_cli_audit(capsys):
    from braidiant.cli import main
    assert main(["--model", "ising", "audit"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["passed"] is True
    assert data["type"] == "model_audit"
    assert data["hexagon_sectors"] > 0


def test_cli_braid_json(capsys):
    from braidiant.cli import main
    assert main(["braid", "--charge", "tau", "--anyons", "4", "--total", "1",
                 "--word", "1,-2,1"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["dimension"] == 2
    assert len(data["word_matrix"]) == 2
    assert data["relations"]["yang_baxter"] < 1e-12


def test_cli_model_file(capsys, tmp_path):
    from braidiant.cli import main
    filename = tmp_path / "custom.json"
    save_model(cyclic(4), filename)
    assert main(["--model-file", str(filename), "audit"]) == 0
    assert json.loads(capsys.readouterr().out)["model"] == "Z4(k=1)"
