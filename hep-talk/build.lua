-- l3build configuration of hep-talk (shared settings: ../support/common.lua)
module  = "hep-talk"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-talk"
uploadconfig.topic = {"presentation", "physics"}
-- First release on CTAN: the announcement describes the package instead of
-- the \changes entry, which lists fixes to unpublished repository versions.
uploadconfig.announcement = [[
First release on CTAN of hep-talk, a package for slides based on the article class instead of beamer.
It sets the page geometry from a paper width and an aspect ratio, and provides slides with overlays (based on the overlays package), blocks, columns and rows, title slides with logos, page numbers, citations and bibliographies suited to slides, and dark, light, blue and metropolis-like colour themes.
hep-talk is part of the hep-paper bundle and uses its fonts, math and bibliography setup.]]
uploadconfig.description = [[
<p>The hep-talk package typesets slides with the article class instead of beamer.</p>
<p>It sets the page geometry from a paper width and an aspect ratio, and provides slides with overlays (based on the overlays package), blocks, columns and rows, title slides with logos, page numbers, citations and bibliographies suited to slides, and dark, light, blue and metropolis-like colour themes.</p>
<p>hep-talk is part of the hep-paper bundle and uses its fonts, math and bibliography setup.</p>]]
-- New on CTAN. Set explicitly: l3build's automatic re-validation as a new
-- package runs the curl options as shell commands and validates nothing.
-- Remove after the first release.
uploadconfig.update = false
