# Build the Image

## `kherve` — KherveFitting

Built and published automatically by CI on every push to `main` — most users never need to build it themselves. Build it locally when developing the Dockerfile or desktop-integration config:

```bash
docker build -f src/nomad_north_xps/north_tools/kherve/Dockerfile \
    -t nomad-north-xps-kherve:dev .
docker run --rm -p 8888:8888 nomad-north-xps-kherve:dev
```

Open `http://localhost:8888/desktop` — KherveFitting appears as a menu entry and Desktop icon.

## `casa` — CasaXPS

This image is never built in the CI because the software is proprietary.

### Get CasaXPS

Download it yourself from [casaxps.com](http://www.casaxps.com/){:target="_blank" rel="noopener"} (a free demo is available). Extract it into `local/casa-app/` at the package root:

```
local/casa-app/CasaXPS.exe
local/casa-app/CasaXPS.DEF/...
...
```

`local/casa-app/` is gitignored except for a `.gitkeep` — nothing there ever gets committed. It
deliberately lives outside `src/`, not next to the Dockerfile: a real Wine prefix (see
`local/casa-wine/` below) contains a symlink to the host filesystem root, and Python packaging
tools that scan `src/` follow symlinks while walking it — see the comment in `casa/Dockerfile`
for what that caused.

### Build and run

`casa`'s Dockerfile starts `FROM` `kherve` — point it at whichever `kherve` image you actually have:

=== "kherve from the registry"

    `kherve`'s defaults resolve it from `ghcr.io` :

    ```bash
    docker build -f src/nomad_north_xps/north_tools/casa/Dockerfile \
        -t nomad-north-xps-casa:dev .
    docker run --rm -p 8888:8888 nomad-north-xps-casa:dev
    ```

=== "kherve built locally"

    Build `kherve` first (see above), then point `BASE_IMAGE`/`IMAGE_TAG` at that local tag:

    ```bash
    docker build -f src/nomad_north_xps/north_tools/casa/Dockerfile \
        --build-arg BASE_IMAGE=nomad-north-xps-kherve --build-arg IMAGE_TAG=dev \
        -t nomad-north-xps-casa:dev .
    docker run --rm -p 8888:8888 nomad-north-xps-casa:dev
    ```

Open `http://localhost:8888/desktop` — CasaXPS appears as a menu entry and Desktop icon.

### Activating a real license

1. Open CasaXPS from its desktop icon and enter your key in its own registration dialog.
2. Copy whatever changed back out, to both gitignored override directories:
   ```bash
   docker cp <container>:/home/jovyan/CasaXPS/. local/casa-app/
   docker cp <container>:/home/jovyan/.wine/. local/casa-wine/
   ```
3. Rebuild (same build command as above — with or without the `--build-arg` flags, whichever variant you used — here we use a **different** tag for the licensed image):
   ```bash
   docker build -f src/nomad_north_xps/north_tools/casa/Dockerfile \
       -t nomad-north-xps-casa-licensed:dev .
   ```
   The Dockerfile's `COPY` steps overlay both directories on top of the freshly built Wine prefix and CasaXPS install.

CasaXPS stores its license in the registry, under `HKEY_CURRENT_USER\Software\Casa Software Ltd Applications\CasaXPS` — not next to `CasaXPS.exe`. Step 2's first `docker cp` (the `CasaXPS/` folder) only ships the program files themselves; the second `docker cp` (the whole `.wine` prefix) is the one that actually carries the license, since that's where Wine keeps its virtualized `HKEY_CURRENT_USER` hive (`~/.wine/user.reg`). Don't skip it.

#### Verify it worked

Run a fresh container from the image you just built and check the registry value directly:

```bash
docker run -d --rm --name casa-verify -p 8888:8888 nomad-north-xps-casa-licensed:dev
docker exec casa-verify grep '"CasaXPS License"' /home/jovyan/.wine/user.reg
docker rm -f casa-verify
```

`"CasaXPS License"="demo only"` means the capture didn't work (check that you actually activated in the original container before copying, and that both `docker cp` commands ran against the *same* container).

## Using a local build

A local tag is enough to try this out — the local Docker setup this repo uses only pulls a tag from a registry if it isn't already present locally (see [Reference](../reference/references.md#northtool-configuration)). See [Install this Plugin](install_this_plugin.md) to point a running NOMAD at it.
