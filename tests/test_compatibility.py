"""Verify the old spelling continues to expose the exact same numerical library."""
import importlib
import numpy as np
import bradiant
import braidiant

def test_compatibility_core_objects_are_identical():
    assert bradiant.FusionModel is braidiant.FusionModel
    assert bradiant.audit is braidiant.audit
    assert bradiant.__version__ == braidiant.__version__

def test_legacy_submodule_alias():
    legacy = importlib.import_module('braidiant.models')
    assert legacy.fibonacci().charges == bradiant.fibonacci().charges

def test_bradiant_numerical_api():
    m = bradiant.fibonacci()
    rep = bradiant.BraidRepresentation(m,'tau',4,'1')
    assert bradiant.audit(m).passed
    assert np.max(np.abs(rep.generator(1))) <= 1.0 + 1e-12
