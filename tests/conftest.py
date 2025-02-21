import sys
import os
import json
import pytest

with open(".\\settings.json") as settings_file:
    settings = json.load(settings_file)
sys.path.append(settings["local path to PowerFactory application"])
import powerfactory

sys.path.insert(0, r".\src")
from powfacpy.base.active_project import ActiveProject
from powfacpy.pf_classes.protocols import IntPrj, PFApp


@pytest.fixture(scope="session")
def pf_app():
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


def create_copy_of_test_project(
    act_prj: ActiveProject, project_name_in_powfacpy_folder: str
) -> IntPrj:
    user = act_prj.app.GetCurrentUser()
    powfacpy_folder_path = settings["path to powfacpy folder in PowerFactory database"]
    full_path_to_project_in_pf = [
        settings["path to powfacpy folder in PowerFactory database"], 
        project_name_in_powfacpy_folder]
    full_path_to_project_in_pf = '\\'.join([x for x in full_path_to_project_in_pf if not x is None])
    project_for_testing = act_prj.get_unique_obj(
        full_path_to_project_in_pf,
        parent_folder=user,
        include_subfolders=False,
    )
    folder_of_project_for_testing = act_prj.get_unique_obj(
        powfacpy_folder_path, parent_folder=user, include_subfolders=False
    )
    project_copy = act_prj.copy_single_obj(
        project_for_testing,
        folder_of_project_for_testing,
        new_name=f"{project_name_in_powfacpy_folder}_copy_where_tests_run",
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
