# Minimal ParFlow-CoLM run template aligned to the provided CoLM-only namelist.
# Place your CoLM namelist as "CoLM_nlfile.nml" in this run directory so CoLM
# can read your mksrfdata/mkinidata paths during initialization.

from parflow.tools import Run
from parflow.tools.fs import get_absolute_path
from parflow.tools.settings import set_working_directory

runname = "zj_colm_minimal"
run = Run(runname, __file__)
run.FileVersion = 4

set_working_directory(get_absolute_path("."))

# ---------------------------------------------------------------------
# Processor topology (single process for minimal run)
# ---------------------------------------------------------------------
run.Process.Topology.P = 1
run.Process.Topology.Q = 1
run.Process.Topology.R = 1

# ---------------------------------------------------------------------
# Computational Grid (minimal example; adjust to your basin/grid)
# ---------------------------------------------------------------------
run.ComputationalGrid.Lower.X = 0.0
run.ComputationalGrid.Lower.Y = 0.0
run.ComputationalGrid.Lower.Z = 0.0

# Minimal 10x10x5 grid (placeholder). Replace with your model grid.
run.ComputationalGrid.NX = 10
run.ComputationalGrid.NY = 10
run.ComputationalGrid.NZ = 5

run.ComputationalGrid.DX = 1000.0
run.ComputationalGrid.DY = 1000.0
run.ComputationalGrid.DZ = 1.0

# ---------------------------------------------------------------------
# Geometry (single-box domain)
# ---------------------------------------------------------------------
run.GeomInput.Names = "domain_input"
run.GeomInput.domain_input.InputType = "Box"
run.GeomInput.domain_input.GeomName = "domain"

run.Geom.domain.Lower.X = 0.0
run.Geom.domain.Lower.Y = 0.0
run.Geom.domain.Lower.Z = 0.0

run.Geom.domain.Upper.X = run.ComputationalGrid.NX * run.ComputationalGrid.DX
run.Geom.domain.Upper.Y = run.ComputationalGrid.NY * run.ComputationalGrid.DY
run.Geom.domain.Upper.Z = run.ComputationalGrid.NZ * run.ComputationalGrid.DZ

run.Geom.domain.Patches = "x_lower x_upper y_lower y_upper z_lower z_upper"

# ---------------------------------------------------------------------
# Permeability & Porosity (uniform constants for minimal run)
# ---------------------------------------------------------------------
run.Geom.Perm.Names = "domain"
run.Geom.domain.Perm.Type = "Constant"
run.Geom.domain.Perm.Value = 1.0e-5

run.Geom.Porosity.GeomNames = "domain"
run.Geom.domain.Porosity.Type = "Constant"
run.Geom.domain.Porosity.Value = 0.25

# ---------------------------------------------------------------------
# Specific storage (uniform)
# ---------------------------------------------------------------------
run.SpecificStorage.Type = "Constant"
run.SpecificStorage.GeomNames = "domain"
run.Geom.domain.SpecificStorage.Value = 1.0e-4

# ---------------------------------------------------------------------
# Time settings (match CoLM timestep = 3600 s)
# ---------------------------------------------------------------------
run.TimingInfo.BaseUnit = 1.0
run.TimingInfo.StartCount = 0
run.TimingInfo.StartTime = 0.0
run.TimingInfo.StopTime = 3600.0
run.TimingInfo.DumpInterval = 3600.0

run.TimeStep.Type = "Constant"
run.TimeStep.Value = 3600.0

# ---------------------------------------------------------------------
# Boundary conditions (simple no-flow sides and bottom)
# ---------------------------------------------------------------------
run.BCPressure.PatchNames = "x_lower x_upper y_lower y_upper z_lower z_upper"

run.Patch.x_lower.BCPressure.Type = "FluxConst"
run.Patch.x_lower.BCPressure.Cycle = "constant"
run.Patch.x_lower.BCPressure.alltime.Value = 0.0

run.Patch.x_upper.BCPressure.Type = "FluxConst"
run.Patch.x_upper.BCPressure.Cycle = "constant"
run.Patch.x_upper.BCPressure.alltime.Value = 0.0

run.Patch.y_lower.BCPressure.Type = "FluxConst"
run.Patch.y_lower.BCPressure.Cycle = "constant"
run.Patch.y_lower.BCPressure.alltime.Value = 0.0

run.Patch.y_upper.BCPressure.Type = "FluxConst"
run.Patch.y_upper.BCPressure.Cycle = "constant"
run.Patch.y_upper.BCPressure.alltime.Value = 0.0

run.Patch.z_lower.BCPressure.Type = "FluxConst"
run.Patch.z_lower.BCPressure.Cycle = "constant"
run.Patch.z_lower.BCPressure.alltime.Value = 0.0

run.Patch.z_upper.BCPressure.Type = "FluxConst"
run.Patch.z_upper.BCPressure.Cycle = "constant"
run.Patch.z_upper.BCPressure.alltime.Value = 0.0

# ---------------------------------------------------------------------
# Initial conditions (hydrostatic with constant pressure)
# ---------------------------------------------------------------------
run.ICPressure.Type = "Constant"
run.ICPressure.GeomNames = "domain"
run.Geom.domain.ICPressure.Value = -1.0

# ---------------------------------------------------------------------
# CoLM coupling (align with your provided namelist)
# ---------------------------------------------------------------------
run.Solver.LSM = "CoLM"

# Output directory (from DEF_dir_output)
run.Solver.CLM.CLMFileDir = "/home/huangh25/output"
run.Solver.CLM.Print1dOut = False
run.Solver.CLM.CLMDumpInterval = 1

# Forcing settings (replace with your actual forcing files)
run.Solver.CLM.MetForcing = "1D"
run.Solver.CLM.MetFileName = "station0.txt"
run.Solver.CLM.MetFilePath = "./"
run.Solver.CLM.MetFileNT = 24
run.Solver.CLM.IstepStart = 1

run.Solver.CLM.EvapBeta = "Linear"
run.Solver.CLM.VegWaterStress = "Saturation"
run.Solver.CLM.ResSat = 0.2
run.Solver.CLM.WiltingPoint = 0.2
run.Solver.CLM.FieldCapacity = 1.0
run.Solver.CLM.IrrigationType = "none"

run.Solver.CLM.RootZoneNZ = 10
run.Solver.CLM.SoiLayer = 10
run.Solver.CLM.ReuseCount = 1
run.Solver.CLM.WriteLogs = False
run.Solver.CLM.WriteLastRST = True
run.Solver.CLM.DailyRST = True
run.Solver.CLM.SingleFile = True

# ---------------------------------------------------------------------
# Richards solver (minimal)
# ---------------------------------------------------------------------
run.Solver = "Richards"
run.Solver.MaxIter = 1000
run.Solver.Nonlinear.MaxIter = 20
run.Solver.Nonlinear.ResidualTol = 1e-6
run.Solver.Linear.KrylovDimension = 20
run.Solver.Linear.MaxRestarts = 2

if __name__ == "__main__":
    run.run()
