# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os
import plistlib
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from ruamel.yaml import YAML

from jrnl import __version__
from jrnl.journals import DayOne


@pytest.mark.parametrize(
    "zone, utc, local, fold",
    [
        ("America/Los_Angeles", "2022-03-13 07:59", "2022-03-12 23:59", 0),
        ("America/Los_Angeles", "2022-03-13 09:59", "2022-03-13 01:59", 0),
        ("America/Los_Angeles", "2022-03-13 10:00", "2022-03-13 03:00", 0),
        ("America/Los_Angeles", "2022-11-06 06:59", "2022-11-05 23:59", 0),
        ("America/Los_Angeles", "2022-11-06 08:30", "2022-11-06 01:30", 0),
        ("America/Los_Angeles", "2022-11-06 09:30", "2022-11-06 01:30", 1),
        ("America/Los_Angeles", "2022-11-06 10:00", "2022-11-06 02:00", 0),
        ("Europe/Berlin", "2022-03-27 00:30", "2022-03-27 01:30", 0),
        ("Europe/Berlin", "2022-03-27 01:30", "2022-03-27 03:30", 0),
        ("Europe/Berlin", "2022-10-30 00:30", "2022-10-30 02:30", 0),
        ("Europe/Berlin", "2022-10-30 01:30", "2022-10-30 02:30", 1),
        ("UTC", "2022-03-13 07:59", "2022-03-13 07:59", 0),
        ("Asia/Kolkata", "2022-03-13 07:59", "2022-03-13 13:29", 0),
    ],
)
def test_open_converts_utc_creation_date(tmp_path, zone, utc, local, fold):
    entry = {
        "Creation Date": datetime.fromisoformat(utc),
        "Time Zone": zone,
        "Entry Text": "DayOne timezone regression",
        "Starred": False,
        "UUID": "DSTREGRESSION",
    }
    (tmp_path / "entry.doentry").write_bytes(plistlib.dumps(entry))

    journal = DayOne(journal=str(tmp_path)).open()

    assert len(journal.entries) == 1
    date = journal.entries[0].date
    assert date == datetime.fromisoformat(local)
    assert date.tzinfo is None
    assert date.fold == fold


def test_open_without_timezone_uses_local_zone(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "tzlocal.get_localzone", lambda: ZoneInfo("America/Los_Angeles")
    )
    entry = {
        "Creation Date": datetime(2022, 3, 13, 7, 59),
        "Entry Text": "Missing timezone regression",
        "Starred": False,
        "UUID": "MISSINGTIMEZONE",
    }
    (tmp_path / "entry.doentry").write_bytes(plistlib.dumps(entry))

    journal = DayOne(journal=str(tmp_path)).open()

    assert journal.entries[0].date == datetime(2022, 3, 12, 23, 59)


@pytest.mark.skipif(sys.platform == "win32", reason="TZ controls POSIX subprocess time")
@pytest.mark.parametrize(
    "local, utc",
    [
        ("2022-03-12", datetime(2022, 3, 13, 7, 59)),
        ("2022-11-05", datetime(2022, 11, 6, 6, 59)),
    ],
)
def test_cli_dayone_round_trip_before_dst(tmp_path, local, utc):
    journal = tmp_path / "journal.dayone"
    entries = journal / "entries"
    entries.mkdir(parents=True)
    config = {
        "version": __version__,
        "journals": {"default": {"journal": str(journal)}},
        "editor": "",
        "encrypt": False,
        "template": False,
        "default_hour": 9,
        "default_minute": 0,
        "timeformat": "%Y-%m-%d %H:%M",
        "tagsymbols": "@",
        "highlight": False,
        "linewrap": 79,
        "indent_character": "|",
        "colors": {key: "none" for key in ("body", "date", "tags", "title")},
    }
    # Use a complete alternate config and isolate any default paths as well.
    config_path = tmp_path / "config.yaml"
    with config_path.open("w", encoding="utf-8") as stream:
        YAML().dump(config, stream)
    env = {
        **os.environ,
        "TZ": "America/Los_Angeles",
        "HOME": str(tmp_path),
        "XDG_CONFIG_HOME": str(tmp_path / "config"),
        "XDG_DATA_HOME": str(tmp_path / "data"),
    }
    command = [sys.executable, "-m", "jrnl", "--config-file", str(config_path)]
    write = subprocess.run(
        command + [f"{local} at 11:59pm: DayOne round trip"],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert write.returncode == 0, write.stderr
    stored_files = list(entries.glob("*.doentry"))
    assert len(stored_files) == 1
    stored = plistlib.loads(stored_files[0].read_bytes())
    assert stored["Creation Date"] == utc
    assert stored["Time Zone"] == "America/Los_Angeles"

    read = subprocess.run(
        command + ["--short"], capture_output=True, text=True, env=env, timeout=30
    )
    assert read.returncode == 0, read.stderr
    assert read.stdout.strip() == f"{local} 23:59 DayOne round trip"
