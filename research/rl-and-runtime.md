# Open Duck Mini v2: RL training + on-robot runtime, as actually implemented

Research notes for writing our own Python runtime and training our own walking policy
for a modified duck (12 V 30 kg·cm ST3215, 3S pack, Radxa Zero 3W, camera + ToF head).

Sources were cloned shallowly (2026-10-28) into
`/private/tmp/claude-501/-Users-hemangvora/c8a30d1f-0498-4660-9327-b47c73ee9657/scratchpad/agents/rl/`:

| Repo | Branch / HEAD | Notes |
|---|---|---|
| apirrone/Open_Duck_Mini_Runtime | `v2` @ 376de654 (2026-09-08 "Added ISO release") | on-robot runtime |
| apirrone/Open_Duck_Playground | `main` @ b9be205a (2025-08-05 "fix onnx export") | MJX/Brax PPO training |
| apirrone/Open_Duck_Mini | `v2` @ b23317a4 (2026-01-31) | docs, hub, ONNX policies |
| apirrone/Open_Duck_reference_motion_generator | `main` @ 3d7bc6fd (2025-04-03) | Placo gait -> polynomial ref motion |
| Rhoban/bam | `main` @ e9a619d5 (2026-09-13) | actuator identification |

Paths below are relative to those clones unless given as URLs.

---

## 1. Runtime control loop (Open_Duck_Mini_Runtime, branch v2)

### 1.1 The PWM-control files you asked about no longer exist

`hwi_feetech_pwm_control.py`, `feetech_pwm_control.py`, `feetech.py`, `hwi.py` are **not on v2 HEAD**.
GitHub history (`/commits?sha=v2&path=.../hwi_feetech_pwm_control.py`) shows they were deleted in
commit `cdfb5714` "cleaning up" (2025-03-17). Their last version is at commit
`1fc8baa8acadb93830d5ecd993130d793cacf72b` ("rustypot", 2025-02-24), where the tree contained
`feetech.py`, `feetech_pwm_control.py`, `feetech_pwm_control_rustypot.py`, `hwi.py`,
`hwi_feetech_pwm_control.py`, `hwi_feetech_pypot.py`, `hwi_feetech_sdk.py`, `io_330.py`,
`scripts/v2_rl_walk.py` (AWD/Isaac-era walk script).

What that older PWM path did (read from the 1fc8baa8 raw files):

* `feetech_pwm_control.py`: `from pypot.feetech import FeetechSTS3215IO`, `/dev/ttyACM0`,
  `baudrate=1000000`, servos put in **mode 2 (PWM mode)** via `self.io.set_mode({id: 2 ...})`;
  a daemon thread at `self.control_freq = 100  # Hz` reads present positions, computes
  `errors = goal_positions - present_positions` (degrees), `pwms = self.kps * errors`,
  `np.clip(pwms, -1000, 1000)`, packs `(direction_bit << 10) | magnitude` and writes it with
  `self.io.set_goal_time(...)` (the STS3215 reuses the goal-time register as the PWM register
  in mode 2). Default `kps = 32`. **P only, no kd**; velocity was a finite difference every 2nd
  cycle and unused in the control law.
* `feetech_pwm_control_rustypot.py`: same law, but on `rustypot.feetech(port, 1000000)` using
  `set_mode(ids, 2)`, `read_present_position(ids)`, `set_goal_time(ids, goal_times)`,
  `disable_torque/enable_torque`, 100 Hz.
* `hwi_feetech_pwm_control.py`: joint dict (same IDs as today), degrees<->radians, per-joint
  software offsets, `turn_on()` = low kp (8) -> init pose -> kp 32.
* `hwi.py`: Dynamixel XL330 driver from the v1 duck (3 Mbaud, P=1280 D=8 legs) — irrelevant to v2.
* `scripts/v2_rl_walk.py` (old AWD/Isaac policy): 50 Hz, kp 32, action_scale 0.25, obs =
  projected gravity (3) + dof pos (16, incl. 2 fake antennas) + dof vel (16) + feet contacts (2)
  + previous action (16) + commands (3) = 56; IMU read as quaternion -> `quat_rotate_inverse`.

So the "own P controller over PWM" design was abandoned in March 2025. **The shipped v2 runtime
commands goal positions and lets the servo's internal P controller run**, which is also exactly
what the MuJoCo `<position>` actuator models.

### 1.2 What runs today: `scripts/v2_rl_walk_mujoco.py` + `rustypot_position_hwi.py`

Hardware interface `mini_bdx_runtime/mini_bdx_runtime/rustypot_position_hwi.py`:

```python
self.io = rustypot.feetech(usb_port, 1000000)        # /dev/ttyACM0, 1 Mbaud
self.kps = np.ones(len(self.joints)) * 32            # default kp (firmware units)
self.kds = np.ones(len(self.joints)) * 0
self.low_torque_kps = np.ones(len(self.joints)) * 2
...
def set_position_all(self, joints_positions):        # radians
    ids_positions = {self.joints[j]: pos + self.joints_offsets[j] for j, pos in joints_positions.items()}
    self.io.write_goal_position(list(self.joints.values()), list(ids_positions.values()))
def get_present_positions(...):  self.io.read_present_position(ids)   # rad, minus offsets
def get_present_velocities(...): self.io.read_present_velocity(ids)   # rad/s
```

