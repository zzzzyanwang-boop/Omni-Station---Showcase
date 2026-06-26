# Rust Native Boundary Proofs

This capsule demonstrates public-safe Rust boundary patterns for native infrastructure surfaces.

What it shows:

- deterministic wire-frame encoding with checksum validation;
- feature-stream IR validation with duplicate and unresolved-input rejection;
- append-only event journal sequencing and replay boundaries.

Run:

```powershell
cargo test --manifest-path code_capsules/rust_native_boundary_proofs/Cargo.toml
```
