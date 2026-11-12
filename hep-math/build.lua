-- l3build configuration of hep-math (shared settings: ../support/common.lua)
module  = "hep-math"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-math"
uploadconfig.topic = {"maths"}
