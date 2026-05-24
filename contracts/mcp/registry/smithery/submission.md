# Smithery Submission

Date prepared: 2026-05-24

## HTTP publication path

The repository now exposes a Streamable HTTP-compatible entry point:

```bash
mchs-mcp-http
```

Routes:

- `POST /mcp`
- `GET /healthz`
- `GET /.well-known/mcp/server-card.json`

Publish after deploying the service to public HTTPS:

```bash
smithery mcp publish "https://<host>/mcp" -n <namespace>/mchs
```

## Local bundle path

Smithery also accepts MCPB bundles for local stdio servers. The candidate bundle
manifest is staged under `contracts/mcp/registry/smithery/mcpb/`.

Publish after producing `server.mcpb` and authenticating the Smithery CLI:

```bash
smithery auth login
smithery mcp publish ./server.mcpb -n <namespace>/mchs
```

## Current status

Prepared locally. A live Smithery listing is not claimed until a public HTTPS
deployment or MCPB bundle is submitted through an authenticated Smithery account.
