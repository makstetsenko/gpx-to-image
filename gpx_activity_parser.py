from pydantic import BaseModel
import datetime
import gpxpy
from geopy.distance import geodesic


class GpxTrackPoint(BaseModel):
    latitude: float
    longitude: float
    elevation: float
    time: datetime.datetime


class GpxActivity(BaseModel):
    distance_km: float
    duration: datetime.timedelta
    avg_speed_kmh: float
    max_speed_kmh: float
    max_elevation_m: float
    min_elevation_m: float
    elevation_gain_m: float

    points: list[GpxTrackPoint] = []


def get_track_points(gpx_file_path: str) -> list[GpxTrackPoint]:

    with open(gpx_file_path, "r") as f:
        gpx = gpxpy.parse(f)

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for p in segment.points:
                points.append(
                    GpxTrackPoint(
                        latitude=p.latitude,
                        longitude=p.longitude,
                        elevation=p.elevation,
                        time=p.time if p.time is not None else datetime.datetime.min,
                    )
                )
    return points


def get_gpx_summary(points: list[GpxTrackPoint]) -> GpxActivity:
    distance_km = 0

    speeds: list[float] = []
    for i in range(1, len(points)):
        distance_diff_km = geodesic(
            (points[i - 1].latitude, points[i - 1].longitude),
            (points[i].latitude, points[i].longitude),
        ).km
        time_hours_diff = (
            points[i].time - points[i - 1].time
        ).total_seconds() / 3600  # hours

        distance_km += distance_diff_km

        speed_kmh = distance_diff_km / time_hours_diff if time_hours_diff > 0 else 0

        speeds.append(speed_kmh)

    avg_speed_kmh = sum(speeds) / len(speeds)
    max_speed_kmh = max(speeds)

    start_time = points[0].time
    end_time = points[-1].time
    duration = end_time - start_time

    max_elevation_m = max(p.elevation for p in points)
    min_elevation_m = min(p.elevation for p in points)
    elevation_gain_m = max_elevation_m - min_elevation_m

    return GpxActivity(
        distance_km=distance_km,
        duration=duration,
        avg_speed_kmh=avg_speed_kmh,
        max_speed_kmh=max_speed_kmh,
        elevation_gain_m=elevation_gain_m,
        max_elevation_m=max_elevation_m,
        min_elevation_m=min_elevation_m,
        points=points,
    )


def get_gpx_summary_from_file(gpx_file_path: str) -> GpxActivity:
    points = get_track_points(gpx_file_path)
    return get_gpx_summary(points)
