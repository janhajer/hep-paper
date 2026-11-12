-- l3build configuration of hep-title (shared settings: ../support/common.lua)
module  = "hep-title"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-title"
uploadconfig.topic = {"titlepage"}
