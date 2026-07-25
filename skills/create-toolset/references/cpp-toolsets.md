# C++ ToolsetRegistry toolsets

## Structure

- Derive one toolset class per file pair from `UToolsetDefinition`.
- Mark exposed static functions with `UFUNCTION(meta = (AICallable))`.
- Leave private helpers without `AICallable`.
- Use reflected Unreal types for parameters, returns, and schema structs.
- Register and unregister the toolset class with `UToolsetRegistry` during module startup and shutdown, following the surrounding plugin pattern.

```cpp
USTRUCT(BlueprintType)
struct FMyThingInfo
{
    GENERATED_BODY()

    /** Domain meaning that the field name does not fully express. */
    UPROPERTY(meta = (ClampMin = "0.0", ClampMax = "1.0"))
    float Thinginess = 0.0f;
};

UCLASS(BlueprintType, MinimalAPI)
class UMyToolset : public UToolsetDefinition
{
    GENERATED_BODY()

public:
    /** Returns matching things, or an empty array when none match. */
    UFUNCTION(meta = (AICallable), Category = "MyToolset")
    static TArray<UMyThing*> FindThings(const FString& NamePattern);
};
```

## Errors

Raise a script error and return a null or default value immediately:

```cpp
if (NamePattern.IsEmpty())
{
    UKismetSystemLibrary::RaiseScriptError(
        EScriptExceptionType::Error,
        TEXT("NamePattern must not be empty."));
    return {};
}
```

## Async operations

Use a `UToolCallAsyncResult` subclass only for genuinely long-running operations. Call `SetValue()` on completion and `SetError()` on failure. Reuse an existing result type before creating a new one.

## Serialization

Rely on ToolsetRegistry's normal Unreal-to-JSON conversion. Create a custom `FToolsetJsonConverter` only when a specific type needs a materially cleaner agent-facing schema. Inspect existing converters before implementing one.
