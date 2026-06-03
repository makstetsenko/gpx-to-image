import pathlib
import cairosvg
from PIL import Image
from io import BytesIO

from data_layers_generation import get_activity_name_layer_svg, get_avg_speed_layer_svg, get_distance_layer_svg, get_elevation_gain_layer_svg, get_track_path_layer_svg
from data_layers_generation.label_generator import TextAlignment
from gpx_activity_parser import GpxActivity

    
def compose_layout(dir_path: pathlib.Path, gpx_activity: GpxActivity, title: str) -> str:
    output_path = dir_path.joinpath("layout_1.png").resolve()


    title_layer_svg_path = get_activity_name_layer_svg(title, dir_path, label_alignment=TextAlignment.MIDDLE, image_size=(2000, 300))
    distance_layer_svg_path = get_distance_layer_svg(gpx_activity, dir_path, label_alignment=TextAlignment.MIDDLE, image_size=(2000, 300))
    avg_speed_layer_svg_path = get_avg_speed_layer_svg(gpx_activity, dir_path, label_alignment=TextAlignment.MIDDLE, image_size=(2000, 300))
    elevation_gain_layer_svg_path = get_elevation_gain_layer_svg(gpx_activity, dir_path, label_alignment=TextAlignment.MIDDLE, image_size=(2000, 300))
    track_path_layer_svg_path = get_track_path_layer_svg(gpx_activity, dir_path, image_size=(2000, 2000))
    
    def _svg_to_png_image(svg_path: str, height: int) -> Image.Image:
        png_data = cairosvg.svg2png(url=svg_path, output_height=height)
        if png_data is None:
            raise ValueError(f"Failed to convert SVG to PNG: {svg_path}")
        return Image.open(BytesIO(png_data))

    title_layer_png = _svg_to_png_image(title_layer_svg_path, height=200)
    distance_layer_png = _svg_to_png_image(distance_layer_svg_path, height=200)
    avg_speed_layer_png = _svg_to_png_image(avg_speed_layer_svg_path, height=200)
    elevation_gain_layer_png = _svg_to_png_image(elevation_gain_layer_svg_path, height=200)
    track_path_layer_png = _svg_to_png_image(track_path_layer_svg_path, height=1200)
    
    layers = [title_layer_png, distance_layer_png, avg_speed_layer_png, elevation_gain_layer_png, track_path_layer_png]
    
    max_width = max(
        title_layer_png.width,
        distance_layer_png.width,
        avg_speed_layer_png.width,
        elevation_gain_layer_png.width,
        track_path_layer_png.width,
    )

    image = Image.new("RGBA", (max_width, 2200), (0, 0, 0, 0))
    
    Y_PADDING = 50
    
    for index, layer in enumerate(layers):
        x_offset = (max_width - layer.width) // 2
        y_offset = 100
        
        if index > 0:
            previous_layers_height_sum = sum(l.height for l in layers[:index])
            y_offset += previous_layers_height_sum + index * Y_PADDING
        
        image.paste(layer, (x_offset, y_offset), layer)
    
    
    image.save(output_path)
    
    return output_path.as_posix()
    
    