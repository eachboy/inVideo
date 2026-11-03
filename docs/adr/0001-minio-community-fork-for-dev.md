# 0001. Use the pgsty/minio community build for object storage in dev

- **Status:** Accepted
- **Date:** 2026-10-30

## Context

inVideo stores originals, HLS segments and images in an S3-compatible
object store. The official `minio/minio` image is no longer maintained:
the community edition lost features, stopped publishing official images and
binaries, and its repository was archived (see `docs/project/stek.md`).
Running it means no security fixes. The application talks to storage only
through the S3 API (boto3), so the engine must be replaceable.

## Options considered

1. **Official `minio/minio`** — familiar and fully featured, but
   unmaintained; no security patches.
2. **`pgsty/minio`** — community-maintained build with an open-source
   codebase and a full web console. Smaller project, so the bus factor is
   a risk.
3. **Garage** — actively developed, lightweight, S3 API. No comparable
   web console; different bucket and key management.

## Decision

Use `pgsty/minio` pinned to the tag `RELEASE.2026-10-26T00-00-00Z`
(never `latest`). Reasons: it is actively maintained, its source is open,
and it behaves like MinIO, so the existing design and tooling stay valid.

## Consequences

- Easier: the same console and S3 behaviour as documented in the project.
- Harder: we depend on a small community project; the pinned tag must be
  updated deliberately and each bump checked.
- Constraint: application code uses only the S3 API, with nothing
  MinIO-specific, so we can move to Garage or cloud S3 by changing
  environment variables.
- Revisit if the fork is abandoned or a security issue is not fixed.
