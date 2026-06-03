from gpx_activity_parser import GpxTrackPoint
from pydantic import BaseModel

import svgwrite
import pathlib


class TrackPathImageRequest(BaseModel):
    track_points: list[GpxTrackPoint]
    output_path: pathlib.Path
    track_color: str = "#FC4C02"
    track_width: int = 8
    image_size: tuple[int, int] = (2000, 2000)


def get_bounds(points: list[GpxTrackPoint]):
    min_lat = min(p.latitude for p in points)
    max_lat = max(p.latitude for p in points)
    min_lon = min(p.longitude for p in points)
    max_lon = max(p.longitude for p in points)
    return min_lat, max_lat, min_lon, max_lon


def get_route_pixels(points: list[GpxTrackPoint], img_width: int, img_height: int):
    min_lat, max_lat, min_lon, max_lon = get_bounds(points)

    route_width = max_lon - min_lon
    route_height = max_lat - min_lat

    scale = min(img_width / route_width, img_height / route_height) * 0.95

    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2

    route_pixels: list[tuple[float, float]] = []
    for point in points:

        px = img_width / 2 + (point.longitude - center_lon) * scale
        py = img_height / 2 - (point.latitude - center_lat) * scale

        route_pixels.append((px, py))

    # smooth_points = simplify_coords(route_pixels, epsilon=1)
    return route_pixels


def generate_svg(request: TrackPathImageRequest) -> str:
    img_size = request.image_size

    dwg = svgwrite.Drawing(
        request.output_path.as_posix(), size=(f"{img_size[0]}px", f"{img_size[1]}px")
    )

    route_pixels = get_route_pixels(request.track_points, img_size[0], img_size[1])

    dwg.add(
        dwg.polyline(
            route_pixels,
            stroke=request.track_color,
            stroke_width=request.track_width,
            fill="none",
            stroke_linecap="round",
            stroke_linejoin="round",
        )
    )

    dwg.save()

    return request.output_path.as_posix()
