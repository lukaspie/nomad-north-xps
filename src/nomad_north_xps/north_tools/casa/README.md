# `casa` - NORTH tool (local build only)

Dockerfile for [CasaXPS](http://www.casaxps.com/) via Wine, layered `FROM` the `kherve` image. Unlike `kherve`, this is never built by CI and never published — CasaXPS is a commercial product, and even its free demo has no confirmed redistribution terms. Build it yourself, locally, with your own copy of CasaXPS.

## Get CasaXPS

Download it yourself from [casaxps.com](http://www.casaxps.com/) (a free demo is available). Extract it into `casa-app/` in this directory:

```
src/nomad_north_xps/north_tools/casa/casa-app/CasaXPS.exe
src/nomad_north_xps/north_tools/casa/casa-app/CasaXPS.DEF/...
...
```

`casa-app/` is gitignored except for a `.gitkeep` — nothing there ever gets committed.

## Build and run

`kherve` isn't published yet, so point `BASE_IMAGE`/`IMAGE_TAG` at a local `kherve` build instead of the default `ghcr.io/...` reference (build that first if you haven't — see [How-to > Build the Image](https://fairmat-nfdi.github.io/nomad-north-xps/how_to/build_the_image.html)):

```bash
docker build -f src/nomad_north_xps/north_tools/casa/Dockerfile \
    --build-arg BASE_IMAGE=nomad-north-xps-kherve --build-arg IMAGE_TAG=dev \
    -t nomad-north-xps-casa:dev .
docker run --rm -p 8888:8888 nomad-north-xps-casa:dev
```

Open `http://localhost:8888/desktop` — CasaXPS appears as a menu entry and Desktop icon.

Once `kherve` is published, drop the two `--build-arg` flags; the Dockerfile's defaults will resolve it from the registry.

## Activating a real license

Confirmed working end-to-end:

1. Open CasaXPS from its desktop icon and enter your key in its own registration dialog.
2. Copy whatever changed back out, to both gitignored override directories:
   ```bash
   docker cp <container>:/home/jovyan/CasaXPS/. \
       src/nomad_north_xps/north_tools/casa/casa-app/
   docker cp <container>:/home/jovyan/.wine/. \
       src/nomad_north_xps/north_tools/casa/casa-wine/
   ```
3. Rebuild (same command as above, new tag):
   ```bash
   docker build -f src/nomad_north_xps/north_tools/casa/Dockerfile \
       --build-arg BASE_IMAGE=nomad-north-xps-kherve --build-arg IMAGE_TAG=dev \
       -t nomad-north-xps-casa-licensed:dev .
   ```
   The Dockerfile's `COPY` steps overlay both directories on top of the freshly-built Wine prefix and CasaXPS install.

CasaXPS stores its license in the registry, under `HKEY_CURRENT_USER\Software\Casa Software Ltd Applications\CasaXPS` — not next to `CasaXPS.exe`. Step 2's first `docker cp` (the `CasaXPS/` folder) only ships the program files themselves; the second `docker cp` (the whole `.wine` prefix) is the one that actually carries the license, since that's where Wine keeps its virtualized `HKEY_CURRENT_USER` hive (`~/.wine/user.reg`). Don't skip it.

### Verify it worked

Run a fresh container from the image you just built and check the registry value directly:

```bash
docker run -d --rm --name casa-verify -p 8888:8888 nomad-north-xps-casa-licensed:dev
docker exec casa-verify grep '"CasaXPS License"' /home/jovyan/.wine/user.reg
docker rm -f casa-verify
```

`"CasaXPS License"="demo only"` means the capture didn't take (check you actually activated before copying, and that both `docker cp` commands ran against the *same* container). Anything else there is your real license key.

## Point NOMAD at it

Same `xps` entry point as `kherve` — override its image in `nomad.yaml`:

```yaml
plugins:
  entry_points:
    options:
      nomad_north_xps.north_tools:xps:
        north_tool:
          image: nomad-north-xps-casa-licensed:dev
```

Restart NOMAD for the change to take effect, then relaunch **xps** from NORTH. See [How-to > Install this Plugin](https://fairmat-nfdi.github.io/nomad-north-xps/how_to/install_this_plugin.html) for the general mechanism.
