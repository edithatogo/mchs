# Mchs.Bindings.DotNet

Thin .NET binding for MCHS NWAU contract validation and CLI interoperability. Formula logic remains in the canonical runtime; this package is not a clinical decision system.

The executable reads a `BindingRequest` JSON document, validates the requested operation, delegates execution to the shared `funding-calculator` CLI, and writes a `BindingResponse` transport status document.

Supported delegated operations:

- `acute`
- `ed`
- `non-admitted`
- `interop contract`

By default the adapter runs `funding-calculator`. For source-tree validation, set `MCHS_DOTNET_SHARED_CORE_CLI` to a command such as `uv run funding-calculator` so the .NET adapter uses the checked-out shared core instead of a globally installed package.

Example:

```bash
MCHS_DOTNET_SHARED_CORE_CLI="uv run funding-calculator" \
  dotnet run --project bindings/dotnet/DotNetBinding.csproj -- \
  --request request.json \
  --response response.json
```
