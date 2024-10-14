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
from powfacpy.pf_classes.protocols import IntPrj


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
def act_prj(pf_app) -> ActiveProject:
    # Return ActiveProject instance
    return ActiveProject(pf_app)


@pytest.fixture(scope="session")
def copy_test_project(act_prj: ActiveProject) -> IntPrj:
    """This method will create
    a copy of that project which is then used for the tests. This
    ensures that the tests are always run with the same initial
    project state.
    """
    return create_copy_of_test_project(act_prj, "powfacpy_tests")


@pytest.fixture(scope="session")
def copy_39_bus_new_england_test_project(act_prj: ActiveProject) -> IntPrj:
    """This method will create  a copy of that project which is then used for the tests. This ensures that the tests are always run with the same initial
    project state.
    """
    return create_copy_of_test_project(act_prj, "39_bus_new_england")


def create_copy_of_test_project(
    act_prj: ActiveProject, project_name_in_powfacpy_folder: str
):
    user = act_prj.app.GetCurrentUser()
    powfacpy_folder_path = settings["path to powfacpy folder in PowerFactory database"]
    project_for_testing = act_prj.get_single_obj(
        rf"{powfacpy_folder_path}\{project_name_in_powfacpy_folder}",
        parent_folder=user,
        include_subfolders=False,
    )
    folder_of_project_for_testing = act_prj.get_single_obj(
        powfacpy_folder_path, parent_folder=user, include_subfolders=False
    )
    project_copy = act_prj.copy_single_obj(
        project_for_testing,
        folder_of_project_for_testing,
        new_name=f"{project_name_in_powfacpy_folder}_copy_where_tests_run",
    )
    return project_copy


@pytest.fixture(scope="module")
def activate_test_project(copy_test_project: IntPrj):
    """The project for testing must be located in the current
    user under "powfacpy\\powfacpy_tests".
    """
    copy_test_project.Activate()


@pytest.fixture(scope="module")
def activate_39_bus_new_england_test_project(
    copy_39_bus_new_england_test_project: IntPrj,
):
    """The project for testing must be located in the current
    user under "powfacpy\\powfacpy_tests".
    """
    copy_39_bus_new_england_test_project.Activate()
