-- l3build configuration of the hep-paper bundle.
--
-- Run l3build here to process every package, or inside a package directory
-- to process only that one. The shared settings are in support/common.lua.
--
--   l3build doc        typeset all documentation
--   l3build check      run the regression tests (pdfTeX and LuaTeX, plus
--                      XeTeX for hep-font and hep-math-font)
--   l3build install    install all packages (and fonts) into TEXMFHOME
--   l3build ctan       build one CTAN zip per package in its directory
--   l3build clean      remove everything that was built
--   l3build coverage   list documented commands that no test uses
--   l3build pytest     run the Python tests of hep-math-font (also part of
--                      a full l3build check)

modules = dofile("support/modules.lua")
cleanfiles = {}

-- Each package is released separately, so build one archive per package
-- instead of a single bundle archive.
target_list.ctan.bundle_func = function()
  return call(modules, "ctan")
end

-- Also remove the shared build tree.
target_list.clean.bundle_func = function()
  return call(modules, "clean") + rmdir("build")
end

-- Documented commands without tests (defined in support/common.lua).
target_list.coverage = {
  desc = "Lists documented commands that no test uses",
  bundle_func = function()
    return call(modules, "coverage")
  end
}

-- Python tests of hep-math-font (defined in hep-math-font/build.lua).
target_list.pytest = {
  desc = "Runs the Python regression tests of the math fonts",
  bundle_func = function()
    return call({"hep-math-font"}, "pytest")
  end
}
