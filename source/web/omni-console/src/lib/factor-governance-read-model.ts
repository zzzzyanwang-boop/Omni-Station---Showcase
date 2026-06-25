/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/lib/factor-governance-read-model.ts
 * System layer: Productization Boundary Layer - typed UI client, fail-closed state, and read-model helpers
 * Review role: factor research and governance surface; governance lifecycle and review-state surface.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: TopKMetricRow, FactorGovernanceSummary, PromotionGovernanceSummary, GovernanceTone.
 * - exported functions/components/constants: governanceStatusTone, parseTopKMetrics, parseFactorGovernanceSummary, parsePromotionGovernanceSummary, summarizeBlockedReasons.
 * - local helper functions: asObject, asArray, asString, asNumber, uniqueStrings.
 *
 * Reviewable responsibilities:
 * - Defines reusable UI-side contracts, gateway helpers, runtime adapters, or state normalization.
 * - Keeps backend interaction typed and centralized rather than embedded across pages.
 * - Provides a stable surface for operator pages, generated clients, and validation tests.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 * - Uses local helpers behind the exported boundary; helper names are retained only as structural signals.
 *
 * Contract shape:
 * - Inputs: typed request state, read-model payload, operator action, route parameter, or gateway response fixture.
 * - Outputs: normalized UI state, typed client result, fail-closed error state, validation signal, or reviewable read-model update.
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
