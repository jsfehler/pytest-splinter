"""pytest-splinter Browser proxy class tests.

Tests related to the modifications made on top of splinter's Browser class.
"""
import time

import pytest


def test_wait_for_condition(browser, splinter_browser_load_condition, splinter_browser_load_timeout):
    """Test that by default wait_until is successful."""
    browser.wait_for_condition(
        splinter_browser_load_condition,
        splinter_browser_load_timeout,
    )
    assert True


def test_wait_for_condition_timeout(mocked_browser, monkeypatch):
    """Check timeouts."""
    ticks = iter([1, 2, 15])

    def fake_time():
        return next(ticks)

    monkeypatch.setattr(time, 'time', fake_time)

    with pytest.raises(Exception) as e:
        mocked_browser.wait_for_condition(lambda browser: False, 10)


def test_wait_for_condititon(mocked_browser, monkeypatch):
    """Check conditioning."""
    checks = iter([False, True])

    def condition(browser):
        return next(checks)

    ticks = iter([1, 2, 3])

    def fake_time():
        return next(ticks)

    sleeps = []

    def fake_sleep(i):
        sleeps.append(i)

    monkeypatch.setattr(time, 'time', fake_time)
    monkeypatch.setattr(time, 'sleep', fake_sleep)

    assert mocked_browser.wait_for_condition(condition, 10)

    assert sleeps == [0.5]
