"""Tests for powfacpy.applications.database (Database, DatabaseDict).

Runs against the 39-bus project with DER templates ('39_bus_with_der'): synchronous
machines, terminals and composite models with DSL models.
"""

from types import SimpleNamespace

import pandas as pd
import pytest

from powfacpy.applications.database import Database, DatabaseDict

NETWORK_DATA = r"Network Model\Network Data"


@pytest.fixture(scope="module")
def database(pf_app, copy_39_bus_with_der_test_project) -> Database:
    copy_39_bus_with_der_test_project.Activate()
    return Database(pf_app)


@pytest.fixture
def machine(database: Database):
    return database.act_prj.get_calc_relevant_obj("*.ElmSym")[0]


@pytest.fixture
def terminal(database: Database):
    return database.act_prj.get_calc_relevant_obj("*.ElmTerm")[0]


def _path_in_project(database: Database, obj) -> str:
    return database.act_prj.get_path_of_object_in_active_project(obj)


# --------------------------------------------------------------------------- #
# get_object_attributes
# --------------------------------------------------------------------------- #


def test_get_object_attributes_without_class_attributes_returns_only_keys(
    database: Database, machine
):
    assert database.get_object_attributes([machine]) == {machine: {}}


def test_get_object_attributes_uses_class_specific_and_wildcard_attributes(
    database: Database, machine, terminal
):
    class_attributes = {"*": ["loc_name"], "ElmSym": ["outserv", "typ_id"]}
    result = database.get_object_attributes([machine, terminal], class_attributes)
    assert result[machine]["loc_name"] == machine.loc_name
    assert result[machine]["outserv"] == machine.outserv
    assert result[machine]["typ_id"] == machine.typ_id  # PF object by default
    assert result[terminal] == {"loc_name": terminal.loc_name}


def test_get_object_attributes_object_values_as_paths(database: Database, machine):
    result = database.get_object_attributes(
        [machine], {"ElmSym": ["typ_id"]}, values_are_pf_obj=False
    )
    type_path = result[machine]["typ_id"]
    assert isinstance(type_path, str)
    assert type_path.endswith(".TypSym")


def test_get_object_attributes_follows_dotted_attributes(database: Database, machine):
    result = database.get_object_attributes(
        [machine], {"ElmSym": ["bus1.cterm", "bus1.cterm.loc_name"]}
    )
    assert result[machine]["bus1.cterm"] == machine.bus1.cterm
    assert result[machine]["bus1.cterm.loc_name"] == machine.bus1.cterm.loc_name


def test_get_object_attributes_with_path_keys_and_truncated_path(
    database: Database, machine
):
    full_key = next(
        iter(database.get_object_attributes([machine], keys_are_pf_obj=False))
    )
    assert full_key == database.act_prj.get_path_of_obj_with_class_names(machine)
    truncated_key = next(
        iter(
            database.get_object_attributes(
                [machine], keys_are_pf_obj=False, truncated_path=NETWORK_DATA
            )
        )
    )
    assert truncated_key == f"Grid.ElmNet\\{machine.loc_name}.ElmSym"


# --------------------------------------------------------------------------- #
# set_pf_obj_attribute_values
# --------------------------------------------------------------------------- #


def test_set_attribute_values_with_object_keys(database: Database, terminal):
    original = terminal.uknom
    database.set_pf_obj_attribute_values({terminal: {"uknom": original + 1.0}})
    assert terminal.uknom == pytest.approx(original + 1.0)
    database.set_pf_obj_attribute_values({terminal: {"uknom": original}})
    assert terminal.uknom == pytest.approx(original)


def test_set_attribute_values_with_string_attribute(database: Database, terminal):
    """Plain strings must be written as strings, not looked up as object paths."""
    name = terminal.loc_name
    database.set_pf_obj_attribute_values({terminal: {"loc_name": name + "_renamed"}})
    assert terminal.loc_name == name + "_renamed"
    database.set_pf_obj_attribute_values({terminal: {"loc_name": name}})
    assert terminal.loc_name == name


def test_set_attribute_values_with_path_keys_and_added_path(
    database: Database, terminal
):
    original = terminal.uknom
    full_path = _path_in_project(database, terminal)
    database.set_pf_obj_attribute_values({full_path: {"uknom": original + 2.0}})
    assert terminal.uknom == pytest.approx(original + 2.0)

    relative = full_path.removeprefix(NETWORK_DATA + "\\")
    database.set_pf_obj_attribute_values(
        {relative: {"uknom": original}}, added_path=NETWORK_DATA
    )
    assert terminal.uknom == pytest.approx(original)


def test_set_attribute_values_with_tuple_keys(database: Database, terminal):
    original = terminal.uknom
    database.set_pf_obj_attribute_values({(terminal, "uknom"): original + 3.0})
    assert terminal.uknom == pytest.approx(original + 3.0)
    database.set_pf_obj_attribute_values({(terminal, "uknom"): original})


