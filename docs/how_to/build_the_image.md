# Build the Image

## `kherve`

Built and published automatically by CI on every push to `main` — most users never need to build it themselves. Build it locally when developing the Dockerfile or desktop-integration config:

```bash
docker build -f src/nomad_north_xps/north_tools/kherve/Dockerfile \
    -t nomad-north-xps-kherve:dev .
docker run --rm -p 8888:8888 nomad-north-xps-kherve:dev
```

Open `http://localhost:8888/desktop` — KherveFitting appears as a menu entry and Desktop icon.

## `casa`

Never CI-built — see [Explanation](../explanation/explanation.md) for why. Get CasaXPS yourself from [casaxps.com](http://www.casaxps.com/){:target="_blank" rel="noopener"} and follow the [`casa` build directory's own README](https://github.com/FAIRmat-NFDI/nomad-north-xps/blob/main/src/nomad_north_xps/north_tools/casa/README.md){:target="_blank" rel="noopener"} for the full build and license-activation procedure (confirmed working end-to-end, including how to verify a license actually carried through). Until `kherve` is published, build it locally first and pass it to `casa`'s build via `--build-arg BASE_IMAGE=nomad-north-xps-kherve --build-arg IMAGE_TAG=dev`.

## Using a local build

A local tag is enough to try this out — NOMAD checks for a local image before pulling from a registry. See [Install this Plugin](install_this_plugin.md) to point a running NOMAD at it.
