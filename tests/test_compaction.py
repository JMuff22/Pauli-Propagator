# %%

from pprop import Propagator #noqa
import pytest

from test_k2_mode import layered_ansatz

# %%
# PPROP_RS_COMPACT_EVERY_LAYER makes pprop_rs rebuild its monomial arenas
# after every layer; the result must not depend on when that happens.
@pytest.mark.parametrize("k2_mode", ["frequency", "sine"])
def test_compaction_keeps_exprs(monkeypatch, k2_mode):
    for n_threads in (1, 4):
        prop = Propagator(layered_ansatz, k2=4, k2_mode=k2_mode)
        prop.propagate(n_threads=n_threads)
        monkeypatch.setenv("PPROP_RS_COMPACT_EVERY_LAYER", "1")
        compacted = Propagator(layered_ansatz, k2=4, k2_mode=k2_mode)
        compacted.propagate(n_threads=n_threads)
        monkeypatch.delenv("PPROP_RS_COMPACT_EVERY_LAYER")
        assert compacted.exprs == prop.exprs
