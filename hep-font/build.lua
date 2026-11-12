-- l3build configuration of hep-font (shared settings: ../support/common.lua)
module  = "hep-font"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- The package supports XeLaTeX, so the tests also run with XeTeX
-- (results in <name>.xetex.tlg where they differ from pdfTeX).
checkengines = {"pdftex", "luatex", "xetex"}

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/fonts/utilities/hep-font"
uploadconfig.topic = {"font", "font-mgmt", "font-use"}
