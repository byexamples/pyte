"""
    benchmark
    ~~~~~~~~~

    A simple script for running benchmarks on captured process output.

    Example run::

        $ BENCHMARK=tests/captured/ls.input python benchmark.py
        .....................
        ls.input: Mean +- std dev: 644 ns +- 23 ns

    Environment variables:

    BENCHMARK: the input file to feed pyte's Stream and render on the Screen
    GEOMETRY: the dimensions of the screen with format "<lines>x<cols>" (default 24x80)

    :copyright: (c) 2016-2021 by pyte authors and contributors,
                    see AUTHORS for details.
    :license: LGPL, see LICENSE for more details.
"""

import io
import os.path
import sys
from functools import partial

try:
    from pyperf import Runner
except ImportError:
    sys.exit("``perf`` not found. Try installing it via ``pip install perf``.")

import pyte


def make_benchmark(path, screen_cls, columns, lines):
    with io.open(path, "rt", encoding="utf-8") as handle:
        data = handle.read()

    stream = pyte.Stream(screen_cls(columns, lines))
    return partial(stream.feed, data)


if __name__ == "__main__":
    benchmark = os.environ["BENCHMARK"]
    lines, columns = map(int, os.environ.get("GEOMETRY", "24x80").split('x'))
    sys.argv.extend(["--inherit-environ", "BENCHMARK,GEOMETRY"])

    runner = Runner(metadata={
        'input_file': benchmark,
        'columns': columns,
        'lines': lines
        })

    for screen_cls in [pyte.Screen, pyte.DiffScreen, pyte.HistoryScreen]:
        name = os.path.basename(benchmark) + "->" + screen_cls.__name__
        runner.bench_func(name, make_benchmark(benchmark, screen_cls, columns, lines))
