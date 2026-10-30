"""Preserve stdout routing at the dataframe-independent runtime boundary."""

import io

from nwau_py import runtime


def test_dash_output_uses_existing_stdout_without_opening_a_file(monkeypatch):
    stdout = io.StringIO()
    monkeypatch.setattr(runtime.sys, "stdout", stdout)
    stream = runtime.open_output_stream("-")
    assert stream is stdout
    stream.write("synthetic,result\n")
    assert stdout.getvalue() == "synthetic,result\n"
    assert not stdout.closed