* **Library**: `rustypot==0.1.0` (Rust + pyo3, Pollen Robotics), pinned in `setup.cfg` together
  with `onnxruntime==1.18.1`, `numpy==1.26.4`, `adafruit-circuitpython-bno055==5.4.13`,
  `scipy==1.15.1`, `pygame==2.6.0`, `pypot @ git+...@support-feetech-sts3215` (pypot is used
  only by the configuration scripts). Every call passes the full ID list, so each loop is one
  **sync read of positions, one sync read of velocities, one sync write of goal positions**
  (14 servos). Note: current upstream rustypot (v1.0.0 .. v1.13.1) has a different Python API
  (`Sts3215PyController(serial_port, baudrate, timeout)`, `sync_read_present_position([ids])`,
  `sync_write_goal_position([ids],[vals])`, `read_register`/`write_register`); the 0.1.0 API
  (`rustypot.feetech(...)`, `set_kps`, `read_present_velocity`) is not documented anywhere I could
  find, so for our own runtime use the current `Sts3215PyController` or `scservo_sdk` directly.
* **Gains written to servos**: `start()` in the walk script sets `kps = [p]*14` with `-p` default
  **30** (HWI default 32), head joints 5:9 lowered to **8**, `kds = 0`. `turn_on()` first writes
  `low_torque_kps = 2`, moves to `init_pos`, waits 1 s, then writes the full kps.
  The one-time EEPROM configuration (`scripts/configure_motor.py`, run per servo before
  assembly; `docs/configure_motors.md`) does:
  `set_mode 0` (position), `set_maximum_acceleration 0`, `set_acceleration 0`, `P=32, I=0, D=0`,
  `change_id`, then `set_goal_position 0` so you can mount the horn at zero.
  Maintainer on Open_Duck_Mini issue #20: "the 17.8 in mujoco corresponds to 32 in the motors
  firmware units".
