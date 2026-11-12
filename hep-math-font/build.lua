-- l3build configuration of hep-math-font (shared settings: ../support/common.lua)
module  = "hep-math-font"
maindir = ".."
dofile(maindir .. "/support/common.lua")

-- The pdfTeX virtual fonts and the accent font are generated from the
-- glyph tables in hep-math-font.sty by hep-math-font-vf.py (python3 with
-- fontTools). They are installed with the package and shipped in the TDS
-- zip.
installfiles = {"*.sty", "*.tfm", "*.vf", "*.enc", "*.map", "*.ttf"}
tdslocations = {
  "fonts/truetype/public/hep-math-font/*.ttf",
  "fonts/tfm/public/hep-math-font/*.tfm",
  "fonts/vf/public/hep-math-font/*.vf",
  "fonts/enc/dvips/hep-math-font/*.enc",
  "fonts/map/pdftex/hep-math-font/*.map",
}
packtdszip = true

-- Generating the fonts takes about 20 seconds and every other package
-- unpacks this one as a dependency, so the result is cached and reused as
-- long as the style file and the generator are unchanged.
local fontcache = maindir .. "/build/font-cache"
local fontglobs = {"*.tfm", "*.vf", "*.enc", "*.map", "*.ttf"}
local fontinputs = {"hep-math-font.sty", "hep-math-font-vf.py"}

local function content(path)
  local file = io.open(path, "rb")
  if not file then return nil end
  local text = file:read("a")
  file:close()
  return text
end

local unpack_sources = bundleunpack
function bundleunpack(sourcedirs, sources)
  local errorlevel = unpack_sources(sourcedirs, sources)
  if errorlevel ~= 0 then return errorlevel end
  local cached = true
  for _, name in ipairs(fontinputs) do
    local new = content(unpackdir .. "/" .. name)
    if not new or new ~= content(fontcache .. "/" .. name) then
      cached = false
    end
  end
  if cached then
    for _, glob in ipairs(fontglobs) do
      errorlevel = errorlevel + cp(glob, fontcache, unpackdir)
    end
    return errorlevel
  end
  print("Generating the pdfTeX virtual fonts of hep-math-font")
  errorlevel = run(unpackdir,
    "python3 hep-math-font-vf.py > " .. os_null .. " 2>&1")
  if errorlevel ~= 0 then
    print("! hep-math-font-vf.py failed; run it in " .. unpackdir)
    return errorlevel
  end
  errorlevel = mkdir(fontcache) + cleandir(fontcache)
  for _, glob in ipairs(fontglobs) do
    errorlevel = errorlevel + cp(glob, unpackdir, fontcache)
  end
  for _, name in ipairs(fontinputs) do
    errorlevel = errorlevel + cp(name, unpackdir, fontcache)
  end
  return errorlevel
end


-- The package supports XeLaTeX, so the tests also run with XeTeX
-- (results in <name>.xetex.tlg where they differ from pdfTeX).
checkengines = {"pdftex", "luatex", "xetex"}

-- The Python regression tests in tests/ (python3 with fontTools, pdffonts
-- and pdftotext) compile documents against the packages and fonts in the
-- shared local tree. `l3build pytest` unpacks hep-font and hep-math-font
-- and runs them; a full `l3build check` (no test names, no -e) runs them
-- after the TeX tests. Each script's output is kept in
-- build/python-tests/<name>.out.
local pytests = {"hep_options", "hep_integration", "hep_toc", "hep_pdf",
                 "run", "outlines"}

local function pytest()
  local errorlevel = dep_install({maindir .. "/hep-font"}) + unpack()
  if errorlevel ~= 0 then return errorlevel end
  local outdir = maindir .. "/build/python-tests"
  errorlevel = mkdir(outdir)
  local failed = {}
  for _, name in ipairs(pytests) do
    local out = abspath(outdir) .. "/" .. name .. ".out"
    local status = run(".", "python3 tests/" .. name .. ".py > \""
      .. out .. "\" 2>&1")
    local lines = {}
    for line in (content(out) or ""):gmatch("[^\n]+") do
      table.insert(lines, line)
    end
    if status == 0 then
      print("  " .. name .. ": " .. (lines[#lines] or "passed"))
    else
      print("  " .. name .. ": FAILED (" .. out .. ")")
      for i = math.max(1, #lines - 9), #lines do
        print("    " .. lines[i])
      end
      table.insert(failed, name)
    end
  end
  if #failed > 0 then
    print("\n  Python tests failed: " .. table.concat(failed, " "))
    return 1
  end
  print("\n  All Python tests passed")
  return errorlevel
end

target_list.pytest = {
  desc = "Runs the Python regression tests of the math fonts",
  func = pytest,
}

-- `bundlecheck` is what a check at the root runs in each package.
for _, target in ipairs({"check", "bundlecheck"}) do
  local check_tex = target_list[target].func
  target_list[target].func = function(names)
    local full = not (names and next(names)) and not options["engine"]
    local errorlevel = check_tex(names)
    if full then
      print("\nRunning the Python tests")
      errorlevel = errorlevel + pytest()
    end
    return errorlevel
  end
end

-- CTAN upload (shared fields in ../support/common.lua)
uploadconfig.ctanPath = "/fonts/utilities/hep-math-font"
uploadconfig.topic = {"font-supp-maths", "font", "font-mgmt", "font-use"}
