# SPDX-FileCopyrightText: The nomad-north-xps Authors
#
# This file is part of nomad-north-xps.
#
# SPDX-License-Identifier: Apache-2.0

ARG UV_VERSION=0.9
ARG BASE_IMAGE=ghcr.io/fairmat-nfdi/nomad-north-desktop-base
ARG IMAGE_TAG=main

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_stage

FROM ${BASE_IMAGE}:${IMAGE_TAG}

COPY --from=uv_stage /uv /uvx /bin/

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# git: KherveFitting has no pyproject.toml/setup.py and is not published on PyPI (a plain
# script + requirements.txt) — installed by cloning, not `pip install`.
# libgtk-3-0/libsdl2-2.0-0/libnotify4/libsm6/libpcre2-32-0: wxPython (wxGTK) runtime libraries
# — the prebuilt wheel dynamically links these; without libpcre2-32-0 specifically, `import wx`
# fails with `ImportError: libpcre2-32.so.0: cannot open shared object file`.
# xdg-utils: a hard dependency of the google-chrome-stable .deb below; without it, `dpkg -i`
# fails to configure the package (not in nomad-north-desktop-base by default, same as
# pynxtools-mpes's Dockerfile).
RUN apt-get -y -qq update \
 && apt-get -y -qq install --no-install-recommends \
        git \
        libgtk-3-0 \
        libsdl2-2.0-0 \
        libnotify4 \
        libsm6 \
        libpcre2-32-0 \
        xdg-utils \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Chrome itself comes from nomad-north-desktop-base already (installed, sandboxed, and
# desktop-integrated there).

USER ${NB_UID}
WORKDIR "${HOME}"

ENV UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_SYSTEM_PYTHON=1

# wxPython ships no PyPI wheel for Linux. The wxPython project publishes prebuilt wheels keyed
# to the exact Ubuntu release + CPython version at extras.wxpython.org, as a flat find-links
# page (not a PEP 503 simple index, so `--find-links`, not `--extra-index-url`). The URL must
# match the base image (Ubuntu 24.04 "noble", CPython 3.13) or uv/pip won't find a matching
# wheel there and fall back to a from-source build, which needs a much larger wxGTK build
# toolchain than this image ships and fails outright without one.
ENV WXPYTHON_FIND_LINKS_URL=https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-24.04/

# -c http.version=HTTP/1.1 plus a retry loop: `git clone` to this URL fails intermittently
# inside Docker Desktop's WSL2 network layer with "could not read Username ... expected flush
# after ref listing" — a known HTTP/2 stream-handling symptom — while the identical clone
# succeeds instantly from the host. wget-based downloads elsewhere in this Dockerfile are
# unaffected (plain HTTP/1.1 by default).
RUN for i in 1 2 3; do \
      git -c http.version=HTTP/1.1 clone --depth 1 \
        https://github.com/KherveFitting/KherveFitting "${HOME}/KherveFitting" && break; \
      echo "git clone attempt $i failed, retrying..." >&2; \
      rm -rf "${HOME}/KherveFitting"; \
      sleep 5; \
    done

# KherveFitting's requirements.txt pins exact versions frozen from its own development
# environment (older CPython, and on Windows for some contributors) — several have no cp313
# Linux wheel. Reinstalling the same package set unpinned lets uv resolve versions that are
# actually compatible with this image, instead of chasing individual pins (the same tradeoff
# made for pynxtools-mpes's north-group dependencies).
# wxPython is the one exception left pinned: unpinned, uv resolves the newest release, which has
# no prebuilt wheel at ${WXPYTHON_FIND_LINKS_URL} and falls back to a from-source build that
# fails outright (no C compiler in this image, by design — see the desktop-base Dockerfile).
# 4.2.2 is the version that extras.wxpython.org actually publishes a wheel for on this image's
# Ubuntu release + CPython version; bump this only after confirming a matching wheel exists.
RUN grep -iv '^wxpython' "${HOME}/KherveFitting/requirements.txt" \
      | sed 's/==.*//' > /tmp/kherve-requirements.txt \
 && uv pip install --find-links ${WXPYTHON_FIND_LINKS_URL} \
      "pynxtools[xps]" \
      "wxPython==4.2.2" \
      -r /tmp/kherve-requirements.txt

# KherveFitting ships its own icon in its repo (Icons/Icon.png); it doesn't register it with
# the icon theme, so a launcher entry can't find it by name unless it's copied there first —
# same reasoning as pynxtools-mpes's silx icon copy.
RUN mkdir -p "${HOME}/.local/share/applications" "${HOME}/.local/share/icons/hicolor/256x256/apps" "${HOME}/Desktop" \
 && cp "${HOME}/KherveFitting/Icons/Icon.png" \
       "${HOME}/.local/share/icons/hicolor/256x256/apps/KherveFitting.png"
COPY --chown=${NB_UID}:${NB_GID} src/nomad_north_xps/north_tools/kherve/config/KherveFitting.desktop "${HOME}/.local/share/applications/KherveFitting.desktop"
COPY --chown=${NB_UID}:${NB_GID} src/nomad_north_xps/north_tools/kherve/config/KherveFitting.desktop "${HOME}/Desktop/KherveFitting.desktop"
RUN chmod 755 "${HOME}/.local/share/applications/KherveFitting.desktop" "${HOME}/Desktop/KherveFitting.desktop"

# Chrome's own Desktop icon and the untrusted-launcher trust-fix autostart both come from
# nomad-north-desktop-base already.

WORKDIR "${HOME}"

EXPOSE 8888
