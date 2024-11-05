from powfacpy.base.active_project import ActiveProjectCached, ActiveProject
from powfacpy.pf_class_protocols import PFApp


class ApplicationBase:
    """Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when one project stays active)
    - or ActiveProject (recommended when the active project may change)
    """

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        if cached:
            self.act_prj: ActiveProjectCached = ActiveProjectCached(pf_app)
        else:
            self.act_prj: ActiveProject = ActiveProject(pf_app)
