---
description: "Write unit tests for a spaceship simulator module or class using pytest"
argument-hint: "Module or class to test, e.g. 'ShipState in ship/ship.py' or 'Galaxy in world/universe.py'"
agent: "agent"
tools: ["search", "read_file"]
---

Write pytest unit tests for the specified module or class in the spaceship simulator project.

## Test File Location

Place test files under `tests/` mirroring the source layout:

| Source | Test file |
|--------|-----------|
| `spaceship_simulator/ship/ship.py` | `tests/ship/test_ship.py` |
| `spaceship_simulator/world/universe.py` | `tests/world/test_universe.py` |
| `spaceship_simulator/config/constants.py` | `tests/config/test_constants.py` |
| `spaceship_simulator/utils/math_utils.py` | `tests/utils/test_math_utils.py` |

Create `tests/__init__.py` and any sub-package `__init__.py` files if they don't already exist.

## Testing Conventions

- Use **pytest** (already available via Poetry; `poetry run pytest`).
- Keep tests free of Panda3D rendering/windowing — instantiate data-only classes directly. Mock `ShowBase` or `app` dependencies with `unittest.mock.MagicMock`.
- Group related tests in a class prefixed with `Test` (e.g., `TestShipState`).
- Use descriptive names: `test_<thing>_<condition>_<expected_outcome>`.
- Cover: happy paths, boundary values, and at least one error/edge case per public method.
- Use `pytest.approx` for floating-point comparisons.
- Do not import from Panda3D in test files unless you mock the windowing system first.

## Task

$ARGUMENTS

Read the target source file, then write comprehensive tests. Create the test file(s) at the correct path(s).
