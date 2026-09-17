# nomad-north-xps

NOMAD NORTH plugin bundling XPS peak-fitting GUI tools.

## About

This is a NOMAD plugin for GUI tools used for peak-fitting in X-ray Photoelectron Spectroscopy (XPS). It registers one NORTH tool entry point, `xps`. By default it runs [KherveFitting](https://github.com/KherveFitting/KherveFitting), an open-source XPS peak fitting tool. [CasaXPS](http://www.casaxps.com/), a commercial XPS analysis tool, can be added via [Wine](https://www.winehq.org/), but only as a local build. It is never CI-built or published, since its licensing terms don't give redistribution rights. See the [documentation](https://fairmat-nfdi.github.io/nomad-north-xps/) for how.

## Docs

More information about this plugin is available in the [documentation](https://fairmat-nfdi.github.io/nomad-north-xps/), including how to [build the image](https://fairmat-nfdi.github.io/nomad-north-xps/how_to/build_the_image/).

## Adding this plugin to NOMAD

Currently, NOMAD has two distinct flavors that are relevant depending on your role as an user:
1. [A NOMAD Oasis](#adding-this-plugin-in-your-nomad-oasis): any user with a NOMAD Oasis instance.
2. [Local NOMAD installation and the source code of NOMAD](#adding-this-plugin-in-your-local-nomad-installation-and-the-source-code-of-nomad): internal developers.

### Adding this plugin in your NOMAD Oasis

Read the [NOMAD plugin documentation](https://nomad-lab.eu/prod/v1/staging/docs/howto/oasis/plugins_install.html) for all details on how to deploy the plugin on your NOMAD instance.

### Adding this plugin in your local NOMAD installation and the source code of NOMAD

We now recommend using the dedicated [`nomad-distro-dev`](https://github.com/FAIRmat-NFDI/nomad-distro-dev) repository to simplify the process. Please refer to that repository for detailed instructions.

### Template update

This `nomad` plugin was generated with `Cookiecutter` along with `@nomad`'s [`cookiecutter-nomad-plugin`](https://github.com/FAIRmat-NFDI/cookiecutter-nomad-plugin) template.

We use [`cruft`](https://github.com/cruft/cruft) to update the project based on template changes. To run the check for updates locally, run `cruft update` in the root of the project. More details see the instructions on [`cruft` website](https://cruft.github.io/cruft/#updating-a-project).

## Main contributors

| Name | E-mail     |
|------|------------|
| Lukas Pielsticker | [lukas.pielsticker@physik.hu-berlin.de](mailto:lukas.pielsticker@physik.hu-berlin.de)
