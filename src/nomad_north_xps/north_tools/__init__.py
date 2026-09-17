# SPDX-FileCopyrightText: The nomad-north-xps Authors
#
# This file is part of nomad-north-xps.
#
# SPDX-License-Identifier: Apache-2.0

from nomad.config.models.north import NORTHTool
from nomad.config.models.plugins import NORTHToolEntryPoint

# One entry point, `xps`, regardless of which build directory produced its image.
# `kherve` (open-source, no license question) is CI-published and what `image` points
# at by default.
# `casa` (CasaXPS via Wine) is never CI-built — even its free demo has no confirmed
# redistribution rights — so it stays a local-only build layered `FROM` the kherve image;
# see north_tools/casa/README.md. Someone who builds it repoints this same entry point's
# `image` via  `nomad.yaml` instead of a second entry point ever appearing in NORTH's launcher.

xps_north_tool = NORTHTool(
    short_description='XPS peak-fitting GUI tools on top of pynxtools[xps].',
    # Reconfigure via `nomad.yaml` to point at a local build that also has CasaXPS —
    # see this package's `install_this_plugin.md`.
    image='ghcr.io/fairmat-nfdi/nomad-north-xps/kherve:main',
    description="""### **XPS peak fitting on the xps NORTH tool**

    KherveFitting (the successor to LG4X) for interactive XPS peak fitting, on top of the
    `pynxtools-xps` conversion tooling. The image can be swapped for a locally-built one that
    also includes CasaXPS via Wine.""",
    external_mounts=[],
    file_extensions=['nxs', 'vms', 'npl', 'h5', 'hdf5', 'txt', 'spe', 'pro', 'ibw'],
    image_pull_policy='Always',
    default_url='/desktop',
    maintainer=[
        {'name': 'Lukas Pielsticker', 'email': 'lukas.pielsticker@physik.hu-berlin.de'}
    ],
    mount_path='/home/jovyan',
    path_prefix='lab/tree',
    privileged=False,
    with_path=True,
    display_name='xps',
)

xps = NORTHToolEntryPoint(
    id_url_safe='xps',
    north_tool=xps_north_tool,
)
