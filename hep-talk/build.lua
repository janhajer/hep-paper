-- l3build configuration of hep-talk (shared settings: ../support/common.lua)
module  = "hep-talk"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-talk"
uploadconfig.topic = {"presentation", "physics"}
