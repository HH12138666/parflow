# -----------------------------------------------------------------------------
# ParFlow-CLM comparison run (single-column baseline)
# -----------------------------------------------------------------------------

import argparse
from parflow import Run
from parflow.tools.fs import mkdir, cp, get_absolute_path

run_name = "zj_parflow_clm_compare"
clm = Run(run_name, __file__)

# -----------------------------------------------------------------------------
# Making output directories and copying input files
# -----------------------------------------------------------------------------

new_output_dir_name = get_absolute_path("test_output/zj_parflow_clm_compare")
mkdir(new_output_dir_name)
mkdir(new_output_dir_name + "/output")

cp("$PF_SRC/test/tcl/clm/pfclm_sc/drv_clmin.dat", new_output_dir_name)
cp("$PF_SRC/test/tcl/clm/pfclm_sc/drv_vegm.dat", new_output_dir_name)
cp("$PF_SRC/test/tcl/clm/pfclm_sc/drv_vegp.dat", new_output_dir_name)
cp(
    "$PF_SRC/test/tcl/clm/pfclm_sc/forcing_singleColumn_3days_CONUS2.prn",
    new_output_dir_name,
)

# -----------------------------------------------------------------------------
# File input version number
# -----------------------------------------------------------------------------

clm.FileVersion = 4

# -----------------------------------------------------------------------------
# Process Topology
# -----------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--p", default=1)
parser.add_argument("-q", "--q", default=1)
parser.add_argument("-r", "--r", default=1)
args = parser.parse_args()

clm.Process.Topology.P = args.p
clm.Process.Topology.Q = args.q
clm.Process.Topology.R = args.r

# -----------------------------------------------------------------------------
# Computational Grid
# -----------------------------------------------------------------------------

clm.ComputationalGrid.Lower.X = 0.0
clm.ComputationalGrid.Lower.Y = 0.0
clm.ComputationalGrid.Lower.Z = 0.0

clm.ComputationalGrid.DX = 2.0
clm.ComputationalGrid.DY = 2.0
clm.ComputationalGrid.DZ = 0.1

clm.ComputationalGrid.NX = 1
clm.ComputationalGrid.NY = 1
clm.ComputationalGrid.NZ = 20

# -----------------------------------------------------------------------------
# The Names of the GeomInputs
# -----------------------------------------------------------------------------

clm.GeomInput.Names = "domain_input"

# -----------------------------------------------------------------------------
# Domain Geometry Input
# -----------------------------------------------------------------------------

clm.GeomInput.domain_input.InputType = "Box"
clm.GeomInput.domain_input.GeomName = "domain"

# -----------------------------------------------------------------------------
# Domain Geometry
# -----------------------------------------------------------------------------

clm.Geom.domain.Lower.X = 0.0
clm.Geom.domain.Lower.Y = 0.0
clm.Geom.domain.Lower.Z = 0.0

clm.Geom.domain.Upper.X = 2.0
clm.Geom.domain.Upper.Y = 2.0
clm.Geom.domain.Upper.Z = 2.0

clm.Geom.domain.Patches = "x_lower x_upper y_lower y_upper z_lower z_upper"

# --------------------------------------------
# variable dz assignments
# ------------------------------------------

clm.Solver.Nonlinear.VariableDz = True
clm.dzScale.GeomNames = "domain"
clm.dzScale.Type = "nzList"
clm.dzScale.nzListNumber = 20

clm.Cell._0.dzScale.Value = 10.0
clm.Cell._1.dzScale.Value = 5.0
clm.Cell._2.dzScale.Value = 1.0
clm.Cell._3.dzScale.Value = 1.0
clm.Cell._4.dzScale.Value = 1.0
clm.Cell._5.dzScale.Value = 1.0
clm.Cell._6.dzScale.Value = 1.0
clm.Cell._7.dzScale.Value = 1.0
clm.Cell._8.dzScale.Value = 1.0
clm.Cell._9.dzScale.Value = 1.0
clm.Cell._10.dzScale.Value = 1.0
clm.Cell._11.dzScale.Value = 1.0
clm.Cell._12.dzScale.Value = 1.0
clm.Cell._13.dzScale.Value = 1.0
clm.Cell._14.dzScale.Value = 1.0
clm.Cell._15.dzScale.Value = 1.0
clm.Cell._16.dzScale.Value = 1.0
clm.Cell._17.dzScale.Value = 1.0
clm.Cell._18.dzScale.Value = 1.0
clm.Cell._19.dzScale.Value = 0.1

# -----------------------------------------------------------------------------
# Perm
# -----------------------------------------------------------------------------

clm.Geom.Perm.Names = "domain"
clm.Geom.domain.Perm.Type = "Constant"
clm.Geom.domain.Perm.Value = 0.1465

