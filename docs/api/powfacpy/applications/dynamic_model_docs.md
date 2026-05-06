Module powfacpy.applications.dynamic_model_docs
===============================================

Classes
-------

`DynamicModelDocs(pf_app: PFApp | None | bool = False, cached: bool = False)`
:   Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when only one project stays active)
    - or ActiveProject (recommended when the active project may change)

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Methods

    `create_docs(self, model: ElmComp | ElmDsl, clear_target_dir: bool = False) ‑> None`
    :