/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/generated/gateway-client.ts
 * System layer: Productization Boundary Layer - generated API/read-model contracts
 * Review role: gateway client and backend contract boundary; generated or typed client boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: OperationSpec, InvokeOperationOptions, GatewayClientConfig, GatewaySuccess, GatewayErrorBody, HttpMethod, RiskLevel, OperationId, Primitive, QueryValue, PathParams, QueryParams, plus 2 more.
 * - exported functions/components/constants: OPERATIONS, OPERATION_IDS, HIGH_RISK_OPERATION_IDS.
 * - local helper functions: normalizeBaseUrl, resolveFetchImpl, buildPath, buildQuery, safeJsonParse.
 *
 * Reviewable responsibilities:
 * - Represents generated client or catalog surface used by the console.
 * - Keeps API shape reviewable without exposing backend implementation logic.
 * - Separates generated read-model access from hand-written page behavior.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 * - Uses local helpers behind the exported boundary; helper names are retained only as structural signals.
 *
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
