-- Shared l3build configuration of the hep-paper bundle.
--
-- Every package directory has a build.lua of the form
--
--   module  = "hep-xyz"
--   maindir = ".."
--   dofile(maindir .. "/support/common.lua")
--
-- followed by package-specific settings. The packages are released to CTAN
-- independently, so each is a standalone l3build module (bundle = "").

bundle = ""

-- All packages of the bundle. The documentation of every package loads
-- hep-paper, which loads most of the others, so documentation and tests
-- depend on all of them.
hep_modules = dofile(maindir .. "/support/modules.lua")

-- Each package gets its own build directory so that unpacking a dependency
-- does not clobber the files of the package being built. The unpacked
-- packages are collected in a single shared local tree.
builddir = maindir .. "/build/" .. module
localdir = maindir .. "/build/local"

-- Files
sourcefiles  = {"*-implementation.dtx", "*.ins"}
unpackfiles  = {"*.ins"}
installfiles = {"*.sty", "*.cls", "*.dbx"}
typesetfiles = {"*-implementation.dtx", "*-documentation.tex"}
typesetsuppfiles = {"bibliography.bib"}
textfiles    = {"README-" .. module .. ".md"}
ctanreadme   = "README-" .. module .. ".md"
tagfiles     = {"*-implementation.dtx"}
cleanfiles   = {"*-documentation.pdf", "*-implementation.pdf", "*.zip"}
-- Only the module's own PDFs go into the CTAN zip, not stale ones that
-- happen to lie in the package directory.
pdffiles     = {module .. "-documentation.pdf", module .. "-implementation.pdf"}

-- Dependencies: every other package of the bundle
local deps = {}
for _, name in ipairs(hep_modules) do
  if name ~= module then
    table.insert(deps, maindir .. "/" .. name)
  end
end
typesetdeps = deps
checkdeps   = deps

-- Typesetting: pdfLaTeX, biber and the doc package index styles (defaults)
typesetexe  = "pdflatex"
typesetopts = "-interaction=nonstopmode -halt-on-error"
typesetruns = 3

-- Tests
checkengines = {"pdftex", "luatex"}
checkruns    = 1
checkopts    = "-interaction=nonstopmode"
-- Helpers shared by all tests: \input{hep-regression}
checksuppfiles = {"hep-regression.tex"}

-- Only the log between \START and \END is compared, so errors in the
-- preamble of a test would go unnoticed. Append them to the normalised log,
-- so that they appear in the .tlg and any new one fails the test.
test_types = test_types or {}
test_types.log = {
  test        = ".lvt",
  generated   = ".log",
  reference   = ".tlg",
  expectation = ".lve",
  compare     = function(...) return compare_tlg(...) end,
  rewrite     = function(source, result, engine, errlevels)
    local errorlevel = rewrite_log(source, result, engine, errlevels)
    local errors = {}
    local f = io.open(source, "rb")
    if f then
      for line in f:lines() do
        if line:match("START%-TEST%-LOG") then break end
        if line:match("^! ") then table.insert(errors, line) end
      end
      f:close()
    end
    if #errors > 0 then
      f = assert(io.open(result, "ab"))
      f:write("Errors before \\START:\n", table.concat(errors, "\n"), "\n")
      f:close()
    end
    return errorlevel
  end,
}

-- The pdfTeX virtual fonts and the accent font of hep-math-font are
-- generated during its unpack step and copied to the shared local tree.
-- Make them visible to every TeX run started by l3build.
do
  local dir = (function()
    local lfs = require("lfs")
    local here = lfs.currentdir()
    return here .. "/" .. localdir
  end)()
  for _, var in ipairs({"TFMFONTS", "VFFONTS", "ENCFONTS", "TEXFONTMAPS",
                         "TTFONTS"}) do
    os.setenv(var, dir .. ":")
  end
end

-- CTAN: the tarball contains the sources, both PDFs, the README, the
-- shared bibliography of the documentation and the license. There is no
-- TDS zip unless a package sets packtdszip = true.
packtdszip = false
local copyctan_files = copyctan
function copyctan()
  copyctan_files()
  local pkgdir = ctandir .. "/" .. ctanpkg
  cp("license.md", maindir, pkgdir)
  cp("bibliography.bib", supportdir, pkgdir)
end

-- l3build upload [in a package directory, after l3build ctan] sends the
-- zip to CTAN. Version and date come from the \Provides line of the
-- package, the announcement from the \changes entries of that version and
-- date (override with --message or --file). l3build validates the
-- upload first and asks before submitting; --dry-run only validates. New
-- packages are detected by l3build. The summary (CTAN one-liner) is the
-- description in the \Provides line, which the README repeats. Packages set
-- ctanPath and topic in their build.lua.
local hep_text_macros = {
  software = true, option = true, texttt = true, textsf = true, emph = true,
  pkg = true, env = true, file = true, hologo = true,
}
local function hep_release()
  local f = io.open(module .. "-implementation.dtx", "rb")
  if not f then return end
  local dtx = f:read("a")
  f:close()
  local date, version, summary = dtx:match("\\Provides%a+{"
    .. module:gsub("%p", "%%%0") .. "}%[(%d%d%d%d/%d%d/%d%d) v([%d.]+) ([^]]*)%]")
  if not date then return end
  local changes = {}
  for v, d, text in dtx:gmatch("\\changes%s*{v([%d.]+)}%s*{([%d/]+)}%s*(%b{})") do
    if v == version and d == date then
      text = text:sub(2, -2)
        :gsub("\\cs(%b{})", function(name) return "\\" .. name:sub(2, -2) end)
        :gsub("\\marg(%b{})", "%1")
        :gsub("\\TeX{}", "TeX"):gsub("\\TeX", "TeX")
        :gsub("\\NCM", "New Computer Modern"):gsub("\\CM", "Computer Modern")
        :gsub("\\LM", "Latin Modern"):gsub("\\PDF%f[^%a]", "PDF")
        :gsub("\\(%a+)(%b{})", function(name, arg)
          if hep_text_macros[name] then return arg:sub(2, -2) end
        end)
      table.insert(changes, text)
    end
  end
  return version .. " " .. date:gsub("/", "-"), table.concat(changes, "\n\n"),
    summary
