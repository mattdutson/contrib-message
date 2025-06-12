#!/usr/bin/env python3

import argparse
import datetime
import pathlib
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "message_segments",
        nargs="+",
        help="components of the message, one per year",
    )
    parser.add_argument(
        "-b",
        "--background-level",
        default=10,
        type=int,
        help="the number of commits per day to use for background",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="show the message grid without making any commits",
    )
    parser.add_argument(
        "-f",
        "--foreground-level",
        default=100,
        type=int,
        help="the number of commits per day to use for foreground text",
    )
    parser.add_argument(
        "-o",
        "--offset",
        default=2,
        type=int,
        help="horizontal to use when rendering text",
    )
    parser.add_argument(
        "-m",
        "--max-push",
        default=50,
        type=int,
        help="the maximum number of commits to push at once",
    )
    args = parser.parse_args()

    # Start at the current year, and go back one year for each segment of the message.
    for i, segment in enumerate(args.message_segments):
        year = datetime.datetime.now().year - i
        is_last_segment = i == (len(args.message_segments) - 1)
        start_date = datetime.datetime(year=year, month=1, day=1)

        # Start on a Sunday so the grid is aligned.
        offset_days = 6 - start_date.weekday()
        start_date += datetime.timedelta(days=offset_days)

        # The number of complete 7-day weeks (number of columns in the grid)
        weeks = (365 - offset_days) // 7

        # Create a binary NumPy array with rendered text.
        image = Image.new("RGB", (weeks, 7))
        draw = ImageDraw.Draw(image)
        draw.fontmode = "1"  # Disable antialiasing.
        font_path = pathlib.Path(__file__).parent / "bpdots_unicase_square_bold.otf"
        draw.text(
            (args.offset, -4),  # -4 gives vertical centering.
            segment.upper(),
            font=ImageFont.truetype(font_path),
        )
        pixels = np.array(image)[..., 0].astype(np.bool)

        # Show a preview.
        print("\u2581" * (weeks + 2))
        for row in pixels:
            print("\u258F", end="")
            for value in row:
                print("\u2588" if value else " ", end="")
            print("\u2595")
        print("\u2594" * (weeks + 2))

        # Don't create commits if this is a dry run.
        if args.dry_run:
            continue

        # Create and push dummy commits.
        unpushed_commits = 0
        for w in range(weeks):
            for d in range(7):
                date = start_date + datetime.timedelta(days=(7 * w) + d)
                level = args.foreground_level if pixels[d, w] else args.background_level
                for j in range(level):
                    subprocess.run(
                        [
                            "git",
                            "commit",
                            "-m",
                            "Message",
                            "--allow-empty",
                            "--date",
                            str(date),
                        ],
                        check=True,
                    )
                    unpushed_commits += 1
                    if unpushed_commits >= args.max_push:
                        subprocess.run(["git", "push"], check=True)
                        unpushed_commits = 0
        subprocess.run(["git", "push"], check=True)
        unpushed_commits = 0


if __name__ == "__main__":
    main()
