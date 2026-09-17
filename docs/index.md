# Welcome to the `nomad-north-xps` documentation

`nomad-north-xps` is a NOMAD NORTH plugin for XPS peak-fitting GUI tools on top of the [`pynxtools-xps`](https://github.com/FAIRmat-NFDI/pynxtools-xps){:target="_blank" rel="noopener"} conversion tooling. It has one NORTH tool entry point, `xps`. By default, `xps` runs [KherveFitting](https://github.com/KherveFitting/KherveFitting){:target="_blank" rel="noopener"}, an open-source XPS peak fitting software. [CasaXPS](http://www.casaxps.com/){:target="_blank" rel="noopener"} can be installed via [Wine](https://www.winehq.org/) as well, but only as a local build — see [Explanation](explanation/explanation.md) for why, and [How-to > Build the Image](how_to/build_the_image.md) for how.

<div markdown="block" class="home-grid">
<div markdown="block">

### Tutorial

A short walkthrough of launching `xps` on a file inside a NOMAD Oasis.

- [Tutorial](tutorial/tutorial.md)

</div>
<div markdown="block">

### How-to guides

- [Build the Image](how_to/build_the_image.md)
- [Install this plugin](how_to/install_this_plugin.md)
- [Use this plugin](how_to/use_this_plugin.md)
- [Contribute to this plugin](how_to/contribute_to_this_plugin.md)
- [Contribute to the documentation](how_to/contribute_to_the_documentation.md)

</div>

<div markdown="block">

### Explanation

Overall architecture of this package, CasaXPS is a local build, and how the single `xps` entry point's image gets swapped for one with a licensed CasaXPS.
- [Explanation](explanation/explanation.md)

</div>
<div markdown="block">

### Reference

The `xps` entry point's configuration and what its image is built from.

- [Reference](reference/references.md)

</div>
</div>

<h2> Contact </h2>

For questions or suggestions:

- Open an issue on the [`nomad-north-xps` GitHub](https://github.com/FAIRmat-NFDI/nomad-north-xps/issues)
- Join our [Discord channel ](https://discord.gg/Gyzx3ukUw8)
- Get in contact with our [lead developers](contact.md).

<h2>Project and community</h2>

The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - [460197019 (FAIRmat)](https://gepris.dfg.de/gepris/projekt/460197019?language=en).
