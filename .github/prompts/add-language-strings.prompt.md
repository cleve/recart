---
description: "Add new UI strings in both English and Spanish to the spaceship simulator constants"
argument-hint: "Describe the strings to add, e.g. 'labels for a new weapons panel: fire, reload, ammo'"
agent: "agent"
tools: ["read_file", "replace_string_in_file"]
---

Add new localization strings to the spaceship simulator's bilingual string system in [spaceship_simulator/config/constants.py](../../spaceship_simulator/config/constants.py).

## String System Overview

All UI strings live in the `STRINGS` dict, keyed by language code (`"en"` / `"es"`), then by string key.
Retrieve strings at runtime with:

```python
from spaceship_simulator.config.constants import get_string
label = get_string("my_key", language)  # language = "en" or "es"
```

## Rules

1. **Always add to both `"en"` and `"es"`** in the same PR/change. Never leave a key in one language only.
2. Keep keys lowercase with underscores: `"fire_weapon"`, `"reload_ammo"`.
3. Group related keys together under a `# <section>` comment matching the existing comment style.
4. Spanish translations must be natural, not literal machine translations — use gaming/space vocabulary appropriate to the context.
5. After adding strings, show an example `get_string(...)` call demonstrating usage.

## Task

$ARGUMENTS

Read [spaceship_simulator/config/constants.py](../../spaceship_simulator/config/constants.py) first to find the right insertion point and follow the existing grouping. Then add the strings.
