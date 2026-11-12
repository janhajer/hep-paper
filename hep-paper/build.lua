-- l3build configuration of hep-paper (shared settings: ../support/common.lua)
module  = "hep-paper"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- Journal compatibility tests (config-journals.lua)
checkconfigs = {"build", "config-journals", "config-loadorder"}

-- Advice on amsmath and an external script, not interfaces of hep-paper.
coverageexclude = {"\\numberwithin", "arxiv-collector"}

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-paper"
uploadconfig.topic = {"physics"}
