# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import pytest

from jrnl.upgrade import is_old_version


def _write_config(tmp_path, contents: str) -> str:
    config_path = tmp_path / "jrnl.yaml"
    config_path.write_text(contents, encoding="utf-8")
    return str(config_path)


def test_modern_json_style_config_is_not_old(tmp_path):
    """Regression for #1908: a modern config must not be treated as 1.x just
    because it happens to be written as JSON-compatible YAML."""
    config_path = _write_config(
        tmp_path,
        '{"version": "v4.1", "journals": {"default": "journal.txt"}}',
    )

    assert is_old_version(config_path) is False


def test_current_version_json_style_config_is_not_old(tmp_path):
    config_path = _write_config(
        tmp_path,
        '{"version": "4.6", "journals": {"default": "journal.txt"}}',
    )

    assert is_old_version(config_path) is False


def test_numeric_version_from_yaml_is_not_old(tmp_path):
    config_path = _write_config(
        tmp_path,
        '{"version": 4.6, "journals": {"default": "journal.txt"}}',
    )

    assert is_old_version(config_path) is False


def test_genuinely_old_json_style_version_is_old(tmp_path):
    config_path = _write_config(
        tmp_path,
        '{"version": "1.9.5", "journals": {"default": "journal.txt"}}',
    )

    assert is_old_version(config_path) is True


def test_genuinely_old_prefixed_version_is_old(tmp_path):
    config_path = _write_config(
        tmp_path,
        '{"version": "v1.9.5", "journals": {"default": "journal.txt"}}',
    )

    assert is_old_version(config_path) is True


def test_two_point_zero_is_not_old(tmp_path):
    config_path = _write_config(
        tmp_path,
        '{"version": "2.0", "journals": {"default": "journal.txt"}}',
    )

    assert is_old_version(config_path) is False


@pytest.mark.parametrize("version", ["1.9", "v1.9", "0.9.9", "1.99.99"])
def test_versions_below_two_are_old(tmp_path, version):
    config_path = _write_config(
        tmp_path,
        f'{{"version": "{version}", "journals": {{"default": "journal.txt"}}}}',
    )

    assert is_old_version(config_path) is True


@pytest.mark.parametrize("version", ["2.0.0", "2.1", "v3.0", "4.6", "10.0"])
def test_versions_at_or_above_two_are_not_old(tmp_path, version):
    config_path = _write_config(
        tmp_path,
        f'{{"version": "{version}", "journals": {{"default": "journal.txt"}}}}',
    )

    assert is_old_version(config_path) is False


def test_json_style_config_without_version_keeps_json_fallback(tmp_path):
    """Still detect real 1.x configs, which predate the version field."""
    config_path = _write_config(
        tmp_path,
        '{"journals": {"default": "journal.txt"}}',
    )

    assert is_old_version(config_path) is True


def test_yaml_config_without_version_is_not_old(tmp_path):
    config_path = _write_config(
        tmp_path,
        "journals:\n  default: journal.txt\n",
    )

    assert is_old_version(config_path) is False


def test_non_json_config_with_modern_version_is_not_old(tmp_path):
    config_path = _write_config(
        tmp_path,
        "version: 4.6\njournals:\n  default: journal.txt\n",
    )

    assert is_old_version(config_path) is False


def test_non_json_config_with_old_version_is_old(tmp_path):
    config_path = _write_config(
        tmp_path,
        "version: 1.9.5\njournals:\n  default: journal.txt\n",
    )

    assert is_old_version(config_path) is True


def test_unparseable_version_does_not_fall_back_to_json_check(tmp_path):
    """A present version field stays authoritative even when it cannot be
    parsed. Source builds write ``version: source``; a JSON-style config with
    that value must not be mistaken for a 1.x config."""
    config_path = _write_config(
        tmp_path,
        '{"version": "source", "journals": {"default": "journal.txt"}}',
    )

    assert is_old_version(config_path) is False


@pytest.mark.parametrize("version_value", ['"source"', '""', "null", "'dev'"])
def test_present_but_unparseable_version_is_not_old(tmp_path, version_value):
    config_path = _write_config(
        tmp_path,
        f'{{"version": {version_value}, "journals": {{"default": "j.txt"}}}}',
    )

    assert is_old_version(config_path) is False


def test_unparseable_version_in_yaml_style_config_is_not_old(tmp_path):
    config_path = _write_config(
        tmp_path,
        "version: source\njournals:\n  default: journal.txt\n",
    )

    assert is_old_version(config_path) is False


def test_is_old_version_reuses_already_loaded_config(tmp_path, monkeypatch):
    """The caller can pass the config it already loaded, so a duplicate-key
    config does not print its warning twice."""
    config_path = _write_config(
        tmp_path,
        '{"version": "4.6", "journals": {"default": "journal.txt"}}',
    )
    config = {"version": "4.6", "journals": {"default": "journal.txt"}}

    def fail_load_config(_path):
        message = "is_old_version unexpectedly reloaded the config"
        raise AssertionError(message)

    monkeypatch.setattr("jrnl.upgrade.load_config", fail_load_config)

    assert is_old_version(config_path, config) is False


def test_load_or_install_passes_loaded_config_to_version_check(tmp_path, monkeypatch):
    """load_or_install_jrnl already loaded the config; is_old_version must not
    load it a second time (which would duplicate duplicate-key warnings)."""
    from jrnl import install

    config_path = _write_config(
        tmp_path,
        '{"version": "4.6", "journals": {"default": "journal.txt"}}',
    )

    def fail_load_config(_path):
        message = "config was loaded again inside is_old_version"
        raise AssertionError(message)

    monkeypatch.setattr("jrnl.upgrade.load_config", fail_load_config)

    config = install.load_or_install_jrnl(config_path)

    assert config["version"] is not None
