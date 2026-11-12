-- Template tests: compile the extracted hep-erc-B1.tex and hep-erc-B2.tex.
-- Any error halts the run before \END, which fails the test.
testfiledir  = "testfiles-templates"
checkengines = {"pdftex"}
checkopts    = "-interaction=nonstopmode -halt-on-error"
