from __future__ import annotations

import os

import nox


@nox.session(
    python=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14", "pypy"]
)
def test(session: nox.Session) -> None:
    # Install deps and the package itself.
    session.install("-U", "pip", "setuptools", silent=False)
    session.install("-r", "dev-requirements.txt", silent=False)

    session.install(".", silent=False)

    # Show the pip version.
    session.run("pip", "--version")
    # Print the Python version and bytesize.
    session.run("python", "--version")

    # Inspired from https://hynek.me/articles/ditch-codecov-python/
    # We use parallel mode and then combine in a later CI step
    session.run(
        "python",
        "-m",
        "coverage",
        "run",
        "--parallel-mode",
        "-m",
        "pytest",
        "-v",
        "-ra",
        f"--color={'yes' if 'GITHUB_ACTIONS' in os.environ else 'auto'}",
        "--tb=native",
        "--durations=10",
        "--strict-config",
        "--strict-markers",
        *session.posargs,
        env={
            "PYTHONWARNINGS": "always::DeprecationWarning",
            "COVERAGE_CORE": "sysmon",
            "PY_IGNORE_IMPORTMISMATCH": "1",
        },
    )


@nox.session()
def format(session: nox.Session) -> None:
    """Run code formatters."""
    lint(session)


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
