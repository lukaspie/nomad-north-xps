# Tutorial

This is a short walkthrough of launching `xps` on an XPS file from inside a NOMAD Oasis. It assumes the plugin is already installed and configured (see [How-to > Install this Plugin](../how_to/install_this_plugin.md)). By default this gives you KherveFitting — see [Explanation](../explanation/explanation.md) for how CasaXPS can be added via a local build.

## Prerequisites

- Access to a NOMAD Oasis with this plugin enabled and NORTH running.
- An upload containing at least one file with one of the supported extensions: `nxs`, `vms`, `npl`, `h5`, `hdf5`, `txt`, `spe`, `pro`, or `ibw`.

## Steps

1. **Open your upload.** In the NOMAD GUI, navigate to the upload that contains the XPS file you want to work with.
2. **Launch xps.** From the upload's file browser, open the tool launcher for that file (or the upload's list of available NORTH tools) and select **xps**. The first launch pulls and starts the container, which can take a moment.
3. **Work in the desktop.** NORTH opens a remote desktop session with your upload's files mounted and visible, and KherveFitting available from the desktop menu.
4. **Convert and fit.** If the file isn't already NeXus, convert it with `pynxtools-xps` first (see [How-to > Use this Plugin](../how_to/use_this_plugin.md)). Some of the file formats above can also be opened in KherveFitting to perform peak fitting.
5. **Save results back to the upload.** Files you save under the mounted upload directory become part of the upload and can be reprocessed like any other upload file.

!!! tip "Important"
    Anything you save outside the mounted upload directory is lost once the container session ends.
