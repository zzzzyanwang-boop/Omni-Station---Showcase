/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/lib/gateway-fail-closed.ts
 * System layer: Productization Boundary Layer - typed UI client, fail-closed state, and read-model helpers
 * Review role: gateway client and backend contract boundary; fail-closed UI/runtime boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: FailClosedErrorState, FailClosedStatus.
 * - exported functions/components/constants: mapGatewayErrorToFailClosed, isGatewayFixtureFallbackEligible.
 * - local helper functions: includesKeyword, classifyHttpError.
 *
 * Reviewable responsibilities:
 * - Defines reusable UI-side contracts, gateway helpers, runtime adapters, or state normalization.
 * - Keeps backend interaction typed and centralized rather than embedded across pages.
 * - Provides a stable surface for operator pages, generated clients, and validation tests.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 * - Uses local helpers behind the exported boundary; helper names are retained only as structural signals.
 * - Participates in a composed dependency graph; import targets are not copied into this file body.
 *
 * Contract shape:
 * - Inputs: typed request state, read-model payload, operator action, route parameter, or gateway response fixture.
 * - Outputs: normalized UI state, typed client result, fail-closed error state, validation signal, or reviewable read-model update.
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
