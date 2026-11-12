-- l3build configuration of hep-graphic (shared settings: ../support/common.lua)
module  = "hep-graphic"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-graphic"
uploadconfig.topic = {"graphics"}
