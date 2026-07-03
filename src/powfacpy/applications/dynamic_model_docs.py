""" """

from __future__ import annotations

import sys, os, shutil
from fnmatch import fnmatchcase
from typing import Callable, Iterable, Any, OrderedDict
import importlib, inspect
import copy
import markdown
from markdown.extensions.toc import slugify
from pathlib import Path

import pandas as pd
import numpy as np
from icecream import ic


from powfacpy.applications.application_base import ApplicationBase
from powfacpy.base.string_manipulation import PFStringManipulation
from powfacpy.pf_classes.protocols import ElmDsl, PFGeneral, PFApp, ElmComp
from powfacpy.pf_classes.elm.comp import CompositeModel
from powfacpy.pf_classes.blk.definition import BlockDefinition

class DynamicModelDocs(ApplicationBase):
    """Document dynamic DSL models in html (parameters, graphics, equations,..). 
    """

    @property
    def composite_model(self) -> CompositeModel:
        "Composite model (ElmComp) to be documented."
        try:
            return self._composite_model._obj
        except AttributeError:
            raise AttributeError("Attribute 'composite mode' not found. Please set.") 

    @composite_model.setter
    def composite_model(self, composite_model):
        if isinstance(composite_model, CompositeModel):
            self._composite_model = composite_model
        else:
            self._composite_model = CompositeModel(composite_model)

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self.target_directory: str = ".\\model_docs"
        "Directory where documentation will be created."
        self.file_name: str | None = None
        "File name of html file in 'target_directory'."
        self.css_file_dir: str | None = None 
        "Directory of css file to style html."
        self.include_out_of_service: bool = False
        "If True, models that are out of service are included."
        self.copy_css_file_to_html_location: bool = True
        "If True, the css file will be copied to target directory and the folder is self contained. If False, the current absolute path of the css file is referenced in the html file."
        self.block_definition_attributes = ["Title", "Output signals", "Input signals", "States", "Parameters", "Upper limitation parameters", "Lower limitation parameters", "Equations"]
        "Block defintion attributes that are referenced."
        self.all_blkdef_info = {
            "blkdefs_without_subblocks": [], 
            "blkdefs_with_subblocks": [],
        }
        "Information about all block definitions (BlkDef) in the composite frame. See 'get_info' method of the 'BlockDefinition' class. The block definitions are separated into with and without subblocks"
        self._composite_model: CompositeModel | None = None
        "Composite model object"
        self._dsl_models: list | None = None
        "DSL models of the composite model."
        self.unique_blkdef_names: dict | None = None
        "Dict that maps block definitions (BlkDef) and their names. In case different block definitions have the same name, unique names are defined ('name(1), name(2), ..') (see method '_get_unique_names_for_block_definitions'). Every block definition must have a unique name because the names are used as links in the html file."
        self._comp_model_docs: str | None = None
        "Documentation of composite model in markdown."
        self._blkdef_with_subblocks_docs: str | None = None
        "Documentation of block definitions with subblocks in markdown."
        self._blkdef_macro_docs: str | None = None
        "Documentation of block definitions without subblocks in markdown."
        

    def create_composite_model_docs(
        self, clear_target_dir: bool = False
    ) -> None:
        """Create html documentation of Composite Model (ElmComp).

        Args:
            clear_target_dir (bool, optional): If True, the target directory for the documentation will be cleared in advance. Defaults to False.
        """
        if clear_target_dir:
            if os.path.exists(self.target_directory):
                shutil.rmtree(self.target_directory)
            os.makedirs(self.target_directory)
        if self.css_file_dir is None:
            # use css file in .\styles folder in root
            module_dir = os.path.dirname(os.path.abspath(__file__))  
            self.css_file_dir = "\\".join(module_dir.split("\\")[0:-3]) + "\\" + "styles\\dynamic_model_docs.css"  
        if self.file_name is None:
            self.file_name = self.composite_model.loc_name    
        self.get_block_defintion_info_of_dsl_models()
        self._get_unique_names_for_block_definitions()
        self._create_blkdef_macro_docs()
        self._create_blkdef_graphical_docs()
        self._create_composite_model_docs()
        markdown_content = self._comp_model_docs + self._blkdef_with_subblocks_docs + self._blkdef_macro_docs
        self._create_html_from_markdown(markdown_content)


    def get_block_defintion_info_of_dsl_models(self) -> dict:
        """Get information on block definitions of DSL models. 
        
        See method 'get_info_incl_subblocks' of 'BlockDefinition' class  on more specifics. 

        Returns:
            dict: Dictionary with information on block definitions separated in to block definitions with (graphical) and without (macros) subblocks.
        """
        self.all_blkdef_info = {
            "blkdefs_without_subblocks": [], 
            "blkdefs_with_subblocks": [],
        }
        self._dsl_models = self._composite_model.get_dsl_models_in_slots()
        for dsl_model in self._dsl_models:
            if self.include_out_of_service == False and dsl_model.outserv == 1:
                continue
            blkdef = BlockDefinition(dsl_model.typ_id)
            self.all_blkdef_info = blkdef.get_info_incl_subblocks(all_blkdef_info=self.all_blkdef_info)
        self.all_blkdef_info["blkdefs_without_subblocks"].sort(key=lambda x: x["BlkDef"].loc_name)
        return self.all_blkdef_info
    
    def _get_unique_names_for_block_definitions(self) -> None:
        """Get dict that maps block definitions (BlkDef) and their names. 
        
        In case different block definitions have the same name, unique names are defined ('name(1), name(2), ..'). Every block definition must have a unique name because the names are used as links in the html file. 
        """
        self._unique_blkdef_names = {}
        for all_info in [self.all_blkdef_info["blkdefs_without_subblocks"], self.all_blkdef_info["blkdefs_with_subblocks"]]:
            for blkdef_info in all_info:
                name = blkdef_info["Name"]
                n = 1
                while name in self._unique_blkdef_names.values():
                    name = blkdef_info["Name"] + f"({n})"
                    n += 1
                self._unique_blkdef_names[blkdef_info["BlkDef"]] = name 

    def _create_blkdef_macro_docs(self) -> None:
        """Create markdown documentation for block definitions that have no subblocks (without graphical representation, also called macros).
        """
        self._blkdef_macro_docs = "# Block Definitions (Macros)\n\n"
        for blkdef_info in self.all_blkdef_info["blkdefs_without_subblocks"]:
            name = self._unique_blkdef_names[blkdef_info["BlkDef"]]    
            link = "#" + slugify(f"{name}", "-")
            self._blkdef_macro_docs += f"## {name}\n\n"
            for attr in self.block_definition_attributes:
                if blkdef_info[attr]:
                    if attr == "Equations":
                        blkdef_info[attr] = blkdef_info[attr].replace("\n", "\n\n")
                    self._blkdef_macro_docs += f"**{attr}:**\n\n{blkdef_info[attr]}\n\n"

    def _create_blkdef_graphical_docs(self) -> None:
        """Create markdown documentation for graphical block definitions (usually with subblocks).
        """
        self._blkdef_with_subblocks_docs = "# Block Defintions (Graphical)\n\n"   
        for blkdef_info in self.all_blkdef_info["blkdefs_with_subblocks"]:
            name = self._unique_blkdef_names[blkdef_info["BlkDef"]]
            self._blkdef_with_subblocks_docs += f"## {name}\n\n"
            abs_dir = str(Path(self.target_directory).resolve())
            blkdef_info["BlockDefinition"].export_block_diagram(target_dir = abs_dir, file_name=name)
            title = blkdef_info["Title"] if blkdef_info["Title"] else "None"
            self._blkdef_with_subblocks_docs += f"### Title\n\n{title} \n\n"
            self._blkdef_with_subblocks_docs += f"### Grafic\n\n![{name}]({name}.svg)\n\n"
            self._create_subblock_docs(blkdef_info)
            for attr in self.block_definition_attributes:
                if not attr == "Title" and blkdef_info[attr]: # Title already added above
                    if attr == "Equations":
                        blkdef_info[attr] = blkdef_info[attr].replace("\n", "\n\n")
                    self._blkdef_with_subblocks_docs += f"### {attr}\n\n{blkdef_info[attr]}\n\n"

    def _create_subblock_docs(self, blkdef_info: dict) -> None:
        """Create markdown documentation of subblocks inside a block definition.

        Lists parameters, states, etc. Also adds the mapping of names (e.g. parameters can have a different name inside the subblock compared to the parent block definition level).  

        Args:
            blkdef_info (dict): Block definition info of parent object.
        """
        attribute_name_mapping = { # mapping between PF name and documentation name
            "sParams": "Parameters",
            "sStates": "States",
            "sUpLimPar": "Upper limitation parameters",
            "sLowLimPar": "Lower limitation parameters",
            "sIntern": "Internal variables",
        }
        self._blkdef_with_subblocks_docs += f"### Subblocks\n\n"
        for subblkref, subblkdef in blkdef_info["Subblocks"].items(): 
            name_subblkdef = self._unique_blkdef_names[subblkdef]
            link = "#" + slugify(name_subblkdef, "-")
            self._blkdef_with_subblocks_docs += f"- [{name_subblkdef}]({link})\n"
            if blkdef_info["Name mapping"].get(subblkref):
                for mapped_attr, par_tuples in blkdef_info["Name mapping"][subblkref].items():
                    mapped_attr = attribute_name_mapping[mapped_attr]
                    if par_tuples:
                        self._blkdef_with_subblocks_docs += f"    - {mapped_attr} mapping: "
                        for par_tuple in par_tuples:
                            self._blkdef_with_subblocks_docs += f"{par_tuple[0]} ({par_tuple[1]}), "
                        self._blkdef_with_subblocks_docs = self._blkdef_with_subblocks_docs[:-1] + "\n"

    def _create_composite_model_docs(self) -> None:
        """Create markdown documentation of composite model (graphic, slots, etc.)
        """
        name = f"Composite Model {self._composite_model.loc_name}" 
        abs_dir = str(Path(self.target_directory).resolve())    
        self._composite_model.export_block_diagram(target_dir = abs_dir, file_name=name)
        title = {self._composite_model.typ_id.sTitle} if {self._composite_model.typ_id.sTitle} else "None"
        self._comp_model_docs = f"""# {name}
- **Block definition**: 
    - Name: {self._composite_model.typ_id.loc_name}
    - Title: {title}

## Graphic
![{name}]({name}.svg)        


## Slot Links
"""
        slot_docs = ""
        parameter_docs = "## Parameters\n\n"    
        for slot, net_elm in self._composite_model.get_slots_and_network_elms_dict(include_empty_slots=False).items():
            if net_elm.GetClassName() == "ElmDsl":
                if self.include_out_of_service == False and net_elm.outserv == 1:
                    continue
                name = self._unique_blkdef_names[net_elm.typ_id] 
                link = "#" + slugify(f"{name}", "-")
                slot_docs += f"- {slot.loc_name}: [{name}]({link})\n" 
                path = self.target_directory + "\\" + name + "_parameters.csv"
                net_elm.ExportToFile(path, ",")
                df = pd.read_csv(path, usecols=list(range(0,5))) # PF creates 6 cols for some parameters
                parameter_docs += f"### Slot Model: {slot.loc_name}\n\n{df.to_html()}\n\n"
        self._comp_model_docs += slot_docs + parameter_docs   

