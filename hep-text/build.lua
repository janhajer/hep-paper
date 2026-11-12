-- l3build configuration of hep-text (shared settings: ../support/common.lua)
module  = "hep-text"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-text"
uploadconfig.topic = {"list"}
