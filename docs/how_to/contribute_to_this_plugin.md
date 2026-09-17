# Contribute to This Plugin

This guide walks through setting up a working environment for developing `nomad-north-xps`.

!!! info "Structure of this repository"
    The plugin's Python side (the single `NORTHTool`/`NORTHToolEntryPoint` definition, `xps`) lives in [`src/nomad_north_xps`](https://github.com/FAIRmat-NFDI/nomad-north-xps/tree/main/src/nomad_north_xps){:target="_blank" rel="noopener"}. Each GUI tool has its own build directory under `src/nomad_north_xps/north_tools/`: [`kherve`](https://github.com/FAIRmat-NFDI/nomad-north-xps/tree/main/src/nomad_north_xps/north_tools/kherve){:target="_blank" rel="noopener"} (CI-built) and [`casa`](https://github.com/FAIRmat-NFDI/nomad-north-xps/tree/main/src/nomad_north_xps/north_tools/casa){:target="_blank" rel="noopener"} (local build only), each with its own README. See [Explanation](../explanation/explanation.md) for why there's still only one entry point.

## Setup

It is recommended to use Python 3.12 with a dedicated virtual environment. We recommend [`uv`](https://github.com/astral-sh/uv){:target="_blank" rel="noopener"}, an extremely fast Python package and project manager; a more classical `venv`/`pip` approach works too.

=== "uv"
    `uv` is capable of creating a virtual environment and installing the required Python version at the same time.

    ```bash
    uv venv --python 3.12
    ```

=== "venv"
    Note that you will need to install the Python version manually beforehand.

    ```bash
    python3.12 -m venv .venv
    . .venv/bin/activate
    ```

## Development installation

Clone the repository:

```console
git clone https://github.com/FAIRmat-NFDI/nomad-north-xps.git
cd nomad-north-xps
```

Install the package in editable mode, together with its dev dependencies:

=== "uv"

    ```bash
    uv pip install -e ".[dev]"
    ```

=== "pip"

    ```bash
    pip install --upgrade pip
    pip install -e ".[dev]"
    ```

## Linting, formatting, and pre-commit hooks

We use [Ruff](https://docs.astral.sh/ruff/){:target="_blank" rel="noopener"} for linting/formatting. `.pre-commit-config.yaml` also runs pyupgrade, nbstripout, and cspell. We use [`prek`](https://github.com/j178/prek){:target="_blank" rel="noopener"} -- a drop-in, faster reimplementation of `pre-commit` that reads the same config file -- as the runner:

```console
prek install           # installs the git hook
prek run --all-files   # run all hooks against the whole repo once
```

You can also run Ruff directly:

```console
ruff check .
ruff format . --check
```

If `cspell` flags a real (correctly spelled) word, add it to `.cspell/custom-dictionary.txt`, or regenerate it from the current source/docs:

```console
scripts/generate_custom_dict.sh
```

## Working on the Docker images

`kherve` is public CI-built, so you can build and test it locally the same way CI does:

```console
docker build -f src/nomad_north_xps/north_tools/kherve/Dockerfile \
    -t nomad-north-xps-kherve:dev .
docker run -p 8888:8888 nomad-north-xps-kherve:dev
```

`casa` is never CI-built and needs your own copy of CasaXPS — see [How-to guides > Build the Image](build_the_image.md) and the `casa` build directory's own README.

## Testing

Unit tests are written with [pytest](https://docs.pytest.org/en/stable/){:target="_blank" rel="noopener"}:

```console
pytest -sv tests
```

These test the Python entry points only (registration, field values) -- they don't build any
Docker image.

## Contributing on GitHub

Fork the repository, commit your changes on a branch in your fork, and open a pull request against `FAIRmat-NFDI/nomad-north-xps`. CI checks linting, runs the tests, builds and pushes the `kherve` image (see `publish_north.yml`), and builds the docs. Once checks pass and a reviewer approves it, the PR can be merged.

Changing something in `docs/`? See [How-to guides > Contribute to the Documentation](contribute_to_the_documentation.md) for the writing conventions, how to build the docs locally, and how to add a new page.

### Template updates

This project was generated from, and stays in sync with, FAIRmat's [`cookiecutter-nomad-plugin`](https://github.com/FAIRmat-NFDI/cookiecutter-nomad-plugin){:target="_blank" rel="noopener"} template via [`cruft`](https://github.com/cruft/cruft){:target="_blank" rel="noopener"}. To check for and apply template updates, run `cruft update` in the repository root -- see the [`cruft` documentation](https://cruft.github.io/cruft/#updating-a-project){:target="_blank" rel="noopener"} for details. `.github/*` workflow files are excluded from these updates to avoid permissions issues -- `publish_north.yml` is hand-maintained (see [Reference > CI](../reference/references.md#ci)).

## Developing this plugin as part of NOMAD

If you're testing this plugin's NORTH integration against a full NOMAD instance -- not just its own unit tests -- use [`nomad-distro-dev`](https://github.com/FAIRmat-NFDI/nomad-distro-dev){:target="_blank" rel="noopener"}, FAIRmat's development environment for NOMAD and its plugins. See [How-to guides > Install this Plugin](install_this_plugin.md) for how this repo is wired into that workspace.

## Troubleshooting

If you hit an issue with the tool or with setting up the development environment, open a [GitHub issue](https://github.com/FAIRmat-NFDI/nomad-north-xps/issues/new){:target="_blank" rel="noopener"}.
