import pytest

from analisis.analizar_experimento import holm, p_bootstrap
import numpy as np


def test_holm_ajusta_en_orden_creciente():
    aj = holm({"a": 0.01, "b": 0.04})
    assert aj["a"] == pytest.approx(0.02)
    assert aj["b"] == pytest.approx(0.04)


def test_holm_no_supera_uno():
    assert holm({"a": 0.9, "b": 0.8})["a"] == 1.0


def test_p_bootstrap_centrado_en_cero_da_p_grande():
    d = np.array([-1.0, 1.0, -1.0, 1.0])
    boot = np.array([-0.5, 0.5, -0.2, 0.2])
    assert p_bootstrap(d, boot) == pytest.approx(1.0)
