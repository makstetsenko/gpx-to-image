from gpx_track_parser import GpxSummary, TrackPoint
import math
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel
from simplification.cutil import simplify_coords


class ImageRequest(BaseModel):
    summary: GpxSummary
    output_path: str
    title: str = "EVENING DRIVE"
    title_font_path: str = "Arial Rounded Bold.ttf"
    title_font_size: int = 100
    stat_font_path: str = "Arial Rounded Bold.ttf"
    stat_font_size: int = 60

def mercator(lat, lon):
    x = lon
    y = math.log(
        math.tan(math.pi / 4 + math.radians(lat) / 2)
    )
    return x, y

def get_bounds(points: list[TrackPoint]):
    min_lat = min(p.latitude for p in points)
    max_lat = max(p.latitude for p in points)
    min_lon = min(p.longitude for p in points)
    max_lon = max(p.longitude for p in points)
    return min_lat, max_lat, min_lon, max_lon


def get_route_pixels(points: list[TrackPoint], img_width: int, img_height: int):
    min_lat, max_lat, min_lon, max_lon = get_bounds(points)
    
    route_width = max_lon - min_lon
    route_height = max_lat - min_lat

    scale = min(
        img_width / route_width,
        img_height / route_height
    ) * 0.8  # 80% of the image size to add some padding
    
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2

    route_pixels = []
    for point in points:
        px = img_width / 2 + (point.longitude - center_lon) * scale
        py = img_height / 4 - (point.latitude - center_lat) * scale
        route_pixels.append((px, py))
    
    
    smooth_points = simplify_coords(
        route_pixels,
        epsilon=1
    )
    return smooth_points

def generate_image(request: ImageRequest):
    # Create a blank white image
    img_width, img_height = 1440, 2560
    
    line_color = (252, 76, 2)  # Strava orange
   
    img_background_color = (0,0,0,0)  # Transparent background
    img = Image.new("RGBA", (img_width, img_height), img_background_color)
    draw = ImageDraw.Draw(img)
    
    # Add route path
    route_pixels = get_route_pixels(request.summary.points, img_width, img_height)
    draw.line(route_pixels, fill=line_color, width=12, joint="curve")
    
    # Add text info
    title_font = ImageFont.truetype(
        request.title_font_path,
        request.title_font_size
    )

    stat_font = ImageFont.truetype(
        request.stat_font_path,
        request.stat_font_size
    )


    draw.text(
        (90, 1300),
        request.title.upper(),
        fill="white",
        font=title_font
    )

    draw.text(
        (90, 1600),
        f"{request.summary.distance_km:.2f}" + " km",
        fill="white",
        font=stat_font
    )

    draw.text(
        (90, 1750),
        request.summary.get_duration_str(),
        fill="white",
        font=stat_font
    )

    draw.text(
        (90, 1900),
        f"{request.summary.avg_speed_kmh:.2f} km/h",
        fill="white",
        font=stat_font
    )
    
    img.save(request.output_path)