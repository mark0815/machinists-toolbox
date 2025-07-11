from milling.models import JobTemplate, ToolAssignment
from tool_library.models import Tool
import typing as t
def generate_job_template_json(job_template:JobTemplate) -> dict:
    return {
        "Fixtures": [
            {
                "G54": True
            }
        ],
        "Desc": job_template.description,
        "OrderOutputBy": "Fixture",
        "Post": "linuxcnc",
        "PostArgs": "",
        "SetupSheet": {
            "CoolantMode": _freecad_job_coolant_mode(job_template=job_template),
            "HorizRapid": f"{job_template.machine.max_vf} mm/min",
            "VertRapid": f"{job_template.machine.max_vf} mm/min"
        },
        "SplitOutput": False,
        "Tolerance": "0.01",
        "ToolController": [
            {
                "version": 1,
                "nr": tool.tool_pocket,
                "name": str(tool.recipe),
                "label": tool.label if tool.label else str(tool.recipe),
                "dir": _freecad_tool_direction(tool.recipe.cutting_data.tool),
                "speed": tool.recipe.cutting_data_effective[0],
                "hfeed": f"{tool.recipe.cutting_data_effective[1]} mm/min",
                "vfeed": f"{tool.recipe.cutting_data_effective[1]} mm/min",
                "hrapid": f"{job_template.machine.max_vf} mm/min",
                "vrapid": f"{job_template.machine.max_vf} mm/min",
                "tool": {
                    "version": 2,
                    "attribute": {},
                    "name": f"{tool.recipe.cutting_data.tool}",
                    "parameter": {
                        "Chipload": "0,02 mm",
                        "CuttingEdgeHeight": f"{tool.recipe.cutting_data.tool.flute_length} mm",
                        "Diameter": f"{tool.recipe.cutting_data.tool.diameter} mm",
                        "Flutes": tool.recipe.cutting_data.tool.flute_count,
                        "Length": f"{tool.recipe.cutting_data.tool.overall_length} mm",
                        "Material": _freecad_tool_material(tool.recipe.cutting_data.tool),
                        "ShankDiameter": f"{tool.recipe.cutting_data.tool.diameter} mm",
                        "SpindleDirection":_freecad_tool_direction(tool.recipe.cutting_data.tool)
                        #"TipAngle": "119,00 \u00b0", Chamfer/Drill
                        # "TipDiameter": "0.1 mm" # Chamfer
                    },
                    "shape":_freecad_tool_shape(tool.recipe.cutting_data.tool),
                    "shape-type":_freecad_tool_shape(tool.recipe.cutting_data.tool),
                },
                "xengine": [
                    {
                        "expr": "${SetupSheet}.HorizRapid",
                        "prop": "HorizRapid"
                    },
                    {
                        "expr": "${SetupSheet}.VertRapid",
                        "prop": "VertRapid"
                    }
                ]
            } for tool in job_template.tools.order_by("tool_pocket")
        ],
        "Version": 1
    }

def _freecad_tool_material(tool: Tool) -> t.Optional[str]:
    match Tool.Material(tool.material):
        case Tool.Material.HSS:
            return "HSS"
        case Tool.Material.CARBIDE:
            return "Carbide"

def _freecad_job_coolant_mode(job_template:JobTemplate) -> t.Optional[str]:
    match job_template.CoolandMode(job_template.coolant_mode):
        case job_template.CoolandMode.MIST:
            return "Mist"
        case job_template.CoolandMode.FLOOD:
            return "Flood"

def _freecad_tool_shape(tool: Tool) -> t.Optional[str]:
    match Tool.ToolType(tool.type):
         case Tool.ToolType.ENDMILL:
            return "endmill.fcstd"
         case Tool.ToolType.CHAMFER:
            return "chamfer.fcstd"

def _freecad_tool_shape_type(tool: Tool) -> t.Optional[str]:
    match Tool.ToolType(tool.type):
        case Tool.ToolType.ENDMILL:
            return "Endmill"
        case Tool.ToolType.CHAMFER:
            return "Chamfer"

@staticmethod
def _freecad_tool_direction(tool: Tool) -> t.Optional[str]:
    match Tool.CuttingDirection(tool.direction):
        case Tool.CuttingDirection.CW:
            return "Forward"
        case Tool.CuttingDirection.CCW:
            return "Reverse"
