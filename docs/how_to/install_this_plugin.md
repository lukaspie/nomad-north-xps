# Install This Plugin

## In your NOMAD Oasis

If your Oasis is built from [`nomad-distro-template`](https://github.com/FAIRmat-NFDI/nomad-distro-template){:target="_blank" rel="noopener"}, add `nomad-north-xps` as a dependency in your distro project's `pyproject.toml`, then rebuild and redeploy the Oasis image. See the [template README > Adding a plugin](https://github.com/FAIRmat-NFDI/nomad-distro-template?tab=readme-ov-file#adding-a-plugin){:target="_blank" rel="noopener"}.

## In `nomad-distro-dev`

Add `nomad-north-xps` as a workspace dependency — see the [`nomad-distro-dev`](https://github.com/FAIRmat-NFDI/nomad-distro-dev){:target="_blank" rel="noopener"} README.

## Default setup

Nothing to configure. The `xps` entry point's `image` already points at the CI-published `ghcr.io/fairmat-nfdi/nomad-north-xps/kherve:main`. Restart NOMAD and **xps** appears in NORTH's tool launcher — see [Use this Plugin](use_this_plugin.md).

## Using a local build (development, or CasaXPS)

Override the entry point's `image` via `nomad.yaml`:

```yaml
plugins:
  entry_points:
    options:
      nomad_north_xps.north_tools:xps:
        north_tool:
          image: nomad-north-xps-casa:dev # or any other local build tag
```

Use the entry point's full `<module>:<object>` path (matching `[project.entry-points.'nomad.plugin']` in `pyproject.toml`), not the short name.

See [Build the Image](build_the_image.md) for building `kherve` or `casa` locally, [Reference](../reference/references.md#northtool-configuration) for the other fields you can override, and the NOMAD docs' [NORTH tools how-to](https://fairmat-nfdi.github.io/nomad-docs/explanation/north.html#how-to-connect-and-use-specific-north-tools-in-a-nomad-deployment) for the general mechanism.
