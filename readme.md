# hep-paper

A LaTeX package for publications in High Energy Physics

The hep-paper package aims to provide a single style file containing most configurations and macros necessary to write appealing publications in High Energy Physics.
Instead of reinventing the wheel by introducing newly created macros hep-paper preferably loads third party packages as long as they are light weight enough.

For usual publications it is enough to load additionally to the |article| class without optional arguments only the |hep-paper| package.

    \documentclass{article}
    \usepackage{hep-paper}

The most notable changes after loading the |hep-paper| package is the change of some LaTeX defaults.