def test_set_attribute_values_resolves_object_paths_in_values(
    database: Database, machine
):
    machine_type = machine.typ_id
    type_path = _path_in_project(database, machine_type)
    database.set_pf_obj_attribute_values({machine: {"typ_id": type_path}})
    assert machine.typ_id == machine_type


def test_set_attribute_values_through_dotted_attribute(database: Database, machine):
    terminal = machine.bus1.cterm
    original = terminal.uknom
    database.set_pf_obj_attribute_values(
        {machine: {"bus1.cterm.uknom": original + 4.0}}
    )
    assert terminal.uknom == pytest.approx(original + 4.0)
    database.set_pf_obj_attribute_values({machine: {"bus1.cterm.uknom": original}})


def test_get_then_set_roundtrip(database: Database, machine):
    attributes = {"ElmSym": ["outserv", "typ_id", "bus1.cterm.loc_name"]}
    data = database.get_object_attributes([machine], attributes)
    database.set_pf_obj_attribute_values(data)
    assert database.get_object_attributes([machine], attributes) == data


# --------------------------------------------------------------------------- #
# names and classes
# --------------------------------------------------------------------------- #


def _fake_terminals(*names):
    return [
        SimpleNamespace(loc_name=name, GetClassName=lambda: "ElmTerm") for name in names
    ]


def test_make_loc_name_unique_numbers_duplicates_with_suffix():
    objs = _fake_terminals("A", "A", "B", "A")
    database = Database.__new__(Database)  # no PowerFactory needed for explicit objs
    counts = database.make_loc_name_unique(objs=objs)
    assert [o.loc_name for o in objs] == ["A", "A_2", "B", "A_3"]
    assert counts == {"A.ElmTerm": 3, "B.ElmTerm": 1}


def test_make_loc_name_unique_with_custom_separator():
    objs = _fake_terminals("A", "A")
    Database.__new__(Database).make_loc_name_unique(objs=objs, suffix_separator="#")
    assert [o.loc_name for o in objs] == ["A", "A#2"]


def test_make_loc_name_unique_of_calc_relevant_objects(database: Database):
    counts = database.make_loc_name_unique(pf_classes=["ElmSym"])
    assert counts  # there are synchronous machines
    assert set(counts.values()) == {1}  # loc_names are unique in the test project


def test_get_class_names_matches_wildcards(database: Database):
    assert "ElmSym" in database.get_class_names("ElmSy*")
    assert database.get_class_names("ElmSym") == ["ElmSym"]
    assert database.get_class_names("ThisClassDoesNotExist*") == []
    assert len(database.get_class_names()) > 100


# --------------------------------------------------------------------------- #
# result variables
# --------------------------------------------------------------------------- #


@pytest.fixture
def load_flow_results(database: Database):
    assert database.act_prj.execute_load_flow() == 0


def test_get_result_variables_of_class(database: Database, load_flow_results):
    df = database.get_result_variables("ElmTerm", ["m_u", "m_phiu"], "LF_Bal")
    terminals = database.act_prj.get_calc_relevant_obj("*.ElmTerm")
    assert list(df.index) == [t.loc_name for t in terminals]
    assert isinstance(df.columns, pd.MultiIndex)
    assert [c[0] for c in df.columns] == ["m:u", "m:phiu"]
    assert all(desc for _, desc in df.columns)  # descriptions from the enum docstrings
    assert df[df.columns[0]].dropna().between(0.8, 1.2).all()


def test_get_result_variables_with_pattern_and_object_selection(
    database: Database, load_flow_results, terminal
):
    df = database.get_result_variables(
        "ElmTerm", "m:u*", "LF_Bal", objs=[terminal], index_format="obj"
    )
    assert list(df.index) == [terminal]
    variables = [c[0] for c in df.columns]
    assert "m:u" in variables and "m:u1" in variables
    assert all(v.startswith("m:u") for v in variables)


def test_get_result_variables_index_formats(
    database: Database, load_flow_results, terminal
):
    by_path = database.get_result_variables(
        "ElmTerm", ["m_u"], "LF_Bal", objs=[terminal], index_format="path"
    )
    assert list(by_path.index) == [_path_in_project(database, terminal)]
    by_name = database.get_result_variables(
        "ElmTerm", ["m_u"], "LF_Bal", objs=[terminal]
    )
    assert list(by_name.index) == [terminal.loc_name]


# --------------------------------------------------------------------------- #
# composite models
# --------------------------------------------------------------------------- #

COMPOSITE = "control_ST_Coal_01"


def _composite(database: Database):
    return database.act_prj.get_unique_obj(
        f"{COMPOSITE}.ElmComp",
        parent_folder=database.act_prj.network_data_folder,
        include_subfolders=True,
    )


def test_get_composite_model_parameters_by_name(database: Database):
    parameters = database.get_composite_model_parameters()
    assert COMPOSITE in parameters
    governor = parameters[COMPOSITE]["governor"]
    assert governor["K"] == pytest.approx(25.0)
    assert all(isinstance(v, float) for v in governor.values())


