import pyhf
import numpy as np

from typing import Any, Dict, List, Tuple

import logging
from .logger import logger
log = logging.getLogger(__name__)

def model_and_data(
    spec: Dict[str, Any], poi_name: str = None, asimov: bool = False, with_aux: bool = True
) -> Tuple[pyhf.pdf.Model, List[float]]:
    """
    Returns model and data for a pyhf workspace spec.
    """
    workspace = pyhf.Workspace(spec)
    model = workspace.model(
        modifier_settings = {
            "normsys": {"interpcode": "code4"},
            "histosys": {"interpcode": "code4p"},
        },
        poi_name = poi_name
    )
    if not asimov:
        data = workspace.data(model, with_aux = with_aux)
    else:
        data = build_Asimov_data(model, with_aux = with_aux)
    return model, data


def get_parameter_names(model: pyhf.pdf.Model) -> List[str]:
    """
    Get the labels of all fit parameters, expanding vectors that act on
    one bin per vector entry (gammas)
    """
    labels = []
    for parname in model.config.par_order:
        for i_par in range(model.config.param_set(parname).n_parameters):
            labels.append(
                f"{parname}[{i_par}]"
                if model.config.param_set(parname).n_parameters > 1
                else parname
            )
    return labels


def build_Asimov_data(model: pyhf.Model, with_aux: bool = True) -> List[float]:
    """
    Returns the Asimov dataset (optionally with auxdata) for a model.
    """
    asimov_data = np.sum(model.nominal_rates, axis=1)[0][0].tolist()
    if with_aux:
        return asimov_data + model.config.auxdata
    return asimov_data
                                      
