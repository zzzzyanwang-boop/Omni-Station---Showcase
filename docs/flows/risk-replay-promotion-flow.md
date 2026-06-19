# Risk, Replay, and Promotion Flow

This flow separates signal evidence from economic and runtime evidence.

```text
candidate signal evidence
  -> risk identity ledger
  -> beta / sector / style sidecar checks
  -> deterministic replay packet
  -> fill / slippage / latency cost evidence
  -> economic gate
  -> review gate
  -> promotion packet or blocked closure
```

## Boundary Rule

Offline evidence cannot directly enable paper, live, broker, OMS, or model-serving posture. A separate promotion packet is required.

