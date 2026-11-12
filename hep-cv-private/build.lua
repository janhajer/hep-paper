-- l3build configuration of hep-cv-private (shared settings: ../support/common.lua)
module  = "hep-cv-private"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- Private package: built, tested and installed, but never released.
hep_private()
