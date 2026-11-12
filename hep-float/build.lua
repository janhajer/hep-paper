-- l3build configuration of hep-float (shared settings: ../support/common.lua)
module  = "hep-float"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-float"
uploadconfig.topic = {"float"}
