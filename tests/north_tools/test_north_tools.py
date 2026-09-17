# SPDX-FileCopyrightText: The nomad-north-xps Authors
#
# This file is part of nomad-north-xps.
#
# SPDX-License-Identifier: Apache-2.0

from importlib.metadata import entry_points


def test_north_tool_entry_point_registered():
    # exercises the actual mechanism NOMAD uses to discover the tool at runtime
    # (pyproject.toml's [project.entry-points.'nomad.plugin']), not just a direct import
    from nomad_north_xps.north_tools import xps

    (entry_point,) = entry_points(group='nomad.plugin', name='xps_north_tool')
    assert entry_point.load() is xps


def test_north_tool_id_url_safe():
    # this will raise an exception if pydantic model validation fails
    from nomad_north_xps.north_tools import xps

    assert xps.id_url_safe == 'xps', 'NORTHTool entry point has incorrect id_url_safe'


def test_north_tool_metadata():
    from nomad_north_xps.north_tools import xps_north_tool

    assert xps_north_tool.display_name == 'xps'
    assert xps_north_tool.default_url == '/desktop'
    assert xps_north_tool.image == 'ghcr.io/fairmat-nfdi/nomad-north-xps/kherve:main'
    assert xps_north_tool.maintainer, 'NORTHTool must list at least one maintainer'
