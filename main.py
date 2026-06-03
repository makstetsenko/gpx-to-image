import gpx_activity_parser
import sys
import pathlib
import data_layers_generation
import layout_composing.layout_1 as layout_1

if len(sys.argv) > 1:
    file_path = pathlib.Path(sys.argv[1]).resolve()
else:
    raise ValueError(
        "Please provide the path to the GPX file as a command-line argument."
    )

if not file_path.is_file():
    raise ValueError(f"The provided path does not exist or is not a file: {file_path}")

if file_path.suffix.lower() != ".gpx":
    raise ValueError(f"The provided file is not a GPX file: {file_path}")

if len(sys.argv) > 2:
    title = sys.argv[2]
else:
    raise ValueError(
        "Please provide a title for the image as a second command-line argument."
    )

summary = gpx_activity_parser.get_gpx_summary_from_file(file_path.as_posix())

output_dir_path = file_path.parent.joinpath(file_path.stem).resolve()

if not output_dir_path.exists():
    output_dir_path.mkdir(parents=True)


layout_path = layout_1.compose_layout(output_dir_path, summary, title)

print(f"Generated image saved to: {layout_path}")
