# How to Use This Plugin

This plugin can be used in a NOMAD Oasis installation that has this plugin installed — see [Install this Plugin](install_this_plugin.md) if that hasn't happened yet.

## Launching xps

**xps** shows up in NORTH's tool launcher for any file in an upload with one of these extensions: `nxs`, `vms`, `npl`, `h5`, `hdf5`, `txt`, `spe`, `pro`, `ibw` — the formats `pynxtools-xps` and KherveFitting both read. Selecting it starts a container with:

- [KherveFitting](https://github.com/KherveFitting/KherveFitting){:target="_blank" rel="noopener"}, available as a desktop menu entry and icon, opened directly into the desktop (`default_url: /desktop`);
- `pynxtools[xps]` conversion tooling, for converting vendor-specific raw files to NeXus (`.nxs`) before peak fitting;
- the triggering upload mounted at `/home/jovyan`, visible from KherveFitting's own file dialogs.

If your deployment points `xps` at a local `casa` build instead (see [Explanation](../explanation/explanation.md)), CasaXPS appears alongside KherveFitting on the same desktop.

## A typical workflow

1. Convert a vendor-specific XPS export (VAMAS, SPECS, Scienta, Kratos, Phi) to NeXus using `pynxtools-xps` (see [its own docs](https://fairmat-nfdi.github.io/pynxtools-xps/){:target="_blank" rel="noopener"}), if it isn't already.
2. Open KherveFitting (or CasaXPS) from the desktop menu and load the file.
3. Fit peaks interactively — background subtraction, component fitting, quantification.
4. Save results under the mounted upload directory.

!!! note "Attention"
    Only files saved under the mounted upload directory persist as part of the upload. Anything written elsewhere in the container is lost when the session ends.
