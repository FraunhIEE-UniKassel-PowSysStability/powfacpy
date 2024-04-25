import powfacpy
from powfacpy.pf_class_protocols import PFApp


class PFStringManipulation:
    """Class to manipulate strings in the PF context.
    """
    
    @staticmethod
    def replace_between_characters(char1: str, 
                                   char2: str, 
                                   replacement: str, 
                                   original: str):
        """Replace between 'char1' and 'char2' in 'original' with 'replacement'.
        
        Example:
          Calling      
            powfacpy.PFStringManipulation.replace_between_characters(
              '.', 
              '\\', 
              '\\', 
              'username.IntUser\\pow.facpy.\\powfacpy.tests.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_base_interface\\Grid.ElmNet\\Terminal HV 1.ElmTerm'
          would give the output:
            'username\\pow.facpy\\powfacpy.tests\\Network Model\\Network Data\\test_base_interface\\Grid\\Terminal HV 1' 
          Note the behavior when there are several '.' in between '\\' 
          -> then the replacement starts after the last '.'
        """
        new_string = ""
        is_after_char_1 = False
        string_between_char_1_occurrences = ""
        for c in original:
            if c == char1:
                is_after_char_1 = True
                new_string += string_between_char_1_occurrences
                string_between_char_1_occurrences = ""
            elif c == char2:
                if is_after_char_1:
                    new_string += replacement
                else:
                    new_string += c
                string_between_char_1_occurrences = ""
                is_after_char_1 = False
            if is_after_char_1:
                string_between_char_1_occurrences += c
            elif not c == char2:
                new_string += c
        return new_string
    
    
    @staticmethod
    def remove_html_tags_from_path(path:str) -> str:
        return path[path.find(">")+1 : path.rfind("<")]
    
    @staticmethod
    def remove_opening_html_tag_from_path(path:str) -> str:
        return path[path.find(">")+1:]
    
    @staticmethod
    def remove_closing_html_tag_from_path(path:str) -> str:
        return path[0:path.rfind("<")]
        
    @staticmethod
    def remove_class_names(path: str) -> str:
        return PFStringManipulation.replace_between_characters('.', '\\', '\\', path)


    @staticmethod
    def truncate_until(original: str, string_pattern: str) -> str:
        """Truncate all characters until (and including) the occurence of string_pattern in original.
        """
        return original[original.find(string_pattern)+len(string_pattern):]

    @staticmethod
    def truncate_beginning(original: str, string_pattern: str) -> str:
        """Truncate string_pattern if it occurs at the beginning of the
        original string. Otherwise return original string.
        """
        index_where_pattern_begins = original.find(string_pattern)
        if index_where_pattern_begins == 0:
            return original[len(string_pattern)+1:]
        else:
            return original

    @staticmethod
    def format_full_path(path: str, pf_app: PFApp) -> str:
        """Takes the full path (including user and project) and returns the path relative to the currently active project. Deletes class information.
        Example:
          input path:  \\username.IntUser\\powfacpy_base.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\Terminal 1.ElmTerm
          output: Network Model\\Network Data\\Grid\\Terminal 1 
        """
        path = PFStringManipulation._get_path_inside_active_project_from_full_path(
            path, pf_app)
        return PFStringManipulation.remove_class_names(path)

    @staticmethod
    def format_variable_name(name: str) -> str:
        """Takes PF-generated csv export variable name and returns shortened version.
        Example:
          name: 's:u0 in kV'
          output: 's:u0' 
        """
        return name.split(" ", 1)[0].replace("\"", "").replace("\n", "")  # get rid of description and quotation marks

    @staticmethod
    def handle_path(path: str):
        """Checks if path starts with '\\' (not accepted by most PF methods)
        and if 'path' is of type string.
        """
        try:
            if not path[0] == "\\":
                return path
            else:
                return path[1:]
        except (TypeError):
            raise TypeError("Path must be of type string.")

    @staticmethod
    def replace_outside_or_inside_of_strings_in_a_string(
            string: str,
            replacements: dict,
            outside = True):
        """This method replaces parts of a string but only in the sections
        of the original string that are either outside of strings. 
        
        Example:
        "p HV load >= 2 and 'This is a string inside the string'"
        In this string the part 'This is a string inside the string'
        is a string inside the original string and no replacements are
        made in this part.

        Args:
            string: The string that will be adjusted
            
            replacements: key-value pairs of matching strings and their replacement
        """
        if outside:
            modulo_result = 0
        else:
            modulo_result = 1
        string = PFStringManipulation.split_but_keep_delimiter(string, "'")
        for n, part_of_string in enumerate(string):
            if n % 2 == modulo_result:  # Even elemnts store the parts that are outside strings
                for par_name, var_name in replacements.items():
                    part_of_string = part_of_string.replace(par_name, var_name)
                    string[n] = part_of_string
        return "".join(string).strip()

    @staticmethod
    def split_but_keep_delimiter(string: str, delimiter: str):
        """Uses the split() method to separate a string acoording
        to a delimiter, but keeps the delimiter in the
        separated strings (it is suprising that this is not optional
        in the split() method).
        Example:
          split_but_keep_delimiter(
            "p HV load >= 2 and (control 1 == 'A' and control 2 != 'S')",
            delimiter: "'")
          returns 
            ["p HV load >= 2 and (control 1 == '", "A'", " and control 2 != '", "S'", ')']
        """
        split_strings_list = [part + delimiter
                              for part in string.split(delimiter)]
        split_strings_list[-1] = split_strings_list[-1].rstrip(delimiter)
        return split_strings_list
    
    @staticmethod
    def _get_path_inside_active_project_from_full_path(path: str, 
                                                       pf_app: PFApp) -> str:
        """
        Takes the full path (including user and project) and returns the path 
        relative to the currently active project.
        Example:
          input path:  \\username.IntUser\\powfacpy_base.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\Terminal 1.ElmTerm</l3>
          output: Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\Terminal 1.ElmTerm
        """
        project_name = pf_app.GetActiveProject().loc_name + '.IntPrj\\'
        path = PFStringManipulation.truncate_until(path, project_name)
        # In case a closing tag occurs at the end of the path </l3> (e.g. when
        # str() is called on a PF object) make sure this is removed.
        if path[-1] == ">":
            path = path[0:path.rfind("<")]
        return path


