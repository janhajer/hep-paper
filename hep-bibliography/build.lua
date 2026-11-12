-- l3build configuration of hep-bibliography (shared settings: ../support/common.lua)
module  = "hep-bibliography"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/biblatex-contrib/hep-bibliography"
uploadconfig.topic = {"biblatex", "physics"}