end
local hep_version, hep_announcement, hep_summary = hep_release()
uploadconfig = {
  pkg          = module,
  version      = hep_version,
  summary      = hep_summary,
  author       = "Jan Hajer",
  uploader     = "Jan Hajer",
  email        = "jan@hajer.com",
  license      = "lppl1.3c",
  announcement = hep_announcement ~= "" and hep_announcement or nil,
  repository   = "https://github.com/janhajer/hep-paper",
  bugtracker   = "https://github.com/janhajer/hep-paper/issues",
}

-- l3build tag vM.N [in a package directory] updates the date and version
-- of all \ProvidesPackage, \ProvidesClass and \ProvidesFile lines.
-- The \changes entry and the \CheckSum remain manual.
function update_tag(file, content, tagname, tagdate)
  if not tagname or not tagname:match("^v%d+%.%d+$") then
    print("Usage: l3build tag vM.N")
    os.exit(1)
  end
  local date = tagdate:gsub("-", "/")
  return (content:gsub(
    "(\\Provides%a+%*?{[^}]+}%[)%d%d%d%d/%d%d/%d%d v[%d.]+",
    "%1" .. date .. " " .. tagname))
end

-- l3build coverage [at the root or in a package directory] lists the
-- documented user commands, environments and options (\DescribeMacro,
-- \DescribeEnv in the .dtx) that no regression test of the bundle uses.
-- It only reports; it never fails. A package can exclude names that are
-- not user interfaces (e.g. margin labels) with coverageexclude = {...}.
local function hep_read(path)
  local f = io.open(path, "rb")
  if not f then return "" end
  local s = f:read("a")
  f:close()
  return s
end
local function hep_coverage()
  local tests = {}
  local lfs = require("lfs")
  for _, name in ipairs(hep_modules) do
    -- testfiles and further test configurations (testfiles-journals, ...)
    local pkgdir = maindir .. "/" .. name
    for entry in lfs.dir(pkgdir) do
      if entry:match("^testfiles") then
        local dir = pkgdir .. "/" .. entry
        for _, file in ipairs(filelist(dir, "*.lvt")) do
          table.insert(tests, hep_read(dir .. "/" .. file))
        end
      end
    end
  end
  tests = table.concat(tests, "\n")
  local seen, missing, total = {}, {}, 0
  for _, name in ipairs(coverageexclude or {}) do seen[name] = true end
  for _, file in ipairs(filelist(".", "*-implementation.dtx")) do
    local dtx = hep_read(file)
    for kind, name in dtx:gmatch("\\Describe(%a+)%s*{?%s*(\\?[%w@*-]+)") do
      if (kind == "Macro" or kind == "Env") and not seen[name] then
        seen[name] = true
        total = total + 1
        local used
        if name:sub(1, 1) == "\\" then
          -- a command: \name not followed by a letter, or the bare name
          -- in a comma list (\@for loops, \DEFINED{Jan,Feb})
          local bare = name:sub(2):gsub("%p", "%%%0")
          used = tests:find("\\" .. bare .. "%f[^%a]") ~= nil
            or tests:find("[{=,]%s*" .. bare .. "%s*[,}]") ~= nil
        else
          -- an environment or option: the bare word
          local pattern = "%f[%w]" .. name:gsub("%p", "%%%0")
          if name:match("%w$") then pattern = pattern .. "%f[^%w]" end
          used = tests:find(pattern) ~= nil
        end
        if not used then table.insert(missing, name) end
      end
    end
  end
  print(string.format("%s: %d of %d documented names used in tests",
    module, total - #missing, total))
  if #missing > 0 then
    print("  untested: " .. table.concat(missing, " "))
  end
  return 0
end
target_list.coverage = {
  desc = "Lists documented commands that no test uses",
  func = hep_coverage,
}

-- Generated files must be unique across the bundle: if two .ins files
-- write the same file, the result depends on the order in which the
-- packages are unpacked. Checked before every test run.
function hep_unique_outputs()
  local lfs = require("lfs")
  local owner, errorlevel = {}, 0
  for _, name in ipairs(hep_modules) do
    local dir = maindir .. "/" .. name
    for entry in lfs.dir(dir) do
      if entry:match("%.ins$") then
        local ins = hep_read(dir .. "/" .. entry)
        for file in ins:gmatch("\\file%s*{([^}]+)}") do
          local here = name .. "/" .. entry
          if owner[file] and owner[file] ~= here then
            print("! " .. file .. " is generated by both "
              .. owner[file] .. " and " .. here)
            errorlevel = 1
          end
          owner[file] = here
        end
      end
    end
  end
  return errorlevel
end
function checkinit_hook()
  return hep_unique_outputs()
end

-- Private packages (hep-cv-private, hep-erc) are built, tested and
-- installed, but never released: their ctan and upload targets do nothing.
function hep_private()
  local function skip()
    print(module .. " is private and not released to CTAN")
    return 0
  end
  target_list.ctan.func = skip
  target_list.upload.func = skip
end
