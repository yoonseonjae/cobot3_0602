# cobot_ws — 스마트팩토리 야간 순찰 로봇
**Isaac Sim 5.1 / ROS2 Humble / Nova Carter + UR10**

시나리오: 야간 무인 순찰 → 배관 과열 감지 → 밸브 차단 → 관제 센터 보고

---

## 개발 환경

- OS: Ubuntu 22.04 LTS
- Isaac Sim: 5.1.0 (alias: `isaacsim`)
- ROS2: Humble
- Python: 3.11 (Isaac Sim 번들)

---

## 워크스페이스 구조

\`\`\`
~/cobot_ws/
├── usd/
│   ├── factory_map.usd        # 공장 맵 (Z-up, 미터 단위)
│   └── industrial_vendor.usdz # 원본 맵 파일
├── isaacsim_scripts/
│   ├── test_connection.py     # VS Code ↔ Isaac Sim 연결 테스트
│   └── utils/
├── maps/                      # 2D Nav 맵 (pgm + yaml) — 미완
├── config/                    # Nav2 파라미터 — 미완
└── src/                       # ROS2 패키지 — 미완
\`\`\`

---

## Session 1 — 완료

- [x] cobot_ws 워크스페이스 생성
- [x] Isaac Sim 5.1 + VS Code Extension 연결
- [x] factory_map.usd 로드, 단위 미터 변환, Z-up 변환, 저장
- [x] Stage 구조: /World/nova_carter + /scene (공장 메시)

---

## Session 2 — 완료 (TF 제외)

- [x] 맵 바운딩박스: 54.32m x 51.23m x 5.33m
- [x] Nova Carter 바닥 배치 (Z = -3.3472)
- [x] Physics Ground Plane (Z = -3.3472)
- [x] ROS2 OmniGraph 생성 및 저장
  - /World/ROS2Clock — /clock 토픽
  - /World/ROS2TFOdom — /tf + /odom 토픽
  - /World/ROS2LiDAR — /scan 토픽 (RPLidar S2E, 22Hz LaserScan)
  - /World/ROS2CmdVel — /cmd_vel → Carter 구동
- [x] Carter cmd_vel 구동 확인
- [x] 휠 반지름: 0.1912m, 휠 간격: 0.6201m
- [ ] /tf 미발행 문제 — 다음 세션 시작점

---

## 알려진 이슈

| 증상 | 원인 | 상태 |
|------|------|------|
| /tf 토픽 비어있음 | ROS2TFOdom 그래프가 odom→base_link 발행 안 함 | 해결 필요 |
| Stop→Play 시 render product 초기화 | Play 후에 render product 재설정 필요 | 우회법 있음 |
| 저장 후 타이틀바 * 안 사라짐 | Isaac Sim 5.1 UI 버그 | 무시 |

---

## Session 3 — 다음 시작점 (여기서 시작)

### Step 1 — Isaac Sim 실행 및 맵 열기
\`\`\`bash
isaacsim
# File → Open → ~/cobot_ws/usd/factory_map.usd
\`\`\`

### Step 2 — Play 후 Script Editor에서 실행
\`\`\`python
import omni.replicator.core as rep
import omni.graph.core as og
lidar_path = "/World/nova_carter/chassis_link/sensors/rear_RPLidar/RPLidar_S2E"
render_product = rep.create.render_product(lidar_path, [1, 1])
node = og.get_graph_by_path("/World/ROS2LiDAR").get_node("/World/ROS2LiDAR/LidarHelper")
node.get_attribute("inputs:renderProductPath").set(render_product.path)
print(f"Done: {render_product.path}")
\`\`\`

### Step 3 — /tf 문제 해결 후 slam_toolbox 실행
\`\`\`bash
source /opt/ros/humble/setup.bash && ros2 launch slam_toolbox online_async_launch.py use_sim_time:=false scan_topic:=/scan
\`\`\`

---

## 주요 Prim 경로

\`\`\`
공장 맵 메시    : /scene
Carter 루트     : /World/nova_carter
Carter 베이스   : /World/nova_carter/chassis_link
RPLidar S2E    : /World/nova_carter/chassis_link/sensors/rear_RPLidar/RPLidar_S2E
전방 카메라    : /World/nova_carter/chassis_link/sensors/front_owl/camera
Ground Plane   : /World/GroundPlane (Z = -3.3472)
\`\`\`

## 주요 수치

\`\`\`
바닥 Z          : -3.3472
Carter 시작위치 : X=0, Y=0, Z=-3.3472
휠 반지름       : 0.1912m
휠 간격         : 0.6201m
ROS Domain ID   : 0
\`\`\`
