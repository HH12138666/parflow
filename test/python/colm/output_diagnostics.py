import csv
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from parflow.tools.io import read_pfb

CLM_OUTPUT_LAYER_NAMES = (
    "eflx_lh_tot",
    "eflx_lwrad_out",
    "eflx_sh_tot",
    "eflx_soil_grnd",
    "qflx_evap_tot",
    "qflx_evap_grnd",
    "qflx_evap_soi",
    "qflx_evap_veg",
    "qflx_tran_veg",
    "qflx_infl",
    "swe_out",
    "t_grnd",
    "irrigation_output_inactive",
    "t_soil_0",
    "t_soil_1",
    "t_soil_2",
    "t_soil_3",
    "t_soil_4",
    "t_soil_5",
    "t_soil_6",
    "t_soil_7",
    "t_soil_8",
    "t_soil_9",
)


@dataclass(frozen=True)
class LayerStatistics:
    layer: int
    variable: str
    point_count: int
    nonzero_difference_count: int
    reference_minimum: float
    reference_maximum: float
    computed_minimum: float
    computed_maximum: float
    maximum_absolute_difference: float
    mean_absolute_difference: float
    root_mean_square_error: float
    relative_l2_error: float
    maximum_y: int
    maximum_x: int
    reference_at_maximum: float
    computed_at_maximum: float
    signed_difference_at_maximum: float


def _relative_l2_error(difference: np.ndarray, reference: np.ndarray) -> float:
    difference_norm = float(np.linalg.norm(difference))
    reference_norm = float(np.linalg.norm(reference))
    if reference_norm != 0.0:
        return difference_norm / reference_norm
    if difference_norm == 0.0:
        return 0.0
    return float("inf")


def _layer_statistics(
    layer: int, computed: np.ndarray, reference: np.ndarray
) -> LayerStatistics:
    difference = computed - reference
    absolute_difference = np.abs(difference)
    maximum_y, maximum_x = np.unravel_index(
        np.argmax(absolute_difference), absolute_difference.shape
    )
    return LayerStatistics(
        layer=layer,
        variable=CLM_OUTPUT_LAYER_NAMES[layer],
        point_count=int(difference.size),
        nonzero_difference_count=int(np.count_nonzero(difference)),
        reference_minimum=float(np.min(reference)),
        reference_maximum=float(np.max(reference)),
        computed_minimum=float(np.min(computed)),
        computed_maximum=float(np.max(computed)),
        maximum_absolute_difference=float(absolute_difference[maximum_y, maximum_x]),
        mean_absolute_difference=float(np.mean(absolute_difference)),
        root_mean_square_error=float(np.sqrt(np.mean(np.square(difference)))),
        relative_l2_error=_relative_l2_error(difference, reference),
        maximum_y=int(maximum_y),
        maximum_x=int(maximum_x),
        reference_at_maximum=float(reference[maximum_y, maximum_x]),
        computed_at_maximum=float(computed[maximum_y, maximum_x]),
        signed_difference_at_maximum=float(difference[maximum_y, maximum_x]),
    )


def _write_summary(path: Path, statistics: tuple[LayerStatistics, ...]) -> None:
    field_names = tuple(asdict(statistics[0]))
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(asdict(item) for item in statistics)


def _write_all_points(path: Path, computed: np.ndarray, reference: np.ndarray) -> None:
    header = (
        "layer",
        "variable",
        "y",
        "x",
        "reference",
        "computed",
        "signed_difference",
        "absolute_difference",
    )
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        for layer, y, x in np.ndindex(computed.shape):
            difference = computed[layer, y, x] - reference[layer, y, x]
            writer.writerow(
                (
                    layer,
                    CLM_OUTPUT_LAYER_NAMES[layer],
                    y,
                    x,
                    f"{reference[layer, y, x]:.17e}",
                    f"{computed[layer, y, x]:.17e}",
                    f"{difference:.17e}",
                    f"{abs(difference):.17e}",
                )
            )


def _print_summary(statistics: tuple[LayerStatistics, ...]) -> None:
    print("CoLM clm_output layer error summary")
    for item in statistics:
        print(
            f"  layer={item.layer:02d} variable={item.variable:<27} "
            f"max_abs={item.maximum_absolute_difference:.17e} "
            f"mean_abs={item.mean_absolute_difference:.17e} "
            f"rmse={item.root_mean_square_error:.17e} "
            f"relative_l2={item.relative_l2_error:.17e} "
            f"max_at=(y={item.maximum_y},x={item.maximum_x})"
        )


def write_clm_output_error_report(
    computed_file: Path, reference_file: Path, report_directory: Path
) -> None:
    computed = read_pfb(str(computed_file))
    reference = read_pfb(str(reference_file))
    if computed.shape != reference.shape:
        raise ValueError(
            f"CoLM output shape mismatch: {computed.shape} != {reference.shape}"
        )
    expected_shape = (len(CLM_OUTPUT_LAYER_NAMES), 5, 5)
    if computed.shape != expected_shape:
        raise ValueError(
            f"Unexpected CoLM output shape: {computed.shape} != {expected_shape}"
        )

    report_directory.mkdir(parents=True, exist_ok=True)
    statistics = tuple(
        _layer_statistics(layer, computed[layer], reference[layer])
        for layer in range(computed.shape[0])
    )
    _write_summary(report_directory / "clm_output_layer_summary.csv", statistics)
    _write_all_points(
        report_directory / "clm_output_all_points.csv", computed, reference
    )
    shutil.copy2(computed_file, report_directory / "clm_output_computed.pfb")
    shutil.copy2(reference_file, report_directory / "clm_output_reference.pfb")
    _print_summary(statistics)