class PFTranslator:
    """Class to translate between languages.
    Currently not used anywhere in powfacpy any more.
    """

    @staticmethod
    def get_default_result_object_name(language):
        if language == "en":
            return "All calculations.ElmRes"
        elif language == "de":
            return "Alle Berechnungsarten.ElmRes"

    @staticmethod
    def get_default_graphics_board_name(language):
        if language == "en":
            return "Graphics Board.SetDesktop"
        elif language == "de":
            return "Grafiksammlung.SetDesktop"

    @staticmethod
    def get_default_study_case_folder_name(language):
        if language == "en":
            return "Study Cases.IntPrjfolder"
        elif language == "de":
            return "Berechnungsfälle.IntPrjfolder"

    @staticmethod
    def get_default_operation_scenario_folder_path(language):
        if language == "en":
            return r"Network Model\Operation Scenarios"
        elif language == "de":
            return r"Netzmodell\Betriebsfälle"

    @staticmethod
    def get_default_variations_folder_path(language):
        if language == "en":
            return r"Network Model\Variations"
        elif language == "de":
            return r"Netzmodell\Varianten"

    @staticmethod
    def _get_language_dependent_name_from_studycase(
            studycase, english_name, german_name):
        studycase_contents = powfacpy.PFTranslator.\
            get_name_with_ending(
                studycase.GetContents())
        has_english_name = english_name in studycase_contents
        has_german_name = german_name in studycase_contents
        assert not (has_english_name and has_german_name), \
            'Two redundant file versions: English and German named files exist.'
        if has_english_name:
            return english_name
        else:
            return german_name

    @staticmethod
    def get_graphics_board_name_from_studycase(studycase):
        name = powfacpy.PFTranslator.\
            _get_language_dependent_name_from_studycase(
                studycase=studycase,
                english_name="Graphics Board.SetDesktop",
                german_name="Grafiksammlung.SetDesktop",
            )
        return name

    @staticmethod
    def get_result_object_name_from_studycase(studycase):
        name = powfacpy.PFTranslator.\
            _get_language_dependent_name_from_studycase(
                studycase=studycase,
                english_name="All calculations.ElmRes",
                german_name="Alle Berechnungsarten.ElmRes",
            )
        return name

    @staticmethod
    def get_name_with_ending(objects):
        if not type(objects) == list:
            objects = [objects]
        return [x.GetFullName().split('\\')[-1] for x in objects]
