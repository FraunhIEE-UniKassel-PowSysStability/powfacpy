Module powfacpy.pf_classes.elm.file
===================================

Classes
-------

`MeasurementFile(obj: ElmFile)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic

    ### Static methods

    `get_full_path_of_elmfile_data_in_external_data_directory() ‑> str`
    :   Get full path of directory where elmfile data are stored (in PF's exteral working directory)
        
        Returns:
            str: path

    `get_path_of_elmfile_data_inside_external_data_directory() ‑> str`
    :   Path inside (i.e. relative to) external data directory of PF where Elmfile data are stored.
        
        Returns:
            str: path

    `insert_row_with_number_of_columns_in_csv_file(file_path: str) ‑> int`
    :   Gets the number of columns of the first row in a csv file and
        inserts a row (first row) with this number in the first column.
        This is needed for ElmFile to read csv files.

    `replace_headers_of_csv_file_with_number_of_colums(file_path: str) ‑> int`
    :   Replaces the first row (headers) of a csv file with its number of
        columns. This is needed for import of csv files to PF using ElmFile.

    ### Methods

    `from_pandas_dataframe(self, dataframe: pd.DataFrame, csv_file_name: str, csv_file_dir: str | None = None) ‑> str`
    :   Read data from a pandas dataframe.
        
        A csv file is created from the dataframe and the measurement file reads from the csv file.
        
        Args:
            dataframe (pd.DataFrame): Data for measurement file. IMPORTANT: The index of the frame is the time.
        
            csv_file_name (str): Name of csv file (created using the dataframe) from which the measurement file reads.
        
            csv_file_dir (str | None, optional): directory where csv file is created. Must have write access. Defaults to None (external data directory of PF is used, see Settings\Project Settings).
        
        Returns:
            str: Directory where csv file was created