from gpx_activity_parser import GpxActivity
import data_layers_generation.label_generator as label_generator
import data_layers_generation.track_path_generator as track_path_generator
import pathlib
import datetime

def get_activity_name_layer_svg(
    activity_name: str,
    dir_path: pathlib.Path,
    label_alignment: label_generator.TextAlignment = label_generator.TextAlignment.LEFT,
    image_size: tuple[int, int] = (3000, 500)
) -> str:
    return label_generator.generate_svg(
        request=label_generator.LabelRequest(
            output_path=dir_path.joinpath("activity_name_layer.svg"),
            label_text=activity_name.upper(),
            font_size=120,
            sub_label_text=None,
            sub_font_size=60,
            label_alignment=label_alignment,
            image_size=image_size,
        )
    )

def get_distance_layer_svg(
    gpx_activity: GpxActivity,
    dir_path: pathlib.Path,
    label_alignment: label_generator.TextAlignment = label_generator.TextAlignment.LEFT,
    image_size: tuple[int, int] = (3000, 500)
) -> str:
    return label_generator.generate_svg(
        request=label_generator.LabelRequest(
            output_path=dir_path.joinpath("distance_layer.svg"),
            label_text=f"{gpx_activity.distance_km:.2f} km",
            font_size=80,
            sub_label_text="Distance",
            sub_font_size=40,
            label_alignment=label_alignment,
            image_size=image_size,
        )
    )


def get_avg_speed_layer_svg(
    gpx_activity: GpxActivity,
    dir_path: pathlib.Path,
    label_alignment: label_generator.TextAlignment = label_generator.TextAlignment.LEFT,
    image_size: tuple[int, int] = (3000, 500)
) -> str:
    return label_generator.generate_svg(
        request=label_generator.LabelRequest(
            output_path=dir_path.joinpath("avg_speed_layer.svg"),
            label_text=f"{gpx_activity.avg_speed_kmh:.2f} km/h",
            font_size=80,
            sub_label_text="Average Speed",
            sub_font_size=40,
            label_alignment=label_alignment,
            image_size=image_size,
        )
    )


def get_max_speed_layer_svg(
    gpx_activity: GpxActivity,
    dir_path: pathlib.Path,
    label_alignment: label_generator.TextAlignment = label_generator.TextAlignment.LEFT,
    image_size: tuple[int, int] = (3000, 500)
) -> str:
    return label_generator.generate_svg(
        request=label_generator.LabelRequest(
            output_path=dir_path.joinpath("max_speed_layer.svg"),
            label_text=f"{gpx_activity.max_speed_kmh:.2f} km/h",
            font_size=80,
            sub_label_text="Maximum Speed",
            sub_font_size=40,
            label_alignment=label_alignment,
            image_size=image_size,
        )
    )


def get_max_elevation_layer_svg(
    gpx_activity: GpxActivity,
    dir_path: pathlib.Path,
    label_alignment: label_generator.TextAlignment = label_generator.TextAlignment.LEFT,
    image_size: tuple[int, int] = (3000, 500)
) -> str:
    return label_generator.generate_svg(
        request=label_generator.LabelRequest(
            output_path=dir_path.joinpath("max_elevation_layer.svg"),
            label_text=f"{gpx_activity.max_elevation_m:.2f} m",
            font_size=80,
            sub_label_text="Maximum Elevation",
            sub_font_size=40,
            label_alignment=label_alignment,
            image_size=image_size,
        )
    )


def get_min_elevation_layer_svg(
    gpx_activity: GpxActivity,
    dir_path: pathlib.Path,
    label_alignment: label_generator.TextAlignment = label_generator.TextAlignment.LEFT,
    image_size: tuple[int, int] = (3000, 500)
) -> str:
    return label_generator.generate_svg(
        request=label_generator.LabelRequest(
            output_path=dir_path.joinpath("min_elevation_layer.svg"),
            label_text=f"{gpx_activity.min_elevation_m:.2f} m",
            font_size=80,
            sub_label_text="Minimum Elevation",
            sub_font_size=40,
            label_alignment=label_alignment,
            image_size=image_size,
        )
    )


def get_elevation_gain_layer_svg(
    gpx_activity: GpxActivity,
    dir_path: pathlib.Path,
    label_alignment: label_generator.TextAlignment = label_generator.TextAlignment.LEFT,
    image_size: tuple[int, int] = (3000, 500)
) -> str:
    return label_generator.generate_svg(
        request=label_generator.LabelRequest(
            output_path=dir_path.joinpath("elevation_gain_layer.svg"),
            label_text=f"{gpx_activity.elevation_gain_m:.2f} m",
            font_size=80,
            sub_label_text="Elevation Gain",
            sub_font_size=40,
            label_alignment=label_alignment,
            image_size=image_size,
        )
    )


def get_duration_layer_svg(
    gpx_activity: GpxActivity,
    dir_path: pathlib.Path,
    label_alignment: label_generator.TextAlignment = label_generator.TextAlignment.LEFT,
    image_size: tuple[int, int] = (3000, 500)
) -> str:

    def get_duration_str(duration: datetime.timedelta) -> str:
        hours = duration.total_seconds() // 3600
        minutes = (duration.total_seconds() % 3600) // 60
        second = duration.total_seconds() % 60

        if hours == 0 and minutes == 0:
            return f"{second:02.0f}s"

        if hours == 0:
            return f"{minutes:02.0f}m {second:02.0f}s"

        return f"{hours:02.0f}h {minutes:02.0f}m {second:02.0f}s"

    return label_generator.generate_svg(
        request=label_generator.LabelRequest(
            output_path=dir_path.joinpath("duration_layer.svg"),
            label_text=get_duration_str(gpx_activity.duration),
            font_size=80,
            sub_label_text="Duration",
            sub_font_size=40,
            label_alignment=label_alignment,
            image_size=image_size,
        )
    )


def get_track_path_layer_svg(gpx_activity: GpxActivity, dir_path: pathlib.Path, image_size: tuple[int, int] = (2000, 2000)) -> str:
    return track_path_generator.generate_svg(
        request=track_path_generator.TrackPathImageRequest(
            track_points=gpx_activity.points,
            output_path=dir_path.joinpath("track_path_layer.svg"),
            track_color="#FC4C02",
            track_width=24,
            image_size=image_size,
        )
    )
