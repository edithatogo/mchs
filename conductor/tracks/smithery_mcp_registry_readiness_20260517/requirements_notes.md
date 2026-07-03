# Smithery MCP Registry Requirements Notes

Date checked: 2026-05-24

Sources:

- Smithery publish documentation: https://smithery.ai/docs/build/limits
- Smithery overview: https://smithery.ai/docs/build
- Smithery CLI documentation: https://smithery.ai/docs/concepts/cli
- Smithery namespaces documentation: https://smithery.ai/docs/concepts/namespaces

## Confirmed requirements

- Smithery URL publishing accepts servers that expose Streamable HTTP.
- If a server requires authentication, OAuth support is expected; Smithery handles client registration for the publishing flow.
- Smithery scans public servers to extract tools, prompts, and resources for the server page.
- If automatic scanning cannot complete because of auth, configuration, or scanner access issues, the server can provide manual metadata at `/.well-known/mcp/server-card.json`.
- Smithery documents CLI publishing with `smithery mcp publish "<url>" -n <namespace>/<server>` and optional `--config-schema`.
- Namespaces group published servers and appear in the public qualified name.
- Scanner compatibility should avoid returning `403` for unauthenticated OAuth flows; auth-required servers should use `401` so OAuth discovery can proceed. WAF/CDN rules must allow Smithery scanner traffic or the static server card must be used.

## MCHS submission decision

- Do not publish the current stdio-only server directly to Smithery as a production listing.
- Add a Streamable HTTP adapter owned by this repository unless an external host is deliberately selected later.
- Preferred route shape:
  - MCP endpoint: `/mcp`
  - Health endpoint: `/healthz`
  - Static metadata fallback: `/.well-known/mcp/server-card.json`
- Keep the initial Smithery listing unauthenticated if possible because MCHS registry demos use only synthetic/public-data-safe tools. If authentication is later added, return `401` for unauthenticated MCP requests and document scanner behavior.
- Candidate namespace/name remains to be confirmed by the project owner before final submission.

## Remaining gate

This track remains deferred at `http_publication_evidence` until a public Streamable HTTP endpoint or delegated host exists, scanner/server-card evidence is captured, HTTP contract tests pass, and Smithery listing/submission/gate evidence exists.
