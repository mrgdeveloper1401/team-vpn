import logging

import pytest
from django.test import TestCase, Client, override_settings


@pytest.fixture(autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)


@pytest.fixture
def maintain_mode_on(settings):
    settings.MAINTENANCE_MODE = True


@pytest.fixture
def maintain_mode_off(settings):
    settings.MAINTENANCE_MODE = False


def test_response_when_maintenance_mode_is_on(maintain_mode_on, client):
    response = client.get("/")
    response_text = "application maintenance mode, please try again"
    assert response.content.decode() == response_text


@override_settings(MAINTENANCE_MODE=False)
def test_response_when_maintenance_mode_is_off(self):
    response = self.client.get("/")
    self.assertContains(response, "Maintenance mode is off")
    self.assertTemplateUsed(response, "maintenance_mode.html")
