/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/lib/data-source-mode.ts
 * System layer: Productization Boundary Layer - typed UI client, fail-closed state, and read-model helpers
 * Review role: data-source-mode source boundary in the retained implementation tree.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: ResolvedDataSourceMode, DataSourceMode.
 * - exported functions/components/constants: dataSourceModeLabel, resolveDataSourceMode, STRICT_GATEWAY_MODE, FIXTURE_FALLBACK_ENABLED, DATA_SOURCE_MODE.
 * - local helper functions: parseEnvBoolean.
 *
 * Reviewable responsibilities:
 * - Defines reusable UI-side contracts, gateway helpers, runtime adapters, or state normalization.
 * - Keeps backend interaction typed and centralized rather than embedded across pages.
 * - Provides a stable surface for operator pages, generated clients, and validation tests.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 * - Uses local helpers behind the exported boundary; helper names are retained only as structural signals.
 *
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
