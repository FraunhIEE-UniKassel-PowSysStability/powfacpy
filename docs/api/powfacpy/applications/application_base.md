Module powfacpy.applications.application_base
=============================================

Classes
-------

`ApplicationBase(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when only one project stays active)
    - or ActiveProject (recommended when the active project may change)

    ### Descendants

    * powfacpy.applications.database.Database
    * powfacpy.applications.database.DatabaseDict
    * powfacpy.applications.dynamic_model_docs.DynamicModelDocs
    * powfacpy.applications.dynamic_simulation.DynamicSimulation
    * powfacpy.applications.model_exchange.CGMES
    * powfacpy.applications.networks.Networks
    * powfacpy.applications.pandapower_interface.PandapowerInterface
    * powfacpy.applications.pandas_interface.PandasInterface
    * powfacpy.applications.parameter_studies.ParameterStudy
    * powfacpy.applications.parameter_studies.Variant
    * powfacpy.applications.plots.Plots
    * powfacpy.applications.results.Results
    * powfacpy.applications.static_calc.StaticCalc
    * powfacpy.applications.study_cases.StudyCases
    * powfacpy.applications.subsystems.SubSystem
    * powfacpy.applications.subsystems.SubSystemContainer
    * powfacpy.applications.topology.Topology

    ### Instance variables

    `app`
    :