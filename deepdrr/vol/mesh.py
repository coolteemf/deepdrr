from __future__ import annotations
from re import T
from typing import Any, Union, Tuple, List, Optional, Dict, Type

import logging
from killeengeo import Point3D
import numpy as np
from pathlib import Path
import nibabel as nib
from pydicom.filereader import dcmread
import nrrd
from scipy.spatial.transform import Rotation
from scipy.interpolate import RegularGridInterpolator
import pyvista as pv
import killeengeo as kg

from ..pyrenderdrr import DRRMaterial
from .. import load_dicom
from .. import utils
from ..utils import data_utils
from ..utils import mesh_utils
from ..device import Device
from ..projector.material_coefficients import material_coefficients
from .renderable import Renderable
import pyrender
import trimesh

# from deepdrr.utils.mesh_utils import polydata_to_trimesh


vtk, nps, vtk_available = utils.try_import_vtk()

log = logging.getLogger(__name__)


class Mesh(Renderable):
    def __init__(
        self,
        anatomical_from_IJK: Optional[kg.FrameTransform] = None,
        world_from_anatomical: Optional[kg.FrameTransform] = None,
        anatomical_from_ijk: Optional[kg.FrameTransform] = None,
        mesh: pyrender.Mesh = None,
        **kwargs,
    ) -> None:
        if mesh is None:
            raise ValueError("mesh must be specified")

        self.mesh = mesh
        
        Renderable.__init__(
            self,
            anatomical_from_IJK=anatomical_from_IJK,
            world_from_anatomical=world_from_anatomical,
            anatomical_from_ijk=anatomical_from_ijk,
            **kwargs,
        )


    def set_enabled(self, enabled: bool) -> None:
        self.mesh.is_visible = enabled
        
    def get_center(self) -> kg.Point3D:
        return kg.point(self.mesh.centroid)

    def get_bounding_box_in_world(self) -> Tuple[Point3D, Point3D]:
        raise NotImplementedError("TODO")

    @classmethod
    def from_stl(
        cls,
        path: Union[str, Path],
        material: str | DRRMaterial = "iron",
        convert_to_RAS: bool = False,
        **kwargs,
    ) -> Mesh:
        """Create a mesh for the given material with default density.

        Args:
            path (Union[str, Path]): Path to the STL file.
            material (str | DRRMaterial, optional): Material to use. Defaults to "iron".
            convert_to_RAS (bool, optional): Good practice is to store meshes in LPS coordinates. When loading a mesh
                from a CT file, such as a segmentation, that was saved in LPS coordinates, this should be set to True.
                Defaults to False.

        Returns:
            Mesh: The mesh.

        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Could not find file {path}")

        if isinstance(material, str):
            material = DRRMaterial.from_name(material)

        mesh = mesh_utils.load_trimesh(path, convert_to_RAS=convert_to_RAS)
        mesh = pyrender.Mesh.from_trimesh(mesh, material=material)
        return cls(mesh=mesh, **kwargs)