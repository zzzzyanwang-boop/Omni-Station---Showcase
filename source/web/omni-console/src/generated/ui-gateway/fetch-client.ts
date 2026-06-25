/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/generated/ui-gateway/fetch-client.ts
 * System layer: Productization Boundary Layer - generated API/read-model contracts
 * Review role: gateway client and backend contract boundary; generated or typed client boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: UiGatewayFetchClientConfig.
 * - exported functions/components/constants: createUiGatewayFetchClient.
 * - local helper functions: normalizeBaseUrl, generateRequestId.
 *
 * Reviewable responsibilities:
 * - Represents generated client or catalog surface used by the console.
 * - Keeps API shape reviewable without exposing backend implementation logic.
 * - Separates generated read-model access from hand-written page behavior.
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