clm.Perm.TensorType = "TensorByGeom"
clm.Geom.Perm.TensorByGeom.Names = "domain"
clm.Geom.domain.Perm.TensorValX = 1.0
clm.Geom.domain.Perm.TensorValY = 1.0
clm.Geom.domain.Perm.TensorValZ = 1.0

# -----------------------------------------------------------------------------
# Specific Storage
# -----------------------------------------------------------------------------

clm.SpecificStorage.Type = "Constant"
clm.SpecificStorage.GeomNames = "domain"
clm.Geom.domain.SpecificStorage.Value = 1.0e-4

# -----------------------------------------------------------------------------
# Phases
# -----------------------------------------------------------------------------

clm.Phase.Names = "water"

clm.Phase.water.Density.Type = "Constant"
clm.Phase.water.Density.Value = 1.0

clm.Phase.water.Viscosity.Type = "Constant"
clm.Phase.water.Viscosity.Value = 1.0

# -----------------------------------------------------------------------------
# Contaminants
# -----------------------------------------------------------------------------

clm.Contaminants.Names = ""

# -----------------------------------------------------------------------------
# Gravity
# -----------------------------------------------------------------------------

clm.Gravity = 1.0

# -----------------------------------------------------------------------------
# Setup timing info
# -----------------------------------------------------------------------------

clm.TimingInfo.BaseUnit = 1.0
clm.TimingInfo.StartCount = 0
clm.TimingInfo.StartTime = 0.0
clm.TimingInfo.StopTime = 24.0
clm.TimingInfo.DumpInterval = 1.0
clm.TimeStep.Type = "Constant"
clm.TimeStep.Value = 1.0

# -----------------------------------------------------------------------------
# Porosity
# -----------------------------------------------------------------------------

clm.Geom.Porosity.GeomNames = "domain"
clm.Geom.domain.Porosity.Type = "Constant"
clm.Geom.domain.Porosity.Value = 0.25

# -----------------------------------------------------------------------------
# Domain
# -----------------------------------------------------------------------------

clm.Domain.GeomName = "domain"

# -----------------------------------------------------------------------------
# Mobility
# -----------------------------------------------------------------------------

clm.Phase.water.Mobility.Type = "Constant"
clm.Phase.water.Mobility.Value = 1.0

# -----------------------------------------------------------------------------
# Relative Permeability
# -----------------------------------------------------------------------------

clm.Phase.RelPerm.Type = "VanGenuchten"
clm.Phase.RelPerm.GeomNames = "domain"

clm.Geom.domain.RelPerm.Alpha = 2.0
clm.Geom.domain.RelPerm.N = 2.0

# -----------------------------------------------------------------------------
# Saturation
# -----------------------------------------------------------------------------

clm.Phase.Saturation.Type = "VanGenuchten"
clm.Phase.Saturation.GeomNames = "domain"

clm.Geom.domain.Saturation.Alpha = 2.0
clm.Geom.domain.Saturation.N = 3.0
clm.Geom.domain.Saturation.SRes = 0.2
clm.Geom.domain.Saturation.SSat = 1.0

# -----------------------------------------------------------------------------
# Wells
# -----------------------------------------------------------------------------

clm.Wells.Names = ""

# -----------------------------------------------------------------------------
# Time Cycles
# -----------------------------------------------------------------------------

clm.Cycle.Names = "constant"
clm.Cycle.constant.Names = "alltime"
clm.Cycle.constant.alltime.Length = 1
clm.Cycle.constant.Repeat = -1

# -----------------------------------------------------------------------------
# Boundary Conditions: Pressure
# -----------------------------------------------------------------------------

clm.BCPressure.PatchNames = "x_lower x_upper y_lower y_upper z_lower z_upper"

clm.Patch.x_lower.BCPressure.Type = "FluxConst"
clm.Patch.x_lower.BCPressure.Cycle = "constant"
clm.Patch.x_lower.BCPressure.alltime.Value = 0.0

clm.Patch.y_lower.BCPressure.Type = "FluxConst"
clm.Patch.y_lower.BCPressure.Cycle = "constant"
clm.Patch.y_lower.BCPressure.alltime.Value = 0.0

clm.Patch.z_lower.BCPressure.Type = "DirEquilRefPatch"
clm.Patch.z_lower.BCPressure.RefGeom = "domain"
clm.Patch.z_lower.BCPressure.RefPatch = "z_lower"
clm.Patch.z_lower.BCPressure.Cycle = "constant"
clm.Patch.z_lower.BCPressure.alltime.Value = 0.0

clm.Patch.x_upper.BCPressure.Type = "FluxConst"
clm.Patch.x_upper.BCPressure.Cycle = "constant"
clm.Patch.x_upper.BCPressure.alltime.Value = 0.0

clm.Patch.y_upper.BCPressure.Type = "FluxConst"
clm.Patch.y_upper.BCPressure.Cycle = "constant"
clm.Patch.y_upper.BCPressure.alltime.Value = 0.0

