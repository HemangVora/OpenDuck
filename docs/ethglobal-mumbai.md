# ETHGlobal Mumbai (Nov 5–7, 2026) — use case for the duck

Written 2026-11-02. Source: https://ethglobal.com/events/mumbai/prizes (read that day).

## Reality check

- Hackathon window: Thu Nov 5 evening → Sat Nov 7. ~36 h of hacking.
- Servos are not ordered yet (3–5 day transit), printing is ~67 h. **The physical duck cannot walk by Nov 7.**
- 0G's Physical AI prize explicitly accepts **simulated builds for 1st/2nd** ("bring your own simulator: MuJoCo"). Only the $1,000 "best build on real hardware" needs hardware. Skip that one.
- Mumbai rule change: existing repos are **welcome** ("Extend Open Source: bring a repo you already maintain"). Upstream Open Duck Mini v2 + this repo are fine; disclose them. Max **three sponsor SDKs** per project.
- Upstream already ships a trained walking policy: `upstream/Open_Duck_Mini/BEST_WALK_ONNX_2.onnx`, runnable with `Open_Duck_Playground/playground/open_duck_mini_v2/mujoco_infer.py -o <onnx>`. Commands today come from the keyboard (`key_callback`: arrows = vx/vy/yaw, `h` toggles head mode). That keyboard hook is the seam we replace.

## The use case: "Imprint"

Ducklings imprint on the first creature they see and follow only it. This duck imprints on a **World-ID-verified human** and only takes orders from that human. Its brain (what to do next, where the target is) runs on **0G**; its body (balance, gait) is the local RL policy.

Why this is a real problem, not a gimmick: on-chain robot control (0G's own zerobot) lets *any wallet* dispatch commands to a public robot. For a machine that moves in a shared room, "any wallet" means bots. World ID gives one accountable, unique, fresh human in front of the protected action without revealing who they are. 0G gives a verifiable, replayable record of every decision the robot took.

### Decision loop (fits 0G's "brain not spinal cord" rule)

```
head camera frame (MuJoCo offscreen render) + human instruction
        │  every ~1 s (checkpoint)
        ▼
0G Private Computer: qwen-vision (OpenAI-compatible API)
  → {vx, vy, yaw, head_pitch, head_yaw, expression, reason}   + request_id
        │
        ▼
local ONNX walking policy @50 Hz (unchanged upstream BEST_WALK_ONNX_2)
        │
        ▼
episode log entry {t, frame_hash, instruction, request_id, command} → 0G Storage
```

- **Safe stop:** 0G unreachable or response invalid → command = zeros, duck stands still and shakes its head. Never substitutes a local guess (a fake decision disqualifies).
- **What breaks if 0G is removed:** the duck can still balance but can neither see nor decide; it stands still.

### World ID Agent Pass gate (protected action = the robot moving)

1. Unverified visitor sends "come here" → duck shakes head, refuses, logs `denied` (required unsuccessful path).
2. Hemang verifies via Agent Pass on the phone → backend validates the proof, binds a session to the duck (never trust the client result).
3. Session expires / cancelled → duck stops obeying (second unsuccessful path, cheap to show).
4. Required debrief: time to first success, friction, missing capability, one improvement.

### Demo script (video ≤ 3 min, also the live judge demo)

1. Stranger taps "come here" → refusal, denied entry in log.
2. Verify with World ID → duck "imprints" (looks up, happy expression).
3. "Walk to the red cup" → 0G vision finds the cup → duck walks there, bows. Side panel streams request IDs.
4. Pull the network → duck freezes (safe stop).
5. Replay viewer loads the episode from a 0G Storage root hash and re-plays it in MuJoCo.
6. The printed shell on the table: "this is the body; servos land next week". Sets up the **Continuity track** ("Keep Building on 0G", $3,000) at the next ETHGlobal with the real robot.

### Prizes targeted

| Prize | Amount | What it needs from us |
|---|---|---|
| 0G · Physical AI: Agents with a Body | $5,000 (1st 2,500 / 2nd 1,500) | 0G call in decision loop, request id per decision, episode log on 0G Storage, replayable sim, safe stop, contract addresses, TG + X handles |
| World · World ID Agent Pass | $5,000 (1st 2,500) | full journey + denied path + backend validation + debrief |
| Stretch: ENSv2 "agents as namespaces" | $7,000 pool | duck gets a subname; its operator key gets Enhanced Access Control rights to edit only `robot.status` / `robot.episode` text records. Only if ahead of schedule Saturday morning. |

Do not add a fourth SDK. Judges punish kitchen-sink projects and the rules cap SDKs at three.

Rejected alternatives: Hedera x402 "duck pays for its own inference" (money loop is roundabout for a sim robot; "revenue from the team's own wallet" is called out as not wanted); Arkiv as episode DB (0G already requires the log on 0G Storage; two stores dilute the story); Arc / Uniswap / Definitive (no honest fit for a robot).

## Build plan

### Before the event (allowed: tooling and setup; keep hackathon features in fresh dated commits)
- Playground running on the Mac: `uv run playground/open_duck_mini_v2/mujoco_infer.py -o BEST_WALK_ONNX_2.onnx`.
- Offscreen render from a camera on the head body in `open_duck_mini_v2.xml` (add a `<camera>` to the head; `mujoco.Renderer`).
- Accounts: 0G Private Computer API key + Galileo testnet faucet; World developer portal app (Agent Pass); repo public with licence.
- Read: 0G compute docs, 0G Storage SDK, Agent Pass docs. Attend the 0G workshop Thu 15:30 and World workshop Thu 17:30.

### Day 1 (Thu night)
- `duck/brain/`: replace `key_callback` with a command source (ZMQ or HTTP) that `mujoco_infer` polls.
- 0G vision call → strict JSON schema → command; invalid → safe stop.
- Episode logger (JSONL) with request ids.

### Day 2 (Fri)
- World ID Agent Pass flow: web page + backend verify + session binding; denied/expired paths.
- Upload each episode to 0G Storage; show root hash in UI.
- Side panel: live frame, instruction, 0G request id, command, log.

### Day 3 (Sat)
- Replay viewer (load episode from 0G Storage, replay commands in MuJoCo).
- README (setup, architecture diagram, what breaks without 0G, contract addresses), World debrief, demo video, submission.
