# Source-Shaped Skeleton

This directory mirrors a public-safe subset of the private OmniStation source tree.

Every file keeps the original public-safe path and filename, but the implementation body has been replaced by a short architecture summary. These files are intentionally not executable. They are included to show ownership boundaries, module responsibilities, and how the Research OS layer model is organized without disclosing source code or research IP.

Layer labels follow the Research OS design baseline:

- Layer 5 - Research Governance & Operations
- Layer 4 - Research Applications
- Layer 3 - Evidence / Contract / DAG Kernel
- Layer 2 - Provider / Model / Runtime Engines
- Layer 1 - Data / Compute / Artifact Infrastructure

Excluded from this skeleton: data, runtime output, configs with strategy-specific names, task files, logs, model artifacts, credentials, private paths, and modules whose filename would reveal sensitive research lines.
