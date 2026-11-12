-- l3build configuration of hep-cv (shared settings: ../support/common.lua)
module  = "hep-cv"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-cv"
uploadconfig.topic = {"cv"}
