import omni.usd
import omni

stage = omni.usd.get_context().get_stage()

xform = omni.usd.commands.CreatePrimWithDefaultXformCommand(
    prim_type="Xform",
    prim_path="/World/cobot_test"
)
xform.do()

print("✅ cobot_ws 연결 성공 — /World/cobot_test 생성됨")