#     def _create_html_from_markdown(self, markdown_content: str) -> None:
#         """Create html documentation from markdown

#         Args:
#             markdown_content (str): markdown document
#         """
#         md = markdown.Markdown(
#             extensions=['extra', 'toc', 'fenced_code'],
#             extension_configs={'toc': {'title': 'Table of Contents', 'anchorlink': True, 'toc_depth': 3}},
#         )
#         body_html = md.convert(markdown_content)
#         toc_html = md.toc

#         css_path = Path(self.css_file_dir)
#         if self.copy_css_file_to_html_location:
#             shutil.copy(self.css_file_dir, self.target_directory)
#             css_file_ref =  css_path.name
#         else:
#             css_file_ref = Path(self.css_file_dir).resolve() # use absolute path

#         full_html = f'''<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>{self.composite_model.loc_name}</title>
#     <link rel="stylesheet" href="{css_file_ref}">
# </head>
# <body>
#     <nav id="sidebar">{toc_html}</nav>
#     <main id="content">{body_html}</main>
# </body>
# </html>'''

#         out = Path(self.target_directory)
#         if out.exists() and out.is_dir():
#             out_file = out / f'{self.file_name}.html'
#         else:
#             out_file = out
#             out_file.parent.mkdir(parents=True, exist_ok=True)

