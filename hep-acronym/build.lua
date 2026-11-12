-- l3build configuration of hep-acronym (shared settings: ../support/common.lua)
module  = "hep-acronym"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- "warning" labels a margin note, not a user interface.
coverageexclude = {"warning"}

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-acronym"
uploadconfig.topic = {"acronym"}
