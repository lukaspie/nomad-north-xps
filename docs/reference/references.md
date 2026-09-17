# References

## `NORTHTool` configuration

One entry point, `xps`, defined in [`src/nomad_north_xps/north_tools/__init__.py`](https://github.com/FAIRmat-NFDI/nomad-north-xps/blob/main/src/nomad_north_xps/north_tools/__init__.py){:target="_blank" rel="noopener"}. See the [`NORTHTool` reference](https://fairmat-nfdi.github.io/nomad-docs/reference/config.html#northtool){:target="_blank" rel="noopener"} for the full field list; the values used here:

| Field | Value | Meaning |
|---|---|---|
| `image` | `ghcr.io/fairmat-nfdi/nomad-north-xps/kherve:main` | Default, CI-published. Reconfigure via `nomad.yaml` to point at a local `casa` build instead — see [Explanation](../explanation/explanation.md) |
| `file_extensions` | `nxs`, `vms`, `npl`, `h5`, `hdf5`, `txt`, `spe`, `pro`, `ibw` | Formats either `pynxtools-xps` or KherveFitting read |
| `default_url` | `/desktop` | Opens into the `xfce` desktop session |
| `mount_path` | `/home/jovyan` | Where the triggering upload is mounted |
| `path_prefix` | `lab/tree` | With `with_path`, builds a link straight to the launched file |
| `with_path` | `true` | The triggering file is included in that URL |
| `image_pull_policy` | `Always` | Only honored by k8s-based NORTH deployments. `nomad-distro-dev`'s local Docker setup uses DockerSpawner directly, which NOMAD never wires this field into — DockerSpawner falls back to its own default (pull only if the tag isn't already present locally), which is why a bare local tag works without a failed registry pull |
| `privileged` | `false` | Neither tool needs elevated container privileges |
| `display_name` | `xps` | Name shown in NORTH's tool list |

## Entry point

```toml
xps_north_tool = "nomad_north_xps.north_tools:xps"
```

## Build directories

- `kherve` — `FROM ghcr.io/fairmat-nfdi/nomad-north-desktop-base:main`, installs `pynxtools[xps]` from PyPI.
- `casa` — `FROM` the `kherve` image, adds Wine + CasaXPS. Local build only; see its own README.

## CI

`.github/workflows/publish_north.yml` builds and publishes `kherve` only.

## Further reading

- [KherveFitting](https://github.com/KherveFitting/KherveFitting){:target="_blank" rel="noopener"}
- [CasaXPS](http://www.casaxps.com/){:target="_blank" rel="noopener"}
- [`pynxtools-xps`](https://github.com/FAIRmat-NFDI/pynxtools-xps){:target="_blank" rel="noopener"}
- [`nomad-north-mpes-igor`](https://github.com/FAIRmat-NFDI/nomad-north-mpes-igor){:target="_blank" rel="noopener"} — the sibling package `casa`'s local-build shape follows
- [NOMAD Docs > NORTH](https://fairmat-nfdi.github.io/nomad-docs/explanation/north.html){:target="_blank" rel="noopener"}
- [NOMAD Docs > How to create a NORTH tool](https://fairmat-nfdi.github.io/nomad-docs/howto/plugins/types/north_tools.html){:target="_blank" rel="noopener"}