clm.Patch.z_upper.BCPressure.Type = "OverlandFlow"
clm.Patch.z_upper.BCPressure.Cycle = "constant"
clm.Patch.z_upper.BCPressure.alltime.Value = 0.0

# -----------------------------------------------------------------------------
# Topo slopes
# -----------------------------------------------------------------------------

clm.TopoSlopesX.Type = "Constant"
clm.TopoSlopesX.GeomNames = "domain"
clm.TopoSlopesX.Geom.domain.Value = 0.05

clm.TopoSlopesY.Type = "Constant"
clm.TopoSlopesY.GeomNames = "domain"
clm.TopoSlopesY.Geom.domain.Value = 0.00

# -----------------------------------------------------------------------------
# Mannings coefficient
# -----------------------------------------------------------------------------

clm.Mannings.Type = "Constant"
clm.Mannings.GeomNames = "domain"
clm.Mannings.Geom.domain.Value = 2.0e-6

# -----------------------------------------------------------------------------
# Phase sources
# -----------------------------------------------------------------------------

clm.PhaseSources.water.Type = "Constant"
clm.PhaseSources.water.GeomNames = "domain"
clm.PhaseSources.water.Geom.domain.Value = 0.0

# -----------------------------------------------------------------------------
# Exact solution specification for error calculations
# -----------------------------------------------------------------------------

clm.KnownSolution = "NoKnownSolution"

# -----------------------------------------------------------------------------
# Set solver parameters
# -----------------------------------------------------------------------------

clm.Solver = "Richards"
clm.Solver.MaxIter = 9000

clm.Solver.Nonlinear.MaxIter = 100
clm.Solver.Nonlinear.ResidualTol = 1e-5
clm.Solver.Nonlinear.EtaChoice = "EtaConstant"
clm.Solver.Nonlinear.EtaValue = 1e-5
clm.Solver.Nonlinear.UseJacobian = False
clm.Solver.Nonlinear.DerivativeEpsilon = 1e-12
clm.Solver.Nonlinear.StepTol = 1e-30
clm.Solver.Nonlinear.Globalization = "LineSearch"
clm.Solver.Linear.KrylovDimension = 100
clm.Solver.Linear.MaxRestarts = 5
clm.Solver.Linear.Preconditioner = "PFMG"
clm.Solver.PrintSubsurf = False
clm.Solver.Drop = 1.0e-20
clm.Solver.AbsTol = 1e-9

# Writing output options for ParFlow
clm.Solver.PrintSubsurfData = False
clm.Solver.PrintPressure = True
clm.Solver.PrintSaturation = True
clm.Solver.PrintCLM = True
clm.Solver.PrintMask = True
clm.Solver.PrintSpecificStorage = True
clm.Solver.PrintEvapTrans = True

clm.Solver.WriteSiloMannings = False
clm.Solver.WriteSiloMask = False
clm.Solver.WriteSiloSlopes = False
clm.Solver.WriteSiloSaturation = False

# -----------------------------------------------------------------------------
# LSM / CLM options
# -----------------------------------------------------------------------------

clm.Solver.LSM = "CLM"
clm.Solver.CLM.MetForcing = "1D"
clm.Solver.CLM.MetFileName = "forcing_singleColumn_3days_CONUS2.prn"
clm.Solver.CLM.MetFilePath = "."

clm.Solver.CLM.EvapBeta = "Linear"
clm.Solver.CLM.VegWaterStress = "Saturation"
clm.Solver.CLM.ResSat = 0.3
clm.Solver.CLM.WiltingPoint = 0.3
clm.Solver.CLM.FieldCapacity = 1.00
clm.Solver.CLM.IrrigationType = "none"
clm.Solver.CLM.RootZoneNZ = 19
clm.Solver.CLM.SoiLayer = 15

clm.Solver.PrintLSMSink = False
clm.Solver.CLM.CLMDumpInterval = 1
clm.Solver.CLM.CLMFileDir = "output/"
clm.Solver.CLM.BinaryOutDir = False
clm.Solver.CLM.IstepStart = 1
clm.Solver.WriteCLMBinary = False
clm.Solver.WriteSiloCLM = False
clm.Solver.CLM.WriteLogs = False
clm.Solver.CLM.WriteLastRST = True
clm.Solver.CLM.DailyRST = False
clm.Solver.CLM.SingleFile = True

# -----------------------------------------------------------------------------
# Initial conditions: water pressure
# -----------------------------------------------------------------------------

clm.ICPressure.Type = "HydroStaticPatch"
clm.ICPressure.GeomNames = "domain"
clm.Geom.domain.ICPressure.Value = 2.0
clm.Geom.domain.ICPressure.RefGeom = "domain"
clm.Geom.domain.ICPressure.RefPatch = "z_lower"

# -----------------------------------------------------------------------------
# Run ParFlow
# -----------------------------------------------------------------------------

clm.run(working_directory=new_output_dir_name)
