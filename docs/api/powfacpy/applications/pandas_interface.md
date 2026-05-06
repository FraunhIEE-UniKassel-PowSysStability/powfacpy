Module powfacpy.applications.pandas_interface
=============================================
Interface to pandas package.

Classes
-------

`PandasInterface(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when only one project stays active)
    - or ActiveProject (recommended when the active project may change)

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Static methods

    `separate_complex_columns_into_real_and_imaginary(df: pandas.core.frame.DataFrame, real_suffix: str = '_real', imag_suffix: str = '_imag') ‑> pandas.core.frame.DataFrame`
    :   Separates complex columns into real and imaginary parts.
        
        Args:
            df (pd.DataFrame): DataFrame with complex columns.
            real_suffix (str, optional): Suffix for real part columns (added to original column label). Defaults to "_real".
            imag_suffix (str, optional): Suffix for imaginary part columns. Defaults to "_imag".

    ### Methods

    `replace_loc_name_with_pf_objects_in_labels(self, df: pandas.core.frame.DataFrame, class_name: str, only_calc_relevant: bool = True, index_and_column_labels_are_equal: bool = False, level: int = 0) ‑> pandas.core.frame.DataFrame`
    :   Replaces string labels ('loc_name' of PF objects) of a dataframe with the corresponding PF objects.
        
        It is assumed that all PF objects are of the same class.
        
        Args:
            df (pd.DataFrame): index and column labels are 'loc_name' attributes of PF objects
        
            class_name (str): PF class name of the labels (e.g. 'ElmTerm'). Note that all PF objects must be of the same class.
        
            only_calc_relevant (bool): Search only for calculation relevant objects (using 'GetCalcRelevantObjects'). If False, search all objects (using 'get_obj') Defaults to True.
        
            index_and_column_labels_are_equal (bool, optional): If True, it is assumed that indices and columns have the same labels (improved performance). This is common for symmetric matrices. Defaults to False.
        
            level (int, optional): If labels are MultiIndex, the level that is replaced can be specified. Defaults to 0.
        
        Returns:
            pd.DataFrame: Frame with updated labels