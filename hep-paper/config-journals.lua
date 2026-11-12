-- Journal compatibility tests: the generated hep-paper-test-*.tex documents
-- with the journal classes and styles in testfiles-journals/support.
-- Any error halts the run before \END, which fails the test.
testfiledir  = "testfiles-journals"
testsuppdir  = testfiledir .. "/support"
checkfiles   = {"hep-paper-test-*.tex"}
checkengines = {"pdftex"}
checkopts    = "-interaction=nonstopmode -halt-on-error"
