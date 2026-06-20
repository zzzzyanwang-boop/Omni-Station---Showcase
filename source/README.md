# Source-Shaped Module Tree

This directory gives reviewers a navigable module map for the OmniStation Research OS architecture.

Each file keeps a retained module path and filename where that name communicates architecture ownership or general engineering responsibility. The implementation body is replaced by a short architecture note. These files are not runtime modules; they are review artifacts for inspecting ownership boundaries, module responsibilities, and the Research OS layer model.

Layer labels follow the Research OS design baseline:

- Layer 5 - Research Governance & Operations
- Layer 4 - Research Applications
- Layer 3 - Evidence / Contract / DAG Kernel
- Layer 2 - Provider / Model / Runtime Engines
- Layer 1 - Data / Compute / Artifact Infrastructure

Each placeholder describes the module's architecture role, public contract shape, and implementation highlights at system-design level. Runtime data, generated artifacts, local configuration, credentials, strategy-specific labels, and implementation logic are outside this review tree by construction.
