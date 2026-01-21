# Template: ParFlow-CoLM run configuration mapped from a CoLM-only namelist.
# NOTE: This is a starting point. You still need to provide ParFlow inputs
# (grid, geology, BCs, initial conditions) that match your watershed setup.

from parflow.tools import Run
from parflow.tools.fs import get_absolute_path
from parflow.tools.settings import set_working_directory


# -----------------------------------------------------------------------------
# Basic Run setup
# -----------------------------------------------------------------------------

runname = "zj_colm"
zj = Run(runname, __file__)
zj.FileVersion = 4

set_working_directory(get_absolute_path("."))

# -----------------------------------------------------------------------------
# Processor topology (match your MPI layout)
# -----------------------------------------------------------------------------

zj.Process.Topology.P = 1
zj.Process.Topology.Q = 1
zj.Process.Topology.R = 1

# -----------------------------------------------------------------------------
# CoLM coupling (maps to your nml)
# -----------------------------------------------------------------------------

zj.Solver.LSM = "CoLM"

# From DEF_dir_output
zj.Solver.CLM.CLMFileDir = "/home/huangh25/output"

# Forcing (map your ERA5LAND namelist to the PF-CoLM forcing format)
# If you already generate PF-CoLM forcing files from ERA5LAND, set:
#   - MetForcing (forcing type)
#   - MetFileName / MetFilePath (file name/path)
zj.Solver.CLM.MetForcing = "1D"
zj.Solver.CLM.MetFileName = "station0.txt"
zj.Solver.CLM.MetFilePath = "./"

# From DEF_simulation_time%timestep and run control
zj.Solver.CLM.MetFileNT = 24
zj.Solver.CLM.IstepStart = 1

# Output / restart behavior (map from DEF_WRST_FREQ / DEF_HIST_FREQ)
zj.Solver.CLM.CLMDumpInterval = 1
zj.Solver.CLM.WriteLastRST = True
zj.Solver.CLM.DailyRST = True
zj.Solver.CLM.SingleFile = True

# Land surface options (keep consistent with your CoLM-only setup)
zj.Solver.CLM.EvapBeta = "Linear"
zj.Solver.CLM.VegWaterStress = "Saturation"
zj.Solver.CLM.ResSat = 0.2
zj.Solver.CLM.WiltingPoint = 0.2
zj.Solver.CLM.FieldCapacity = 1.0
zj.Solver.CLM.IrrigationType = "none"

# Root-zone and soil layers (ensure these match your CoLM configuration)
zj.Solver.CLM.RootZoneNZ = 10
zj.Solver.CLM.SoiLayer = 10

# -----------------------------------------------------------------------------
# ParFlow model setup (must be completed for a runnable case)
# -----------------------------------------------------------------------------

# TODO: Define ComputationalGrid, Geom, Permeability, BCs, Solver, etc.
# See pfsimulator/colm/examples/colm_version/unname_test.py for a full example.
