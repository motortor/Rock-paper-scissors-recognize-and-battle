# Rock-paper-scissors-recognize-and-battle
石头剪刀布的手势识别和对决（Rock paper scissors recognize and battle）

 """
    Classify hand gesture as Rock, Paper, or Scissors based on finger states.
    landmarks: A list of (x,y,z) for each of the 21 hand landmarks in normalized coordinates.

    We will define which fingers are "extended" by comparing the tip and DIP joint positions:
    For each finger, the tip's y-coordinate should be less than (i.e., above) the PIP (or DIP) joint's y-coordinate if the finger is extended in a typical front-facing posture.
    Index finger: Tip (8), PIP(6)
    Middle finger: Tip(12), PIP(10)
    Ring finger: Tip(16), PIP(14)
    Pinky finger: Tip(20), PIP(18)
    Thumb: We'll check if thumb tip (4) is to the left of the IP joint (2) for simplicity (assuming a right hand, palm facing camera). Adjust logic as needed.

    NOTE: This is a heuristic approach that may need adjustments depending on camera orientation and hand position.
    """

    # Extract relevant landmark indices
    # Landmarks:
    #   Thumb: Tip (4), IP(3), MCP(2)
    #   Index: Tip (8), PIP(6)
    #   Middle: Tip (12), PIP(10)
    #   Ring: Tip (16), PIP(14)
    #   Pinky: Tip (20), PIP(18)

    # Normalize assumption: camera oriented so that a lower y-value means finger pointing up (somewhat)
    # We'll say a finger is "extended" if tip.y < PIP.y (for index/middle/ring/pinky).
    # For thumb, we'll consider x-coordinates since thumb extends sideways:
    #   If thumb tip (4) is to the left of thumb MCP (2) (for a right-hand palm facing camera),
    #   then it's considered extended. You might need to flip logic depending on which hand and orientation.

    """
根据手指状态将手势分类为石头、剪刀或布。
landmarks: 一个包含 21 个手部关键点的列表，每个关键点表示为 (x, y, z) 的归一化坐标。

我们将通过比较手指指尖和 DIP 关节的位置来定义哪些手指是“伸展”的：
对于每根手指，如果指尖的 y 坐标小于（即高于）PIP（或 DIP）关节的 y 坐标，并且手掌面向正前方，则认为该手指是伸展的。
- 食指: 指尖 (8), PIP(6)
- 中指: 指尖 (12), PIP(10)
- 无名指: 指尖 (16), PIP(14)
- 小指: 指尖 (20), PIP(18)
- 拇指: 为简化逻辑（假设是右手且手掌面向相机），我们检查拇指指尖 (4) 是否位于 IP 关节 (2) 的左侧。可以根据需要调整逻辑。

注意: 这是一种启发式方法，可能需要根据相机方向和手部姿势进行调整。
"""

# 提取相关的关键点索引
# 关键点说明:
# - 拇指: 指尖 (4), IP(3), MCP(2)
# - 食指: 指尖 (8), PIP(6)
# - 中指: 指尖 (12), PIP(10)
# - 无名指: 指尖 (16), PIP(14)
# - 小指: 指尖 (20), PIP(18)

# 归一化的假设: 相机方向设定为 y 坐标越低表示手指向上伸展（大致方向）。
# 定义手指“伸展”的条件:
# - 对于食指/中指/无名指/小指，如果指尖的 y 坐标 < PIP 的 y 坐标，则认为该手指是“伸展”的。
# - 对于拇指，我们考虑 x 坐标: 
#   如果拇指指尖 (4) 在 MCP (2) 的左侧（假设右手手掌面向相机），则认为拇指是伸展的。
#   需要根据使用哪只手和方向翻转逻辑。
