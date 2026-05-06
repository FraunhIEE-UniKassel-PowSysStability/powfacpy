Module powfacpy.base.string_manipulation
========================================

Classes
-------

`PFStringManipulation()`
:   Class to manipulate strings in the PF context.

    ### Static methods

    `format_full_path(path: str, pf_app: powfacpy.pf_classes.protocols.PFApp) ‑> str`
    :   Takes the full path (including user and project) and returns the path relative to the currently active project. Deletes class information.
        
        Examples:
            ```
            input path:  \username.IntUser\powfacpy_base.IntPrj\Network Model.IntPrjfolder\Network Data.IntPrjfolder\Grid.ElmNet\Terminal 1.ElmTerm
            output: Network Model\Network Data\Grid\Terminal 1
            ```

    `format_variable_name(name: str) ‑> str`
    :   Takes PF-generated csv export variable name and returns shortened version.
        Example:
          name: 's:u0 in kV'
          output: 's:u0'

    `handle_path(path: str)`
    :   Checks if path starts with '\' (not accepted by most PF methods)
        and if 'path' is of type string.

    `remove_class_names(path: str) ‑> str`
    :

    `remove_closing_html_tag_from_path(path: str) ‑> str`
    :

    `remove_html_tags_from_path(path: str) ‑> str`
    :

    `remove_opening_html_tag_from_path(path: str) ‑> str`
    :

    `replace_between_characters(char1: str, char2: str, replacement: str, original: str)`
    :   Replace between 'char1' and 'char2' in 'original' with 'replacement'.
        
        Example:
          Calling
            PFStringManipulation.replace_between_characters(
              '.',
              '\',
              '\',
              'username.IntUser\pow.facpy.\powfacpy.tests.IntPrj\Network Model.IntPrjfolder\Network Data.IntPrjfolder\test_base_interface\Grid.ElmNet\Terminal HV 1.ElmTerm'
          would give the output:
            'username\pow.facpy\powfacpy.tests\Network Model\Network Data\test_base_interface\Grid\Terminal HV 1'
          Note the behavior when there are several '.' in between '\'
          -> then the replacement starts after the last '.'

    `replace_outside_or_inside_of_strings_in_a_string(string: str, replacements: dict, outside=True)`
    :   This method replaces parts of a string but only in the sections
        of the original string that are either outside of strings.
        
        Example:
        "p HV load >= 2 and 'This is a string inside the string'"
        In this string the part 'This is a string inside the string'
        is a string inside the original string and no replacements are
        made in this part.
        
        Args:
            string: The string that will be adjusted
        
            replacements: key-value pairs of matching strings and their replacement

    `split_but_keep_delimiter(string: str, delimiter: str)`
    :   Uses the split() method to separate a string acoording
        to a delimiter, but keeps the delimiter in the
        separated strings (it is suprising that this is not optional
        in the split() method).
        Example:
          split_but_keep_delimiter(
            "p HV load >= 2 and (control 1 == 'A' and control 2 != 'S')",
            delimiter: "'")
          returns
            ["p HV load >= 2 and (control 1 == '", "A'", " and control 2 != '", "S'", ')']

    `truncate_beginning(original: str, string_pattern: str) ‑> str`
    :   Truncate string_pattern if it occurs at the beginning of the
        original string. Otherwise return original string.

    `truncate_until(original: str, string_pattern: str) ‑> str`
    :   Truncate all characters until (and including) the occurence of string_pattern in original.

`PFTranslator()`
:   Class to translate between languages.
    Currently not used anywhere in powfacpy any more.

    ### Static methods

    `get_default_graphics_board_name(language)`
    :

    `get_default_operation_scenario_folder_path(language)`
    :

    `get_default_result_object_name(language)`
    :

    `get_default_study_case_folder_name(language)`
    :

    `get_default_variations_folder_path(language)`
    :

    `get_graphics_board_name_from_studycase(studycase)`
    :

    `get_name_with_ending(objects)`
    :

    `get_result_object_name_from_studycase(studycase)`
    :