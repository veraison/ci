#!/usr/bin/env python3
# Copyright 2026 Contributors to the Veraison project.
# SPDX-License-Identifier: Apache-2.0
#
# Fails if a Go package with test files did not run in the output of a test
# command, e.g. because it is missing from a hand-written package list or lives
# in a nested module that `go test ./...` does not descend into.
#
# Test files are found without build tags, so tests that should not run by
# default belong behind a build tag (e.g. //go:build integration).
#
# Usage: check-tests-ran.py OUTPUT
#
#   OUTPUT  file with the combined output of the test command
import os
import re
import subprocess
import sys

# "ok  \tpkg\t0.1s", "FAIL\tpkg [build failed]", "ok  \tpkg\t(cached)"
RAN_RE = re.compile(r"^(?:ok|FAIL)\s+(?P<package>\S+)")

SKIP_DIRS = {"vendor", "testdata"}


def modules(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith((".", "_"))]
        if "go.mod" in filenames:
            yield dirpath


def packages_with_tests(module):
    out = subprocess.run(
        ["go", "list", "-e", "-f", "{{if or .TestGoFiles .XTestGoFiles}}{{.ImportPath}}{{end}}", "./..."],
        cwd=module,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout
    return {line for line in out.splitlines() if line}


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2

    # test output may contain binary data, e.g. dumped CBOR
    with open(sys.argv[1], errors="replace") as f:
        ran = {m.group("package") for m in map(RAN_RE.match, f) if m}

    expected = set()
    for module in modules("."):
        expected |= packages_with_tests(module)

    missing = sorted(expected - ran)
    for package in missing:
        print(f"::error::{package} has test files but its tests did not run")
    if missing:
        print(
            "Run all packages in the test command, e.g. `go test ./...` in every module instead of "
            "a fixed package list. Tests that should not run by default belong behind a build tag."
        )
        return 1
    print(f"all {len(expected)} packages with test files ran")
    return 0


if __name__ == "__main__":
    sys.exit(main())
