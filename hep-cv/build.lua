-- l3build configuration of hep-cv (shared settings: ../support/common.lua)
module  = "hep-cv"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/macros/latex/contrib/hep-cv"
uploadconfig.topic = {"cv"}
uploadconfig.topic = {"cv", "letter", "biblio"}
-- First release on CTAN: the announcement describes the package instead of
-- the \changes entry, which lists fixes to unpublished repository versions.
uploadconfig.announcement = [[
First release on CTAN of hep-cv, a package and a class for curricula vitae, cover letters and publication lists.
The package provides a CV layout with dates in a left column, CV entries and lists, month abbreviations, and publication lists from biblatex bibliographies, sorted by date and numbered or unnumbered.
The class adds article-based defaults, a title page with contact data and photo, cover letters, section and page styles, and subfile support.
hep-cv is part of the hep-paper bundle.]]
uploadconfig.description = [[
<p>The hep-cv package and class typeset curricula vitae, cover letters and publication lists.</p>
<p>The package provides a CV layout with dates in a left column, CV entries and lists, month abbreviations, and publication lists from biblatex bibliographies, sorted by date and numbered or unnumbered. The class adds article-based defaults, a title page with contact data and photo, cover letters, section and page styles, and subfile support.</p>
<p>hep-cv is part of the hep-paper bundle.</p>]]
-- New on CTAN. Set explicitly: l3build's automatic re-validation as a new
-- package runs the curl options as shell commands and validates nothing.
-- Remove after the first release.
uploadconfig.update = false
