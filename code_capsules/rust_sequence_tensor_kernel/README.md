# Rust Sequence Tensor Kernel

This capsule is a standalone Rust toy kernel. It is not a PyO3 extension and does not contain production OmniStation code. It demonstrates the native-kernel part of the design in a compact, reviewable form.

What it shows:

- validity bitmap packing;
- contiguous anchor-run discovery for sequence batching;
- deterministic sequence tensor gathering from row-major numeric data;
- explicit errors for invalid feature counts, ragged inputs, and out-of-bounds anchors.

Run:

```powershell
cargo test --manifest-path code_capsules/rust_sequence_tensor_kernel/Cargo.toml
```
