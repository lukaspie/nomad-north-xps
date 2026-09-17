# SPDX-FileCopyrightText: The nomad-north-xps Authors
#
# This file is part of nomad-north-xps.
#
# SPDX-License-Identifier: Apache-2.0

ARG BASE_IMAGE=ghcr.io/fairmat-nfdi/nomad-north-xps/kherve
ARG IMAGE_TAG=main

FROM ${BASE_IMAGE}:${IMAGE_TAG}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# ---- Wine (generic — copied from nomad-north-mpes-igor's mpes_igor Dockerfile; keep this
# block in sync if copied elsewhere) ----
RUN dpkg --add-architecture i386 \
 && mkdir -pm755 /etc/apt/keyrings \
 && wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key \
 && wget -nc -P /etc/apt/sources.list.d/ \
      https://dl.winehq.org/wine-builds/ubuntu/dists/$(lsb_release -sc)/winehq-$(lsb_release -sc).sources \
 && apt-get update -y \
 && apt-get install -y --install-recommends winehq-staging \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# icoutils (wrestool/icotool): extracts the desktop icon straight out of the user-supplied
# CasaXPS.exe at build time, below — same reasoning as the license capture. CasaXPS's own icon
# has no confirmed redistribution rights, so it's never committed to this repo either.
RUN apt-get update -y \
 && apt-get install -y --no-install-recommends icoutils \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}
WORKDIR "${HOME}"

ENV WINEDEBUG=-all

# Wine Mono (.NET runtime for Wine) is required for CasaXPS.exe to start at all — without it,
# Wine blocks on an interactive "Wine Mono Installer" GUI dialog on first launch. Installing the
# matching `.msi` silently (`msiexec ... /qn`) here means it's never needed again once
# casa-app/ is captured with a real CasaXPS install. If CasaXPS ever fails to start with a
# Mono-related error after a WineHQ version bump (winehq-staging is installed unpinned, always
# latest), check https://dl.winehq.org/wine/wine-mono/ for the version the new Wine release
# expects and bump WINE_MONO_VERSION below.
ENV WINE_MONO_VERSION=11.3.0
RUN wine wineboot --init \
 && wget -q -P "${HOME}/.cache/wine" \
      https://dl.winehq.org/wine/wine-mono/${WINE_MONO_VERSION}/wine-mono-${WINE_MONO_VERSION}-x86.msi \
 && wine msiexec /i "${HOME}/.cache/wine/wine-mono-${WINE_MONO_VERSION}-x86.msi" /qn \
 && wineserver -w

# CasaXPS itself — demo or licensed — is a locally-supplied build input, never committed (see
# this directory's README for why, and how to get one). This directory is gitignored except for
# a `.gitkeep`, so on a fresh checkout this COPY is a no-op and the image only has Wine + Mono.
# CasaXPS's own install notes say it needs read/write access to its own directory, so grant it
# explicitly rather than relying on whatever the local copy's permissions happened to be.
#
# Lives at the package root (`local/`), NOT under `src/` — a real Wine prefix's
# `dosdevices/z:` is a symlink to `/` (the host root, standard Wine behavior), and
# `setuptools`'s `where=["src"]` package auto-discovery follows symlinks while walking `src/`.
# With this directory under `src/`, every `uv sync`/editable install ran an unbounded recursive
# walk of the entire host filesystem through that symlink — not a slow build, one that never
# finishes. Keep both `casa-app/` and `casa-wine/` out of `src/` permanently.
COPY --chown=${NB_UID}:${NB_GID} local/casa-app/ "${HOME}/CasaXPS/"
RUN chmod -R u+rwX "${HOME}/CasaXPS"

# CasaXPS stores its license under HKEY_CURRENT_USER\Software\Casa Software Ltd
# Applications\CasaXPS — not next to CasaXPS.exe. Under Wine that key lives in the prefix's own
# registry hive (~/.wine/user.reg), so activation requires overlaying a captured prefix here,
# not just the CasaXPS folder above. Same gitignored/`.gitkeep`-only-by-default shape.
COPY --chown=${NB_UID}:${NB_GID} local/casa-wine/ "${HOME}/.wine/"

# Menu entry and desktop icon. The icon is extracted from CasaXPS.exe itself, not committed to
# this repo (see the icoutils install above) — a no-op if casa-app/ is still empty.
RUN mkdir -p "${HOME}/.local/share/applications" "${HOME}/Desktop" \
             "${HOME}/.local/share/icons/hicolor/32x32/apps"
# CasaXPS.exe ships two RT_GROUP_ICON resources (`wrestool -l`: name=128 and name=129).
# name=128 is the actual application icon (house mark, "XPS"); name=129 is an unrelated
# ISO-19775 file-association badge. Extracting without `-n128` pulls whichever one `icotool`
# happens to expand first, not necessarily the app icon — pin it explicitly.
RUN if [ -f "${HOME}/CasaXPS/CasaXPS.exe" ]; then \
      mkdir -p /tmp/CasaXPS-icons \
   && wrestool -x -t14 -n128 "${HOME}/CasaXPS/CasaXPS.exe" -o /tmp/CasaXPS.ico \
   && icotool -x -o /tmp/CasaXPS-icons /tmp/CasaXPS.ico \
   && cp $(ls /tmp/CasaXPS-icons/*32x32*.png 2>/dev/null | head -1 \
           || ls -S /tmp/CasaXPS-icons/*.png | head -1) \
         "${HOME}/.local/share/icons/hicolor/32x32/apps/CasaXPS.png" \
   && rm -rf /tmp/CasaXPS.ico /tmp/CasaXPS-icons; \
    fi
COPY --chown=${NB_UID}:${NB_GID} src/nomad_north_xps/north_tools/casa/config/CasaXPS.desktop "${HOME}/.local/share/applications/CasaXPS.desktop"
COPY --chown=${NB_UID}:${NB_GID} src/nomad_north_xps/north_tools/casa/config/CasaXPS.desktop "${HOME}/Desktop/CasaXPS.desktop"
RUN chmod 755 "${HOME}/.local/share/applications/CasaXPS.desktop" "${HOME}/Desktop/CasaXPS.desktop"

WORKDIR "${HOME}"

EXPOSE 8888
