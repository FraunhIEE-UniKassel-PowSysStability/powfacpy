import os
import sys
import json
from pathlib import Path
import pytest

# Tests must not open plot windows (no display on CI); an explicit MPLBACKEND wins.
os.environ.setdefault("MPLBACKEND", "Agg")

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "src"))

# Most tests drive a real PowerFactory installation (see settings_local.json).
# Without it (e.g. on a CI runner) only the tests marked 'unit' are run; all
# others are skipped, see pytest_collection_modifyitems below.
try:
    with open(_REPO_ROOT / "settings_local.json") as settings_file:
        settings = json.load(settings_file)
    sys.path.append(settings["local path to PowerFactory application"])
    import powerfactory

    POWERFACTORY_AVAILABLE = True
except (OSError, KeyError, ImportError):
    settings = {}
    powerfactory = None
    POWERFACTORY_AVAILABLE = False


def pytest_collection_modifyitems(config, items):
    if POWERFACTORY_AVAILABLE:
        return
    skip_no_pf = pytest.mark.skip(
        reason="PowerFactory not available (settings_local.json or 'powerfactory' module missing)"
    )
    for item in items:
        if "unit" not in item.keywords:
            item.add_marker(skip_no_pf)


from powfacpy.base.active_project import ActiveProject
from powfacpy.pf_classes.protocols import IntPrj, PFApp


@pytest.fixture(scope="session")
def pf_app():
    if not POWERFACTORY_AVAILABLE:
        pytest.skip("PowerFactory not available")
    if settings["PowerFactory username"]:
        if settings["PowerFactory command line arguments for GetApplication"]:
            return powerfactory.GetApplicationExt(
                settings["PowerFactory username"],
                settings["PowerFactory password"],
                settings["PowerFactory command line arguments for GetApplication"],
            )
        else:
            return powerfactory.GetApplicationExt(
                settings["PowerFactory username"],
                settings["PowerFactory password"],
            )
    else:
        return powerfactory.GetApplicationExt()


@pytest.fixture(scope="session")
def act_prj(pf_app: PFApp) -> ActiveProject:
    # Return ActiveProject instance
    return ActiveProject(pf_app)


@pytest.fixture(scope="module")
def copy_test_project(act_prj: ActiveProject) -> IntPrj:
    """This method will create a copy of that project which is then used for the tests. This ensures that the tests are always run with the same initial
    project state.
    """
    return create_copy_of_test_project(act_prj, "powfacpy_tests")


@pytest.fixture(scope="module")
def copy_39_bus_new_england_test_project(act_prj: ActiveProject) -> IntPrj:
    """This method will create a copy of that project which is then used for the tests. This ensures that the tests are always run with the same initial
    project state.
    """
    return create_copy_of_test_project(act_prj, "39_bus_new_england")


@pytest.fixture(scope="module")
def copy_control_block_testing_test_project(act_prj: ActiveProject) -> IntPrj:
    """Copy of the control_block_testing project (holds the BlockDefinitionTesting
    composite frame used by powfacpy.applications.frame_test)."""
    return create_copy_of_test_project(act_prj, "control_block_testing")


@pytest.fixture(scope="module")
def copy_component_tests_test_project(act_prj: ActiveProject) -> IntPrj:
    """Copy of the component_tests project (SMIB test bench used by the dynamic
    model validation / component test interface)."""
    return create_copy_of_test_project(act_prj, "component_tests")


@pytest.fixture(scope="module")
def copy_39_bus_with_der_test_project(act_prj: ActiveProject) -> IntPrj:
    """Copy of the 39_bus_with_der project (39-bus New England with a range of
    grid-following/synchronous-machine templates from the global library applied;
    used to exercise the template-model interface)."""
    return create_copy_of_test_project(act_prj, "39_bus_with_der")


def create_copy_of_test_project(
    act_prj: ActiveProject, project_name_in_powfacpy_folder: str
) -> IntPrj:
    user = act_prj.app.GetCurrentUser()
    powfacpy_folder_path = settings["path to powfacpy folder in PowerFactory database"]
    project_for_testing = act_prj.get_unique_obj(
        rf"{powfacpy_folder_path}\{project_name_in_powfacpy_folder}",
        parent_folder=user,
        include_subfolders=False,
    )
    folder_of_project_for_testing = act_prj.get_unique_obj(
        powfacpy_folder_path, parent_folder=user, include_subfolders=False
    )
    project_copy = act_prj.copy_single_obj(
        project_for_testing,
        folder_of_project_for_testing,
        new_name=f"{project_name_in_powfacpy_folder}_copy_to_run_tests",
    )
    return project_copy


@pytest.fixture(scope="function")
def activate_powfacpy_test_project(
    copy_test_project: IntPrj, act_prj: ActiveProject
) -> IntPrj:
    """The project for testing must be located in the current
    user under "powfacpy\\powfacpy_tests".
    """
    # ap = act_prj.app.GetActiveProject()
    # if ap is None:
    copy_test_project.Activate()
    # if not ap == copy_test_project:
    #     ap.Deactivate()
    #     copy_test_project.Activate()
    # assert act_prj.app.GetActiveProject() == copy_test_project
    return copy_test_project


@pytest.fixture(scope="function")
def activate_39_bus_new_england_test_project(
    copy_39_bus_new_england_test_project: IntPrj,
) -> IntPrj:
    """The project for testing must be located in the current
    user under "powfacpy\\powfacpy_tests".
    """
    copy_39_bus_new_england_test_project.Activate()
    return copy_39_bus_new_england_test_project


@pytest.fixture(scope="function")
def activate_control_block_testing_test_project(
    copy_control_block_testing_test_project: IntPrj,
) -> IntPrj:
    copy_control_block_testing_test_project.Activate()
    return copy_control_block_testing_test_project


@pytest.fixture(scope="function")
def activate_component_tests_test_project(
    copy_component_tests_test_project: IntPrj,
) -> IntPrj:
    """Activate the component_tests copy and return it (function-scoped)."""
    copy_component_tests_test_project.Activate()
    return copy_component_tests_test_project


@pytest.fixture(scope="function")
def activate_39_bus_with_der_test_project(
    copy_39_bus_with_der_test_project: IntPrj,
) -> IntPrj:
    """Activate the 39_bus_with_der copy and return it (function-scoped)."""
    copy_39_bus_with_der_test_project.Activate()
    return copy_39_bus_with_der_test_project