* **Loop rate**: `control_freq = 50` Hz (`-c 50`), `time.sleep(max(0, 1/50 - took))`; it prints
  "Policy control budget exceeded by ..." when late (users on Pi 5 see 2–35 ms overruns,
  runtime issue #40). IMU is polled in its own thread at 50 Hz, gamepad thread at 20 Hz.
* **Joint order and IDs** (dict order is the policy order and equals the MJCF actuator order):

  ```
  left_hip_yaw 20, left_hip_roll 21, left_hip_pitch 22, left_knee 23, left_ankle 24,
  neck_pitch 30, head_pitch 31, head_yaw 32, head_roll 33,
  right_hip_yaw 10, right_hip_roll 11, right_hip_pitch 12, right_knee 13, right_ankle 14
  ```
  Antennas are not on the bus (driven by GPIO PWM in `antennas.py`). `rl_utils.py` still carries
  the 16-joint Isaac ordering helpers; they are unused by the v2 script.
* **Offsets**: `~/duck_config.json` -> `joints_offsets` (radians, see `example_config.json`),
  loaded by `duck_config.py`; added on write, subtracted on read. Found interactively with
  `scripts/find_soft_offsets.py` (torque off one joint, move it to the mechanical zero, record
  `new_pos - current_pos`). `init_pos` (standing pose, rad) is hard-coded in the HWI and equals
  the MJCF `home` keyframe:
  `L: 0.002, 0.053, -0.63, 1.368, -0.784 | head 0,0,0,0 | R: -0.003, -0.065, 0.635, 1.379, -0.796`.

### 1.3 Observation vector (101 floats), `RLWalk.get_obs()`

| # | component | size | source / scaling |
|---|---|---|---|
| 1 | gyro | 3 | BNO055 `imu.gyro` (rad/s), body frame after axis remap |
| 2 | accelerometer | 3 | BNO055 `imu.acceleration` (m/s², includes gravity) |
| 3 | commands | 7 | `[vx, vy, wz, neck_pitch, head_pitch, head_yaw, head_roll]` from Xbox pad |
| 4 | dof_pos - init_pos | 14 | rad |
| 5 | dof_vel * 0.05 | 14 | rad/s × `dof_vel_scale` |
| 6 | last_action | 14 | raw policy output (tanh, [-1,1]) |
| 7 | last_last_action | 14 | |
| 8 | last_last_last_action | 14 | |
| 9 | motor_targets | 14 | previous commanded targets (rad, absolute) |
| 10 | feet_contacts | 2 | GPIO foot switches (`feet_contacts.py`, pins D22/D27, pull-up, active low) |
| 11 | imitation_phase | 2 | `[cos, sin](2π · imitation_i / nb_steps_in_period)` |

Total 3+3+7+14+14+42+14+2+2 = **101** (matches "Observation size: 101" in Playground issue #19).
The ONNX input name is `obs`, shape `(1, 101)`; `onnx_infer.py` runs
`onnxruntime` CPUExecutionProvider with `awd=True` (batch dim added).

**IMU**: `raw_imu.py` (the one actually imported) uses `adafruit_bno055.BNO055_I2C` in
`NDOF_MODE`, with `axis_remap` (Y,X,Z and sign flips; `imu_upside_down` in duck_config picks the
variant), optional saved calibration offsets (`imu_calib_data.pkl`), and only exposes
`{"gyro","accelero"}`. **No quaternion and no projected gravity are used by the deployed
policy** (that is the older `imu.py`, which converts the BNO055 quaternion to Euler, subtracts a
pitch bias, and returns a scalar-last quaternion for the Isaac/AWD policy). `pitch_bias` is
still a CLI arg but has no effect on `raw_imu.Imu`.

**Command injection**: `xbox_controller.py` (pygame) maps left stick to
`vx ∈ [-0.15, 0.15]`, `vy ∈ [-0.2, 0.2]`, right stick x to `wz ∈ [-1, 1]`; Y toggles a head
mode where sticks fill commands[4:7] (neck_pitch command is forced 0). The 7 commands go into
the obs unchanged, and **the head commands are additionally added to the policy's head targets**:

```python
head_motor_targets = self.last_commands[3:] + self.motor_targets[5:9]
self.motor_targets[5:9] = head_motor_targets
```
(In sim the equivalent `motor_targets.at[5:9].set(command[3:])` is commented out and there is no
head-tracking reward active, so head commands are pure observation noise during training.)

**Action path**: 14-dim action, `motor_targets = init_pos + action * 0.25` (`-a 0.25`).
The 5.24 rad/s slew-rate clip used in sim is **commented out** on the robot. Optional
`LowPassActionFilter` (`--cutoff_frequency`, first-order, alpha from cutoff/control freq) is
applied to the targets after a 1 s warm-up; users report running with `--cutoff_frequency 40`.
Phase clock: `imitation_i += phase_frequency_factor + phase_frequency_factor_offset` per tick
(LB held -> 1.3 "sprint", D-pad adjusts offset by ±0.05, offset persisted in duck_config),
modulo `PRM.nb_steps_in_period` read from `polynomial_coefficients.pkl` (the only thing the
runtime uses the reference motion for).

**Safety / fall handling**: none. There is no tilt check, no torque cut, no current/temperature
monitoring. "A" pauses the loop (servos keep holding), Ctrl-C stops expression threads and prints
"TURNING OFF" **without calling `hwi.turn_off()`**. `turn_off.py` exists as a separate script
(`io.disable_torque`). `check_voltage.py` reads bus voltage but is not used in the loop.
`checklist.md`/`TODO.md`: offsets flashing to EEPROM and an automatic pre-flight script are
unfinished.

### 1.4 Platform notes

* Target board is Raspberry Pi Zero 2W (Raspberry Pi OS Lite 64-bit); README also has Pi 5 notes
  (`pip uninstall RPi.GPIO; pip install lgpio`), udev `latency_timer=1` for FTDI serial, I2C.
  Prebuilt image 0.2.3 (`docs/INSTALL.md`) is Pi-Zero-2W only. GPIO access is through
  Adafruit Blinka (`board`, `busio`, `digitalio`) — for Radxa Zero 3W check Blinka board
  detection (not verified here) or replace with `gpiod`/`smbus2`.
* No Radxa mention anywhere in the three repos' issues. Other boards: Pi 5 GPIO/timing issues
  (runtime #40), Jetson Orin Nano request (Open_Duck_Mini #42), CRC/checksum Rust panic on
  Pi Zero while walking (Open_Duck_Mini #49), `set_kps()` parsing error (runtime #26).

---

## 2. Training (Open_Duck_Playground)

### 2.1 Setup

`pyproject.toml`: python ≥3.11, `jax[cuda12]>=0.5.0`, `playground>=0.0.3` (= mujoco_playground
from PyPI), `tensorflow>=2.18`, `tf2onnx`, `onnxruntime`, `mediapy`, `framesviewer`.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv run playground/open_duck_mini_v2/runner.py --task flat_terrain_backlash --num_timesteps 300000000
uv run tensorboard --logdir=checkpoints
uv run playground/open_duck_mini_v2/mujoco_infer.py -o <ckpt>.onnx [--model_path .../scene_flat_terrain_backlash.xml]
```
README "Current win" is exactly that `flat_terrain_backlash` / 300 M command.
`runner.py` default `--num_timesteps` is 150 M (300 M commented out). Tasks
(`constants.py::task_to_xml`): `flat_terrain`, `rough_terrain`, `flat_terrain_backlash`,
`rough_terrain_backlash` -> `xmls/scene_*.xml`, which `<include>` either
`open_duck_mini_v2.xml` or `open_duck_mini_v2_backlash.xml` and add the floor + `home` keyframe.
The 50 Hz robot ONNX is produced automatically at every eval checkpoint by
`playground/common/export_onnx.py` (policy MLP rebuilt in Keras with the observation
normalizer `mean/std["state"]` baked in, `tanh(loc)` output, opset 11, input `obs`, output
`continuous_actions`; also always overwrites `./ONNX.onnx`). Known breakage: TF has no CUDA
kernels for RTX 50xx -> export crashes with `CUDA_ERROR_INVALID_HANDLE` (issues #16, #19);
work around by hiding the GPU from TF (`CUDA_VISIBLE_DEVICES` for TF only / export on CPU).

### 2.2 Where the robot constants live

* `playground/open_duck_mini_v2/constants.py`: XML paths, `FEET_SITES = left_foot/right_foot`,
  `FEET_GEOMS = *_foot_bottom_tpu`, `ROOT_BODY = "trunk_assembly"`, sensor names
  (`gyro`, `accelerometer`, `local_linvel`, `upvector`, `global_linvel`, `global_angvel`),
  `JOINTS_ORDER_NO_HEAD` (10 leg joints; used only to build per-joint pos-noise scales — note
  it is indexed against 14 actuators, so the right-leg noise scales land on head joints).
* `playground/open_duck_mini_v2/base.py`: loads MJCF, separates actuated joints from
  `*_backlash` joints and the freejoint, exposes sensor getters.
* `playground/open_duck_mini_v2/joystick.py`: `default_config()`, obs, rewards, commands.
* `playground/common/randomize.py`, `rewards.py`, `custom_rewards.py` (imitation),
  `poly_reference_motion.py` (JAX), `runner.py` (Brax PPO), `export_onnx.py`.
* MJCF: `xmls/open_duck_mini_v2*.xml`, `joints_properties.xml`, `sensors.xml`, `config.json`
  (onshape-to-robot config), `assets/*.stl`.

### 2.3 Sim config (`joystick.py::default_config`)

`sim_dt 0.002`, `ctrl_dt 0.02` (decimation 10 -> 50 Hz policy), `episode_length 1000` (20 s),
`action_scale 0.25`, `dof_vel_scale 0.05`, `max_motor_velocity 5.24` rad/s
(`USE_MOTOR_SPEED_LIMITS=True` clips target change per step to ±5.24·0.02 = 0.105 rad),
`soft_joint_pos_limit_factor 0.95`. MJCF `<option iterations="1" ls_iterations="5">`,
`eulerdamp` disabled (MJX speed settings).

Commands sampled per episode and re-sampled every 500 steps (10 % chance all-zero):
`lin_vel_x [-0.15, 0.15]`, `lin_vel_y [-0.2, 0.2]`, `ang_vel_yaw [-1, 1]`,
`neck_pitch [-0.34, 1.1]`, `head_pitch [-0.78, 0.78]`, `head_yaw [-1.5, 1.5]`, `head_roll [-0.5, 0.5]`.

Observation (`_get_obs`, "state" key, policy input) is built identically to the runtime:
noisy gyro, noisy accelerometer, command(7), joint_angles(+backlash angle) − default(14),
joint_vel·0.05, last/last_last/last_last_last action, motor_targets, contact(2),
imitation_phase(2). The critic gets `privileged_state` (adds true gyro/accel/gravity/linvel,
angvel, root height, actuator forces, feet velocities, air time, full reference frame).
Quirk: `accelerometer.at[0].set(accelerometer[0] + 1.3)` is not assigned back, so the +1.3 m/s²
x-bias meant to mimic the real IMU is **not applied in training** but **is** applied in
`mujoco_infer.py` (`accelerometer[0] += 1.3`).

Noise (`noise_config`, level 1.0, uniform ±scale): hip_pos 0.03, knee_pos 0.05, ankle_pos 0.08
rad, joint_vel 2.5 rad/s, gyro 0.1, accelerometer 0.05, gravity 0.1; action delay 0–3 steps,
IMU delay 0–3 steps (delay applied to the gravity vector, which is not in the policy obs).
Pushes: every 5–10 s, base xy velocity kick 0.1–1.0 m/s. Reset: xy ±5 cm, random yaw, joint
qpos × U(0.5, 1.5), base qvel ±0.05.

Termination: `upvector_z < 0` (trunk past horizontal) or NaN.

### 2.4 Actuator model (MJCF defaults) and where it comes from

`xmls/open_duck_mini_v2_backlash.xml` (the model used by `flat_terrain_backlash`):

```xml
<default class="sts3215">
  <joint damping="0.56" frictionloss="0.068" armature="0.027"/>
  <position kp="17.11" kv="0.0" forcerange="-3.23 3.23"/>
</default>
<default class="backlash">   <!-- +/- 0.5 deg -->
  <joint damping="0.01" frictionloss="0" armature="0.01" limited="true"
         range="-0.008726646259971648 0.008726646259971648"/>
</default>
```
Each of the 10 leg joints has a stacked passive `<joint name="*_backlash" class="backlash"/>` on
the same axis (head joints have none). `joints_properties.xml` (the onshape-to-robot
`additional_xml`) carries the earlier numbers `damping 0.60, frictionloss 0.052, armature 0.028,
kp 17.8, forcerange ±3.35`; the plain `open_duck_mini_v2.xml` has `kp 13.37` with the same
joint params. Joint ranges come from Onshape (hip yaw ±30°, hip roll ±25°, hip pitch −70°/+30°,
knee ±90°, ankle ±90°, neck −20°/+65°, head pitch ±45°, head yaw ±160°, head roll ±30°);
actuators use `inheritrange="1"` so ctrlrange = joint range.

These come from **BAM** (`docs/sim2real.md`: "BAM allows us to export the main identified
parameters to mujoco units (using bam.to_mujoco)"). `bam/to_mujoco.py`
(`voltage_controlled_to_mujoco`):

```
forcerange   = vin * kt / R
armature     = model.armature
kp           = error_gain * kp_fw * vin * max_pwm * kt / R
damping      = friction_viscous + kt² / R          # back-EMF folded into damping
frictionloss = friction_base
```
with `bam/feetech/actuator.py` STS3215 constants `vin=7.4, kp=32, error_gain=0.166, max_pwm=0.97`,
`default_max_velocity = 3400·2π/4096 = 5.22 rad/s`, and `bam/params/feetech_sts3215_7_4V/m1.json`
(`kt 1.178, R 2.479, armature 0.0261, friction_base 0.0515, friction_viscous 0.0599,
max_velocity 5.288, command_delay 1.0 ms`). Plugging in gives kp ≈ 18.1, forcerange ≈ 3.5,
damping ≈ 0.62, frictionloss 0.052, armature 0.026 — i.e. the XML numbers (an earlier fit). The
runtime's `max_motor_velocity = 5.24` is "from system identification" (runtime issue #7; also
equals the STS3215 7.4 V no-load 50 rpm). `to_mujoco.py` is now marked **deprecated** by BAM:
the full m6 model (Stribeck + load-dependent friction, `m6.json`) cannot be collapsed into
constant kp/damping; BAM now offers `bam.mujoco.MujocoController` (CPU) and
`bam.mjlab.BamActuatorCfg` (MuJoCo-Warp / mjlab, with `vin_range`, `vin_drop_resistance_range`,
`friction_scale_range`, command delay randomization). The runtime repo has `mjlab_test` /
`new_mjlab_test` / `new_firmware` branches, so upstream is moving that way.

**For 12 V servos**: BAM has no ST3215-12V set, but it has `waveshare_st3025` (12 V, 30 kg·cm
class, contributed from the "duck_mini_pro_headless" project by i1Cps): `bam/waveshare/actuator.py`
uses `vin=12, kp=32, error_gain=0.166 (inherited), max_pwm=1.0`, `m1.json`: `kt 1.620, R 3.731,
armature 0.0044, friction_base 0.0519, friction_viscous 0.0201, error_gain_ratio 1.18`.
Through `to_mujoco` that is roughly `kp ≈ 28–33, forcerange ≈ ±5.2 N·m, damping ≈ 0.72,
frictionloss 0.052, armature 0.004`. Treat it as a starting point only; the honest path is to run
BAM's pendulum identification on one of our ST3215-12V (docs `identification/` in bam) and fit
m1 (for MJX position actuator) plus m6 (for mjlab/BAM controller). Also re-measure the no-load
speed: 12 V ST3215 is spec'd slower than the 7.4 V 50 rpm unit, so `max_motor_velocity` and the
reference gait period may need to change.

### 2.5 Domain randomization (`playground/common/randomize.py`)

floor friction U(0.5, 1.0); dof frictionloss × U(0.9, 1.1) (actuated joints only);
armature × U(1.0, 1.05); torso CoM `body_ipos` ± 5 cm; all body masses × U(0.9, 1.1);
torso mass + U(−0.1, 0.1) kg; `qpos0` ± 0.03 rad; actuator kp × U(0.9, 1.1) (gainprm and
biasprm together). Hard-coded `TORSO_BODY_ID = 1`, `FLOOR_GEOM_ID = 0`.

### 2.6 Rewards (`joystick.py::_get_reward`, weights in `reward_config.scales`)

| term | weight | definition |
|---|---|---|
| tracking_lin_vel | 2.5 | exp(−(ex² + max(|ey|−0.1,0)²)/0.01) on local linvel |
| tracking_ang_vel | 6.0 | exp(−(wz_cmd − gyro_z)²/0.01) |
| torques | −1e-3 | Σ actuator_force² |
| action_rate | −0.5 | Σ (a − a_prev)² |
| stand_still | −0.2 | (Σ|q−q0| + Σ|q̇|) when ‖cmd[:3]‖ < 0.01, head included |
| alive | 20.0 | 1 |
| imitation | 1.0 | `custom_rewards.py`: exp-tracking of ref base lin/ang vel + −15·Σ(q−q_ref)² (legs only) −1e-3·Σ(q̇−q̇_ref)² + Σ(contact == ref_contact), zero when cmd ≈ 0 |

Sum × dt (0.02), clipped ≥ 0. Feet air time, swing peak, orientation etc. exist in `rewards.py`
but are not enabled.

### 2.7 PPO hyper-parameters (`common/runner.py`)

Taken from `mujoco_playground.config.locomotion_params.brax_ppo_config("BerkeleyHumanoidJoystickFlatTerrain")`
with `num_timesteps` overridden: `num_envs 8192`, `batch_size 256`, `num_minibatches 32`,
`unroll_length 20`, `num_updates_per_batch 4`, `discounting 0.97`, `learning_rate 3e-4`,
`entropy_cost 0.005`, `clipping_epsilon 0.2`, `max_grad_norm 1.0`, `normalize_observations True`,
`num_evals 15`, `num_resets_per_eval 10`, policy MLP (512, 256, 128) swish on `state`, value MLP
(512, 256, 128) on `privileged_state`. Checkpoints via Orbax + ONNX at each eval; JAX
persistent compile cache in `.tmp/jax_cache`. `--restore_checkpoint_path` resumes.
Wall-clock: **not reported anywhere in the repos/issues**. Reference point: the MuJoCo Playground
paper (arXiv 2502.08844) trains Berkeley Humanoid joystick (same PPO config, 150 M steps) in
"under 15 minutes on two RTX 4090"; the duck adds 10 backlash joints and mesh-foot contacts, so
expect roughly 1–3 h for 300 M steps on one RTX 4090 (my estimate, verify with a short run).

### 2.8 Swapping masses / inertias (heavier battery, camera + ToF head)

Pipeline (`docs/sim2real.md`, `docs/prepare_robot.md`, `xmls/config.json`):
Onshape doc `64074dfcfa379b37d8a47762` -> `onshape-to-robot` with `outputFormat mujoco`,
`simplify_stls`, `ignore` lists (everything but `foot_bottom_tpu` is visual-only; electronics are
dropped from geometry but their mass is in the assembly), `joint_properties.default.class =
sts3215`, `additional_xml = [sensors.xml, joints_properties.xml]`. Part masses are overridden in
Onshape with slicer estimates (infill). After export you must by hand (comment in config.json):
wrap everything in `<body name="base"><freejoint name="floating_base"/><site name="imu"
pos="-0.08 0 0.05"/>`, keep the sensors block, add `<position>` actuators in the joint order
above, add the `*_backlash` joints, and the `home` keyframe.

Required named sites/sensors: site `imu` (gyro, velocimeter `local_linvel`, accelerometer,
framezaxis `upvector`, framexaxis `forwardvector`, framelinvel `global_linvel`, frameangvel
`global_angvel`, framepos, framequat), sites `left_foot`/`right_foot` (framelinvel
`*_global_linvel`, framexaxis `*_upvector`, framepos `*_pos`), collision geoms named
`left_foot_bottom_tpu`/`right_foot_bottom_tpu`, geom `floor`, body `trunk_assembly`,
bodies `foot_assembly`/`foot_assembly_2` (used by `mujoco_infer_base.get_feet_contacts`).

Quick path without Onshape: edit the `<inertial>` blocks directly. Current values:
`trunk_assembly mass 0.6985 kg, pos (-0.048, 0, 0.038), fullinertia 1.68e-3 3.44e-3 2.93e-3 ...`;
`head_assembly mass 0.4066 kg` (includes Pi Zero, speaker, eyes); legs per side ≈ 0.414 kg;
total ≈ 2.11 kg. Add our pack/camera/ToF as extra mass+inertia (parallel-axis) to those two
bodies, or add child bodies with their own `<inertial>` and no geoms. DR already covers ±10 %
mass, ±0.1 kg torso and ±5 cm CoM, so moderate changes are partially absorbed, but a 3S pack
(~+0.1–0.2 kg, different position) shifts the standing CoM enough that `init_pos`/`home` and the
reference gait's `walk_com_height`/`walk_trunk_pitch` should be re-checked.

---

## 3. Reference motion (Open_Duck_reference_motion_generator)

* Placo kinematic walk engine (`placo_walk_engine.py`: `placo.HumanoidRobot(urdf)`,
  `WalkPatternGenerator`, `FootstepsPlannerRepetitive`, `KinematicsSolver` with
  `set_velocity_limits(12.0)` rad/s). `gait_generator.py` records at **FPS = 50** frames of
  `[root_pos(3), root_quat(4), joints(16 incl. antennas), left_toe(3), right_toe(3),
  world_linvel(3), world_angvel(3), joint_vel(16), toe vels(6), foot_contacts(2)]` plus
  `Placo` metadata (`period = 2·single_support + 2·double_support`, ratios, com height ...).
  File name `<name>_<vx>_<vy>_<wz>.json`.
* `scripts/auto_waddle.py --duck open_duck_mini_v2 --sweep` sweeps
  `robots/open_duck_mini_v2/auto_gait.json`: dx −0.04..0.06, dy ±0.03 (step 0.02),
  dtheta ±0.3 (step 0.07), starting from `placo_presets/medium.json`; filters out gaits slower
  than 0.05 m/s or faster than 0.15 m/s. `placo_defaults.json` (v2): `single_support_duration
  ≈ 0.17 s`, `double_support_ratio 0.18`, `walk_com_height 0.20`, `walk_foot_height 0.04`,
  `walk_trunk_pitch −3°`, `feet_spacing 0.16`, `foot_length 0.06` (period ≈ 0.40 s).
* `scripts/fit_poly.py` cuts one period (`start_offset = startend_double_support_ratio·fps`,
  `nb_steps_in_period = period·fps`), fits a **degree-15 polynomial** per dimension over
  t ∈ [0,1] for joints pos (16), joints vel (16), contacts (2), base lin vel (3), base ang vel (3)
  = 40 dims, and writes `polynomial_coefficients.pkl` = dict `"<dx>_<dy>_<dtheta>"` ->
  `{coefficients, period, fps, frame_offsets, start_offset, nb_steps_in_period,
  startend_double_support_ratio}`. `PolyReferenceMotion.get_reference_motion(dx,dy,dtheta,i)`
  picks the nearest grid point and evaluates the polynomials.

**Does it need regenerating for a heavier robot or slower servos?** It is purely kinematic
(IK on the URDF): mass does not enter, and the 12 rad/s Placo velocity limit is far above the
servo. So a different battery/head does **not** require regeneration. Slower servos do matter
indirectly: the gait period (≈0.4 s, i.e. ~2.5 steps/s with knee swings reaching ~5 rad/s
targets — see Open_Duck_Mini issue #48 where C001 gearbox users measured knees reaching only
31–49 % of commanded range) is baked into the reference and the `imitation_phase` clock. If our
12 V servos are slower than ~5 rad/s, regenerate with a longer `single_support_duration` (and
lower `walk_foot_height`/speeds), then retrain; the runtime's `phase_frequency_factor_offset`
can only nudge the clock, not the joint trajectories. Regenerate also if link lengths / joint
names change (e.g. a new head doesn't matter — head joints are excluded from the imitation
reward — but leg geometry does).

---

## 4. Compute and cost

* JAX GPU wheels: `jax[cuda12]` (needs driver ≥ 525, CUDA ≥ 12.1 bundled via pip, cuDNN ≥ 9.10)
  or `jax[cuda13]` (driver ≥ 580, SM ≥ 7.5); Linux x86_64/aarch64 only. mujoco_playground
  recommends `uv venv --python 3.12`, `uv pip install -U "jax[cuda12]"`, and
  `JAX_DEFAULT_MATMUL_PRECISION=highest` on Ampere/Ada for reproducibility. XLA preallocates
  ~75 % of GPU memory by default; 8192 envs of this model fit easily in 24 GB (issue #19 shows
  only ~1.5 GB actually allocated), so an RTX 4090/L4-class card is sufficient. Avoid Blackwell
  (RTX 50xx) for now because the TensorFlow-based ONNX export has no CUDA kernels for sm_120
  (issues #16/#19) — or run the export on CPU. Training is CPU-light; 8 vCPU is plenty.
* Current hourly prices (checked 2026-10-27/28):
  * RunPod (pricing page, updated 2026-10-08): RTX 4090 $0.34 community / $0.89 secure;
    L4 $0.44 / $0.59; A40 $0.35 / $0.59; RTX A6000 $0.33 / $0.59; A100 80GB PCIe $1.19 / $1.79;
    H100 PCIe $1.99 / $2.89. No A100 40GB.
  * Lambda (on-demand): A100 40GB $1.99, A100 80GB SXM $2.79 (8× only), H100 PCIe $3.29,
    GH200 $2.29, A6000 $1.09, A10 $1.29. No consumer cards.
  * Vast.ai marketplace: RTX 4090 ≈ $0.37–0.56/GPU-h median (computeprices.com, 2026-10-27),
    "from $0.14" for interruptible/low-reliability hosts (Hostinger comparison, Oct 2026).
* One 300 M-step run (estimate 1–3 h on a 4090 incl. ~5–10 min JIT; a few iterations needed):
  RTX 4090 on RunPod community ≈ **$0.35–1.0**, secure ≈ $0.9–2.7; Vast ≈ $0.4–1.7;
  L4 (roughly 2–3× slower) ≈ $1–4; A100 80GB ≈ $1.2–5.4 (RunPod) or A100 40GB ≈ $2–6 (Lambda).
  Budget ~$10–30 for a tuning campaign of 10–20 runs; the cheapest sane choice is an RTX 4090
  (or A40/A6000 at $0.33–0.35) on RunPod community cloud.

---

## 5. Issues / discussions worth knowing (sim2real, backlash, 12 V, boards)

* **12 V 30 kg·cm servos** — Open_Duck_Mini #52: knees swapped to 12 V 30 kg STS3215 stopped
  falls but right foot clearance too low to walk. #21: feet "tremble" with 12 V 30 kg motors
  (BEST_WALK_ONNX_2, `-p 32`, `cutoff_frequency 40`); maintainer (2025-04-19): "12V and 7.4V
  servos differ and need different simulation parameters from system identification...
  BEST_WALK_ONNX2 was trained for 7.4V servos". #33 (V2.5 TODO): evaluate 12 V motors, new BMS,
  retrain policy, move USB->UART, fix neck part, new head. #51: 8.4 V from a full 2S on 7.4 V
  servos question (closed, not planned).
* **Servo speed** — Open_Duck_Mini #48: STS3215-C001 (1:345) maxes ~2.7 rad/s vs the ~5.24
  rad/s the gait wants; measured knee/ankle/hip-pitch reach only 31–49 % of commanded range on
  hardware, sim foot clearance 12–15 mm collapses on the robot. Runtime #7: 5.24 comes from
  BAM identification at 7.4 V (`feetech_sts3215_7_4V/m1.json`).
* **Gains** — Open_Duck_Mini #20: MJCF kp 17.8 == firmware P 32, kd 0.
* **Sim2real** — Playground #5 ("Not work on real robot", feet don't lift) -> pushed to Discord
  (https://discord.gg/UtJZsgfQGe); #4 obs mismatch solved by updating both repos; Open_Duck_Mini
  #43: BEST_WALK_ONNX_2 falls in MuJoCo after a forward command, asks how to init the three
  previous actions (zeros, as in both scripts). #56 "Not moving forward".
* **Backlash** — no issue discusses it; it exists only as the ±0.5° passive joints in
  `open_duck_mini_v2_backlash.xml` plus `backlash_idx_to_add` handling in `joystick.py`.
* **Boards/timing** — Runtime #40 (Pi 5 GPIO + control budget exceeded), Open_Duck_Mini #49
  (CRC/checksum errors + Rust panic on Pi Zero), #42 (Jetson Orin Nano), #34 (LED current).
  Nothing on Radxa.
* **Training infra** — Playground #16/#19 (RTX 50xx TF/CUDA export failure), #15 (cuSolver
  error on RTX A1000, CPU works), #8 (`'dict' object has no attribute 'policy'` in export —
  fixed by b9be205a), #3 (orbax asyncio on py3.10), #25 (`mujoco_playground._src.collision`
  missing: pin the playground version), #14 (custom robot KeyError in PolyReferenceMotion when
  the dy grid is incomplete).
* Community 12 V duck: BAM credits `i1Cps/duck_mini_pro_headless` for the Waveshare ST3025
  12 V identification data — a useful reference project for a 12 V duck.

---

## 6. Implications for our runtime + training

1. **Keep the architecture**: 50 Hz loop, position targets to the servo's internal P loop
   (P = whatever we identify, I = D = 0, acceleration 0), one sync read of pos + vel and one sync
   write per tick; policy obs exactly as §1.3; actions × 0.25 + standing pose. Write it against
   current rustypot (`Sts3215PyController` sync_* calls) or `scservo_sdk`; keep the firmware P
   identical between BAM identification, MJCF export and the robot.
2. **Identify our ST3215-12V with BAM** (pendulum rig, m1 + m6) and either export m1 to
   `kp/damping/frictionloss/armature/forcerange` for the MJX `<position>` actuator, or move to
   mjlab + `BamActuatorCfg` (upstream direction) which also randomizes battery voltage — relevant
   for a 3S pack sagging from 12.6 to ~10 V.
3. **Update the MJCF**: new inertials for trunk (3S pack) and head (camera + ToF), recheck
   `home`/`init_pos`, keep all named sites/sensors/geoms, keep backlash joints
   (re-measure backlash on the 30 kg gear train; ±0.5° may be optimistic).
4. **Reference motion**: reuse `polynomial_coefficients.pkl` unless the 12 V servos are slower
   than ~5 rad/s; then regenerate with a longer `single_support_duration` and retrain.
5. **Add what upstream lacks**: fall detection (accel/gyro or upvector from BNO055 quaternion)
   with torque-off, bus voltage/temperature logging, graceful `turn_off()` on exit, and a
   pre-flight checklist script (offsets, IMU axes, foot switches) — all listed as TODO upstream.
6. **IMU on Radxa**: BNO055 over I2C (clock-stretching issues are a known Pi problem; Radxa
   RK3566 I2C may behave differently — test early) or switch to a gyro+accel-only IMU, since the
   policy only consumes gyro and accelerometer.

Open questions: actual wall-clock per 300 M steps on a single 4090 (no published number);
exact rustypot 0.1.0 API if we want to keep the old HWI; whether the `+1.3` accelerometer bias
should be in training (it is a no-op today); whether the mis-indexed joint noise scales matter;
real no-load speed and backlash of the 12 V ST3215; Blinka support for Radxa Zero 3W.
