"""Test fixtures for pytest."""

import kubernetes
import pytest


def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        "--run-kube-tests", action="store_true", default=False,
        help="run tests that require a Kubernetes or OpenShift cluster"
    )
    parser.addoption(
        "--run-benchmarks", action="store_true", default=False,
        help="run benchmark tests (also needs kubernetes)"
    )

def pytest_configure(config):
    """Define kube_required pytest mark."""
    config.addinivalue_line("markers", "kube_required: mark test as requiring kubernetes")
    # Allow non-kube tests to run.
    if not config.getoption("--run-kube-tests"):
        kubernetes.config.load_kube_config = object

def pytest_collection_modifyitems(config, items):
    """Only run kube_required tests when --run-kube-tests is used."""
    if not config.getoption("--run-kube-tests"):
        skip_kube = pytest.mark.skip(reason="need --run-kube-tests option to run")
        for item in items:
            if "kube_required" in item.keywords:
                item.add_marker(skip_kube)
    if not config.getoption("--run-benchmarks"):
        skip_bench = pytest.mark.skip(reason="need --run-benchmarks option to run")
        for item in items:
            if "benchmark" in item.keywords:
                item.add_marker(skip_bench)
