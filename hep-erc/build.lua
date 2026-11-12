-- l3build configuration of hep-erc (shared settings: ../support/common.lua)
module  = "hep-erc"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- Install the proposal templates next to the package.
installfiles = {"*.sty", "hep-erc-header.tex", "hep-erc-B1.tex",
  "hep-erc-B2.tex"}

-- Template compilation tests (config-templates.lua)
checkconfigs = {"build", "config-templates"}

-- Private package: built, tested and installed, but never released.
hep_private()
