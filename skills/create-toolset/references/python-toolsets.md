# Python ToolsetRegistry toolsets

## Structure

- Decorate the class with `@unreal.uclass()` and inherit from `unreal.ToolsetDefinition`.
- Keep one toolset class per file.
- Put `@toolset_registry.tool_call` immediately above `@staticmethod`.
- Type-annotate every parameter and return value with standard Python annotations.
- Keep private helpers static, underscore-prefixed, and at the end of the class.

```python
@unreal.uclass()
class MyToolset(unreal.ToolsetDefinition):
    """Manages MyThings in the current level."""

    @toolset_registry.tool_call
    @staticmethod
    def find_things(name_pattern: str) -> list[MyThing]:
        """Returns matching things.

        Args:
            name_pattern: Substring matched against thing names.

        Returns:
            Matching things, or an empty list when none match.
        """
        if not name_pattern:
            raise ValueError("name_pattern must not be empty.")
        ...
```

## Registration

Registration is not automatic. Add the class to the plugin's existing registration flow and call:

```python
unreal.ToolsetRegistry.register_toolset_class(MyToolset)
```

Unregister it during plugin shutdown. Follow the neighboring package's `__init__.py` or `init_unreal.py` pattern.

## Reloading

The Editor does not automatically pick up changed Python toolsets. Enable Python Remote Execution and reload the plugin package with the ToolsetRegistry reload helper before rediscovering tests:

```text
python Engine/Plugins/Experimental/ToolsetRegistry/Content/Python/toolset_registry/tests/reload_remote.py <plugin>
```
