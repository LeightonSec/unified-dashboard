"""Pytest bootstrap.

app.py reads SECRET_KEY at import time and raises RuntimeError if it is unset
(fail-closed, by design). The test suite imports app, so a dummy SECRET_KEY
must exist in the environment before that import — otherwise collection fails
in a clean checkout (e.g. CI, where there is no .env). conftest.py is imported
by pytest before any test module, so this runs first. The value is a throwaway
used only to satisfy the import; it is never a real secret.
"""
import os

os.environ.setdefault('SECRET_KEY', 'test-secret-not-for-production')