#         with open(out_file, 'w', encoding='utf-8') as f:
#             f.write(full_html)

#         print(f"Wrote: '{out_file}'. Uses css style from file '{css_file_ref}'.")

    def _create_html_from_markdown(self, markdown_content: str) -> None:
        """Create self-contained html documentation from markdown.
        All CSS and SVG figures are inlined so the file works standalone
        (e.g. when included in a Quarto document via iframe or {{< include >}}).
        """
        md = markdown.Markdown(
            extensions=['extra', 'toc', 'fenced_code'],
            extension_configs={'toc': {'title': 'Table of Contents', 'anchorlink': True, 'toc_depth': 3}},
        )
        body_html = md.convert(markdown_content)
        toc_html = md.toc

        # Inline SVGs referenced in the html
        body_html = self._inline_svgs(body_html)

        # Inline CSS
        with open(self.css_file_dir, 'r', encoding='utf-8') as f:
            css_content = f.read()

        full_html = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{self.composite_model.loc_name}</title>
        <style>
    {css_content}
        </style>
    </head>
    <body>
        <nav id="sidebar">{toc_html}</nav>
        <main id="content">{body_html}</main>
    </body>
    </html>'''

        out = Path(self.target_directory)
        if out.exists() and out.is_dir():
            out_file = out / f'{self.file_name}.html'
        else:
            out_file = out
            out_file.parent.mkdir(parents=True, exist_ok=True)

        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"Wrote self-contained: '{out_file}' (CSS and SVGs inlined).")


    def _inline_svgs(self, html: str) -> str:
        """Replace <img src="*.svg"> tags with inline <svg> content.
        Falls back to base64 data URI if the SVG file cannot be read as text.

        Args:
            html (str): HTML string potentially containing <img> tags referencing SVG files.

        Returns:
            str: HTML with SVG files inlined.
        """
        import re
        target_dir = Path(self.target_directory).resolve()

        def replace_svg(match):
            src = match.group(1)
            alt = match.group(2) or ""
            # Only handle .svg files
            if not src.lower().endswith('.svg'):
                return match.group(0)
            svg_path = target_dir / Path(src).name
            try:
                svg_content = svg_path.read_text(encoding='utf-8')
                # Strip XML declaration if present, keep only <svg>...</svg>
                svg_content = re.sub(r'<\?xml[^?]*\?>', '', svg_content).strip()
                return f'<div class="svg-figure" title="{alt}">{svg_content}</div>'
            except Exception:
                # Fallback: base64 data URI
                import base64
                try:
                    b64 = base64.b64encode(svg_path.read_bytes()).decode('utf-8')
                    return f'<img src="data:image/svg+xml;base64,{b64}" alt="{alt}"/>'
                except Exception:
                    return match.group(0)  # leave unchanged if all else fails

        # Match both <img src="..." alt="..."> and <img alt="..." src="...">
        html = re.sub(
            r'<img\s+src="([^"]+)"(?:\s+alt="([^"]*)")?\s*/?>',
            replace_svg,
            html
        )
        # Also handle alt-first ordering
        html = re.sub(
            r'<img\s+alt="([^"]*?)"\s+src="([^"]+?)"\s*/?>',
            lambda m: replace_svg(type('m', (), {
                'group': lambda self, i: [None, m.group(2), m.group(1)][i]
            })()),
            html
        )
        return html
