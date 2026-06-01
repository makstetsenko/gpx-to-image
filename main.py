import gpx_track_parser
import image_generator
import sys
import pathlib

if len(sys.argv) > 1:
    file_path = pathlib.Path(sys.argv[1]).resolve()
else:
    raise ValueError("Please provide the path to the GPX file as a command-line argument.")

if not file_path.is_file():
    raise ValueError(f"The provided path does not exist or is not a file: {file_path}")

if file_path.suffix.lower() != ".gpx":
    raise ValueError(f"The provided file is not a GPX file: {file_path}")

if len(sys.argv) > 2:
    title = sys.argv[2]
else:
    raise ValueError("Please provide a title for the image as a second command-line argument.")

summary = gpx_track_parser.get_gpx_summary_from_file(file_path.as_posix())

output_image_path = file_path.with_suffix(".png")
image_generator.generate_image(image_generator.ImageRequest(
    summary=summary,
    output_path=output_image_path.as_posix(),
    title=title
))
print(f"Generated image saved to: {output_image_path}")