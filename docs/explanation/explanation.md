# Explanation

## What this package is

`nomad-north-xps` has one NORTH tool entry point, `xps`, and two build directories in `src/nomad_north_xps/north_tools/`:

- `kherve` — KherveFitting. CI-built and published. This is what `xps`'s `image` points at by default.
- `casa` — CasaXPS via [Wine](https://www.winehq.org/), layered `FROM` the `kherve` image. It is never buil in the CI, but you can build it yourself, locally.

Only one entry point exists regardless of which image is running — `casa` never appears as a separate tool in NORTH's launcher. Point `xps` at a `casa` build via `nomad.yaml` instead (see [How-to > Install this Plugin](../how_to/install_this_plugin.md)).

## Why standalone, not embedded in `pynxtools-xps`

We do not embed the NORTH tool for XPS analysis together with the `pynxtools-xps` NeXus conversion package. `pynxtools-xps` is already substantially complexx (six vendor-specific parser families plus its own NOMAD app). Embedding would couple this image's release cycle to `pynxtools-xps`'s own parser and app releases for no benefit. Most `nomad-north-*` sibling are standalone — this package follows that convention. The `kherve` image installs `pynxtools[xps]` from PyPI like any other dependency.

## Why CasaXPS is a local build, not CI-built

CasaXPS is a commercial product with paid licenses. It has a free demo, but "free to download" isn't the same as "free to redistribute inside a public Docker image," and no redistribution terms were found anywhere (not in the download, not on the vendor's site). Rather than assume it's fine, `casa` stays local-only.

## Wine, Wine Mono, and where CasaXPS keeps its license

`CasaXPS.exe` is a native Windows executable; it runs under Wine (confirmed by actually launching it). It needs Wine Mono (the .NET runtime Wine substitutes for real .NET) to start; without it, Wine blocks on an interactive install dialog on first launch. The `casa` Dockerfile installs the matching Mono `.msi` silently at build time.

CasaXPS stores an activated license in the registry, under `HKEY_CURRENT_USER\Software\Casa Software Ltd Applications\CasaXPS` — not next to `CasaXPS.exe`. Under Wine that's the prefix's own registry hive (`~/.wine/user.reg`), which is why activating a license means capturing the whole Wine prefix, not just the CasaXPS folder — see the `casa` build directory's own README.