def test_get_composite_model_parameters_key_formats(database: Database):
    comp = _composite(database)
    by_obj = database.get_composite_model_parameters([comp], obj_format="obj")
    assert list(by_obj) == [comp]
    assert all(not isinstance(k, str) for k in by_obj[comp])
    comp_path = _path_in_project(database, comp)
    by_path = database.get_composite_model_parameters([comp], obj_format="path")
    assert list(by_path) == [comp_path]
    assert all("\\" in k for k in by_path[comp_path])


@pytest.mark.parametrize("obj_format", ["obj", "path"])
def test_set_composite_model_parameters_roundtrip(database: Database, obj_format: str):
    comp = _composite(database)
    parameters = database.get_composite_model_parameters([comp], obj_format=obj_format)
    (comp_key,) = parameters
    governor_key = next(k for k in parameters[comp_key] if "governor" in str(k))
    original = parameters[comp_key][governor_key]["K"]

    def stored_value():
        current = database.get_composite_model_parameters([comp], obj_format=obj_format)
        return current[comp_key][governor_key]["K"]

    parameters[comp_key][governor_key]["K"] = original + 1.0
    database.set_composite_model_parameters(parameters)
    assert stored_value() == pytest.approx(original + 1.0)
    parameters[comp_key][governor_key]["K"] = original
    database.set_composite_model_parameters(parameters)
    assert stored_value() == pytest.approx(original)


# --------------------------------------------------------------------------- #
# DatabaseDict
# --------------------------------------------------------------------------- #


@pytest.fixture
def database_dict(pf_app, database: Database, terminal) -> DatabaseDict:
    attributes = {"uknom": terminal.uknom, "loc_name": terminal.loc_name}
    return DatabaseDict({terminal: attributes}, pf_app)


def test_database_dict_is_a_dict_and_reset_replaces_content(
    database_dict: DatabaseDict,
):
    assert isinstance(database_dict, dict)
    database_dict.reset({"a": {"x": 1}})
    assert dict(database_dict) == {"a": {"x": 1}}


def test_obj_to_str_converts_keys_to_paths(
    database_dict: DatabaseDict, terminal, database
):
    expected = _path_in_project(database, terminal)
    converted = database_dict.obj_to_str()
    assert list(converted) == [expected]
    assert list(database_dict) == [terminal]  # not in place
    prefix = NETWORK_DATA + "\\"
    truncated = database_dict.obj_to_str(truncate=prefix)
    assert list(truncated) == [expected.removeprefix(prefix)]
    database_dict.obj_to_str(inplace=True)
    assert list(database_dict) == [expected]


def test_keys_to_obj_attr_str(database_dict: DatabaseDict, terminal, database):
    path = _path_in_project(database, terminal)
    converted = database_dict.keys_to_obj_attr_str()
    assert isinstance(converted, DatabaseDict)
    assert set(converted) == {path + "\\uknom", path + "\\loc_name"}
    assert converted[path + "\\loc_name"] == terminal.loc_name
    database_dict.keys_to_obj_attr_str(inplace=True)
    assert set(database_dict) == set(converted)


def test_get_obj_attribute_strings(database_dict: DatabaseDict, terminal, database):
    path = _path_in_project(database, terminal)
    assert sorted(database_dict.get_obj_attribute_strings()) == sorted(
        [path + "\\uknom", path + "\\loc_name"]
    )


def test_set_values_of_dict_assigns_values_in_key_order(pf_app):
    dbd = DatabaseDict({"obj_a": {"x": 0, "y": 0}, "obj_b": {"z": 0}}, pf_app)
    dbd.set_values_of_dict([1, 2, 3])
    assert dbd == {"obj_a": {"x": 1, "y": 2}, "obj_b": {"z": 3}}


def test_set_values_of_dict_in_pf(database_dict: DatabaseDict, terminal):
    original = terminal.uknom
    database_dict[terminal]["uknom"] = original + 5.0
    database_dict.set_values_of_dict_in_pf()
    assert terminal.uknom == pytest.approx(original + 5.0)
    database_dict[terminal]["uknom"] = original
    database_dict.set_values_of_dict_in_pf()


def test_set_values_of_dict_in_pf_and_store_original(
    database_dict: DatabaseDict, terminal
):
    original = terminal.uknom
    database_dict[terminal]["uknom"] = original + 6.0
    database_dict.set_values_of_dict_in_pf_and_store_original()
    assert terminal.uknom == pytest.approx(original + 6.0)
    assert database_dict[terminal]["uknom"] == pytest.approx(original)  # stored
    database_dict.set_values_of_dict_in_pf()  # restores the original value
    assert terminal.uknom == pytest.approx(original)


def test_set_pf_obj_values_with_tuple_keys(pf_app, terminal):
    original = terminal.uknom
    dbd = DatabaseDict({(terminal, "uknom"): original}, pf_app)
    dbd.set_pf_obj_values([original + 7.0])
    assert terminal.uknom == pytest.approx(original + 7.0)
    dbd.set_pf_obj_values([original])
    assert terminal.uknom == pytest.approx(original)
