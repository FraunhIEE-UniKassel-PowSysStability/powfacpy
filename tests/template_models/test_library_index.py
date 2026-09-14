"""Tests for `LibraryTemplateIndex` - detecting which global-library template an
applied composite model in a grid was built from.

Run against ``39_bus_with_der_copy_to_run_tests``: the 39-bus New England
system with a range of library templates applied (WECC Large-scale PV, WECC WT
Type 4B, and an older packed synchronous-generator template).
"""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.base.active_project import ActiveProject
from powfacpy.template_models import LibraryTemplateIndex, TemplateMatcher


@pytest.fixture(scope="module")
def der_grid(pf_app, copy_39_bus_with_der_test_project):
    """The `Grid` ElmNet of the activated 39_bus_with_der copy."""
    copy_39_bus_with_der_test_project.Activate()
    act_prj = ActiveProject(pf_app)
    return act_prj.get_unique_obj(r"Network Model\Network Data\Grid")


@pytest.fixture(scope="module")
def index(pf_app, copy_39_bus_with_der_test_project) -> LibraryTemplateIndex:
    """A `LibraryTemplateIndex` built once for the module (the 39_bus_with_der copy)."""
    copy_39_bus_with_der_test_project.Activate()
    return LibraryTemplateIndex(pf_app)


def test_index_covers_the_grid_forming_converter_templates(index):
    """The index picks up templates across the library branches, not just one."""
    paths = set().union(*index.frame_path_to_templates.values())
    assert any("Grid-forming Converters" in p for p in paths)
    assert any("Photovoltaic" in p for p in paths)


def test_detects_applied_pv_and_wind_templates(index, der_grid):
    """Applied WECC PV / WT type 4B controllers resolve to their templates by frame."""
    matches = {m.composite_model.loc_name: m for m in index.identify_in(der_grid)}
    assert matches, "no composite models found in the grid"

    pv = matches["control_PV_03"]
    assert pv
    assert pv.matched_by == "frame"
    assert all("WECC Large-scale PV Plant" in p for p in pv.template_paths)

    wind = matches["control_Gen Wind 06_stat"]
    assert wind
    assert all("WECC WTG Type4B" in p for p in wind.template_paths)


def test_packed_legacy_template_is_not_falsely_matched(index, der_grid):
    """A controller from an old packed template (frame absent from the current
    library) is reported with low confidence, not a false positive."""
    matches = {m.composite_model.loc_name: m for m in index.identify_in(der_grid)}
    sync_gen = matches["control_CC_NG_01"]
    # frame "Frame Synchronous Generator IEEE" was packed from an old PF version
    # and is not in the current library -> no confident match
    assert sync_gen.confidence < 0.5


def test_matcher_enriches_result_with_library_template_paths(
    pf_app, copy_39_bus_with_der_test_project
):
    """`TemplateMatcher(app=...)` names the library template even when no
    `TemplateModel` class matches (grid-following PV has none)."""
    copy_39_bus_with_der_test_project.Activate()
    act_prj = ActiveProject(pf_app)
    grid = act_prj.get_unique_obj(r"Network Model\Network Data\Grid")
    matcher = TemplateMatcher(app=pf_app)

    pv_comp = act_prj.get_unique_obj("control_PV_03", parent_folder=grid)
    result = matcher.identify(pv_comp)
    # no powfacpy class for WECC PV plants (grid-following) ...
    assert result.template_class is None
    # ... but the library template is still identified
    assert result.library_template_paths
    assert all(
        "WECC Large-scale PV Plant" in p for p in result.library_template_paths
    )


if __name__ == "__main__":
    pytest.main([__file__])
