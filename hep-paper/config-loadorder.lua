-- Load-order tests: testfiles-loadorder/support/loadorder.tex loads the
-- packages in the order given by each test (that of hep-paper, reversed,
-- and with each package moved to the front and to the end) and records
-- results that must not depend on it. All .tlg files of one engine are
-- therefore identical.
testfiledir = "testfiles-loadorder"
testsuppdir = testfiledir .. "/support"

-- Fail if the saved results differ between load orders.
function checkinit_hook()
  local errorlevel = hep_unique_outputs()
  for _, engine in ipairs(checkengines) do
    local suffix = engine == stdengine and "" or "." .. engine
    local reference
    for _, file in ipairs(filelist(testfiledir, "*" .. suffix .. ".tlg")) do
      if suffix ~= "" or not file:match("%.%a+%.tlg$") then
        local f = assert(io.open(testfiledir .. "/" .. file, "rb"))
        local content = f:read("a")
        f:close()
        if not reference then
          reference = {file, content}
        elseif content ~= reference[2] then
          print("! " .. file .. " differs from " .. reference[1])
          errorlevel = 1
        end
      end
    end
  end
  return errorlevel
end
