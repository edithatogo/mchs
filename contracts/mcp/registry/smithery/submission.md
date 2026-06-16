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

Published as a Smithery stdio bundle on 2026-05-24.

- Qualified name: `edithatogo/mchs`
- Deployment ID: `200f2fd3-86c4-4122-b3bf-98abe5aa62f1`
- Status URL: https://smithery.ai/servers/edithatogo/mchs/releases
- Registry API: https://registry.smithery.ai/servers/edithatogo/mchs
- Runtime: `python`
- Bundle: `contracts/mcp/registry/smithery/mchs-0.2.2.mcpb`
- Bundle SHA-256: `de353472d4a88848a9cb69fe1376f3d22deca97c72ca264d49eba1f09c056456`

The first accepted Smithery release publishes the local stdio bundle. A public
Streamable HTTP Smithery endpoint is still not claimed until a hosted HTTPS MCP
server is deployed and submitted.
