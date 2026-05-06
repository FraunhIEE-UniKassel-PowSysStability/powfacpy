Module powfacpy.applications.pandapower_interface
=================================================
Interface with pandapower.
Tutorial on internal data structure and matrices of pandapower: https://github.com/e2nIEE/pandapower/blob/develop/tutorials/internal_datastructure.ipynb

Functions
---------

`rearrange_matrix_rows_and_cols(matrix: <class 'collections.abc.Buffer'> | numpy._typing._array_like._SupportsArray[numpy.dtype[typing.Any]] | numpy._typing._nested_sequence._NestedSequence[numpy._typing._array_like._SupportsArray[numpy.dtype[typing.Any]]] | complex | bytes | str | numpy._typing._nested_sequence._NestedSequence[complex | bytes | str], index_order: <class 'collections.abc.Buffer'> | numpy._typing._array_like._SupportsArray[numpy.dtype[typing.Any]] | numpy._typing._nested_sequence._NestedSequence[numpy._typing._array_like._SupportsArray[numpy.dtype[typing.Any]]] | complex | bytes | str | numpy._typing._nested_sequence._NestedSequence[complex | bytes | str]) ‑> <built-in function array>`
:   

Classes
-------

`PandapowerInterface(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when only one project stays active)
    - or ActiveProject (recommended when the active project may change)

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Methods

    `get_Bbus_matrix(self, net: pandapower.auxiliary.pandapowerNet, return_deepcopy=True) ‑> numpy.matrix`
    :   Get Bbus matrix  (sparse) used for dc power flow.
        
        If internal bus-branch model for dc power flow does not exist yet, a dc power flow must be executed.
        
        Arguments:
        - net: pandapower network

    `get_Ybus_frame(self, net: pandapower.auxiliary.pandapowerNet) ‑> pandas.core.frame.DataFrame`
    :   Get Dataframe with admittance matrix and row (column) labels according to the 'loc_name' of the terminal objects.
        
        Args:
            net (pp.pandapowerNet): pandapower dataset (exported from PF)
        
        Returns:
            pd.DataFrame: admittance matrix

    `get_Ybus_matrix(self, net: pandapower.auxiliary.pandapowerNet, return_deepcopy=True) ‑> numpy.matrix`
    :   Get admittance matrix (sparse).
        
        If internal bus-branch model does not exist yet, a power flow must be executed.
        
        Arguments:
            net: pandapower network
            return_deepcopy: If True, a deepcopy of the matrix stored in 'net' is returned.
        
        Returns:
            np.matrix: admittance matrix

    `get_admittance_matrix_labels(self, net: pandapower.auxiliary.pandapowerNet)`
    :

    `get_connectivity_frame(self, net: pandapower.auxiliary.pandapowerNet, boolean: bool = False) ‑> pandas.core.frame.DataFrame`
    :

    `get_connectivity_matrix(self, net: pandapower.auxiliary.pandapowerNet, boolean: bool = False) ‑> <built-in function array>`
    :   Get the connectivity (also called adjacency) matrix.
        
        Indices of connected nodes are True. The connectivity matrix is the admittance matrix where nonzero entries are True, other entries are False.
        
        Args:
            net (pp.pandapowerNet): pandapower dataset
        
        Returns:
            np.array[bool]: Connectivity matrix.

    `get_difference_between_pf_and_pandapower_dataset(self, net: pandapower.auxiliary.pandapowerNet) ‑> pandas.core.frame.DataFrame | None`
    :   Get difference between pandapower dataset (exported from PF) and the original PF.
        
        Assumes default settings for units in the PF project (see Settings/Units). Note that only a small subset of classes and parameters is checked (see 'get_pandapower_2_pf_parameter_mapping' and 'get_pandapower_2_pf_class_mapping')
        
        Args:
            net (pp.auxiliary.pandapowerNet): pandapower dataset (exported from PF)
        
        Returns:
            pd.DataFrame | None: Dataframe with differences. None if there are no differences

    `get_imaginary_Ybus_matrix(self, net: pandapower.auxiliary.pandapowerNet, return_deepcopy=True) ‑> numpy.matrix`
    :   Get imaginary part of admittance matrix (sparse).
        
        Args:
            net (pp.pandapowerNet): pandapower dataset (exported from PF)
            return_deepcopy (bool, optional): _description_. Defaults to True.
        
        Returns:
            np.matrix: imaginary part of admittance matrix (sparse)

    `get_jacobian_matrix(self, net: pandapower.auxiliary.pandapowerNet, return_deepcopy=True) ‑> numpy.matrix`
    :   Get load flow jacobian matrix.
        
        Arguments:
        - net: pandapower network

    `get_pandapower_2_pf_class_mapping(self) ‑> dict[str, list[str]]`
    :   Get mapping between pandapower classes (components) and PowerFactory classes.
        
        Returns:
            dict[str, list[str]]: Mapping. Note that the values are lists because one pandapower class can have multiple corresponding pf classes.

    `get_pandapower_2_pf_parameter_mapping(self) ‑> dict[str, dict[str, str | Callable]]`
    :   Get parameter mapping between pandapower and PowerFactory.
        
        Only a small subset of all the parameters is currently implemented.
        
        Returns:
            dict[str, dict[str, str | Callable]]: For each pf class, a mapping between the pandapower and the pf parameter is provided. The pf parameter can be a string or a callable (input is the pf object; used for example to access a parameter of the type).

    `pf_project_to_pandapower(self, project_path_in_user: str = None, json_path: str = None) ‑> pandapower.auxiliary.pandapowerNet`
    :   Convert PowerFactory network to pandapower format.
        
        see pandapower docs: https://pandapower.readthedocs.io//en//v2.13.1//converter//powerfactory.html
        
        The method 'from_pfd' that is used deactivates the currently active PF project, so it is reactivated.
        
        Arguments:
            project_path_in_user (str): path of the project in PowerFactory database relative to user
        
            json_path (str): path of exported pandapower json file
        
        Returns:
            pp.auxiliary.pandapowerNet: pandapower network

    `rearrange_Ybus_frame(self, y_bus: pandas.core.frame.DataFrame, bus_objs: powfacpy.pf_classes.protocols.ElmTerm) ‑> pandas.core.frame.DataFrame`
    :   Rearrange admittance matrix dataframe in order of 'bus_obj'.
        
        Args:
            y_bus (pd.DataFrame): Admittance matrix frame (labels are terminal names)
            bus_objs (ElmTerm): Terminals in new order.
        
        Returns:
            pd.DataFrame: Rearranged admittance matrix frame.