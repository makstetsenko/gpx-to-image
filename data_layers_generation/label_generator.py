from pydantic import BaseModel
import svgwrite
import pathlib
from enum import Enum


class TextAlignment(Enum):
    LEFT = "left"
    MIDDLE = "center"
    RIGHT = "right"


class LabelRequest(BaseModel):
    output_path: pathlib.Path
    label_text: str
    sub_label_text: str | None = None
    font_family: str = "Arial"
    font_size: int = 100
    sub_font_size: int = 30
    image_size: tuple[int, int] = (700, 250)
    label_color: str = "#E3E3E3"
    label_alignment: TextAlignment = TextAlignment.LEFT


def generate_svg(request: LabelRequest):
    dwg = svgwrite.Drawing(
        request.output_path.as_posix(),
        size=(f"{request.image_size[0]}px", f"{request.image_size[1]}px"),
    )

    if request.label_alignment == TextAlignment.LEFT:
        text_anchor = "start"
        x_position = "0%"
    elif request.label_alignment == TextAlignment.MIDDLE:
        text_anchor = "middle"
        x_position = "50%"
    else:  # TextAlignment.RIGHT
        text_anchor = "end"
        x_position = "100%"

    if request.sub_label_text:
        dwg.add(
            dwg.text(
                request.sub_label_text,
                insert=(x_position, request.sub_font_size),
                fill=request.label_color,
                font_size=request.sub_font_size,
                font_family=request.font_family,
                text_anchor=text_anchor,
            )
        )

    dwg.add(
        dwg.text(
            request.label_text,
            insert=(
                x_position,
                request.font_size
                + (request.sub_font_size if request.sub_label_text else 0),
            ),
            fill=request.label_color,
            font_size=request.font_size,
            font_family=request.font_family,
            text_anchor=text_anchor,
        )
    )

    dwg.save()

    return request.output_path.as_posix()
