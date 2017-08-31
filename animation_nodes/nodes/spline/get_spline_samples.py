import bpy
from ... base_types import AnimationNode
from . spline_evaluation_base import SplineEvaluationBase

class GetSplineSamplesNode(bpy.types.Node, AnimationNode, SplineEvaluationBase):
    bl_idname = "an_GetSplineSamplesNode"
    bl_label = "Get Spline Samples"

    def create(self):
        self.newInput("Spline", "Spline", "spline", defaultDrawType = "PROPERTY_ONLY")
        self.newInput("Integer", "Amount", "amount", value = 50)
        self.newInput("Float", "Start", "start", value = 0.0).setRange(0.0, 1.0)
        self.newInput("Float", "End", "end", value = 1.0).setRange(0.0, 1.0)
        self.newOutput("Vector List", "Positions", "positions")
        self.newOutput("Vector List", "Tangents", "tangents")

    def draw(self, layout):
        layout.prop(self, "parameterType", text = "")

    def drawAdvanced(self, layout):
        col = layout.column()
        col.active = self.parameterType == "UNIFORM"
        col.prop(self, "resolution")

    def getExecutionCode(self, required):
        if len(required) == 0:
            return

        yield "if spline.isEvaluable():"
        yield "    amount = max(amount, 0.0)"
        yield "    _start = min(max(start, 0), 1)"
        yield "    _end = min(max(end, 0), 1)"

        if self.parameterType == "UNIFORM":
            yield "    spline.ensureUniformConverter(self.resolution)"
        if "positions" in required:
            yield "    positions = spline.getDistributedPoints(amount, _start, _end, self.parameterType)"
        if "tangents" in required:
            yield "    tangents = spline.getDistributedTangents(amount, _start, _end, self.parameterType)"

        yield "else:"
        yield "    positions = Vector3DList()"
        yield "    tangents = Vector3DList()"
