# ========================================================================
# ------------------------ Copyright 2023 Mabrains -----------------------
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ========================================================================
"""
Usage:
  install_tech.py (--tech_name=<tech_name>) (--tech_path=<tech_path>)

  -h, --help                   Show help text.
  -v, --version                Show version.
  --tech_name=<tech_name>      Name of technology to be installed
  --tech_path=<tech_path>      Path of technology to be installed
"""


from pathlib import Path
from docopt import docopt
import logging
import os

def remove_path_or_dir(dest: Path):
    if dest.is_dir():
        os.unlink(dest)
    else:
        os.remove(dest)


def make_link(src, dest, overwrite: bool = True) -> None:
    """
    Function to create a symlink of source to destination path.

    Parameters
    ----------
    src : str
        Path to source we need to create a link from it
    dest : str
        Path to destiantion we need to add a link to it
    overwrite: bool
        Option for overwriting the current link.
    Returns
    -------
        None
    """

    src_path = Path(src)
    dest_path = Path(dest)

    if not src_path.exists():
        raise ValueError(f"{src} does not exist")

    if dest_path.exists() and not overwrite:
        logging.info(f"{dest} dir already exists")
        return

    if dest_path.exists() or dest_path.is_symlink():
        logging.info(f"Removing {dest_path} already installed")
        remove_path_or_dir(dest_path)

    try:
        os.symlink(src_path, dest_path, target_is_directory=True)
    except OSError as err:
        logging.info("Could not create symlink!")
        logging.error("Error: ", err)

    logging.info("Symlink made:")
    logging.info(f"From: {src_path}")
    logging.info(f"To:   {dest_path}")


def main(tech_name, tech_path):
    """
    Main function for PDK installation
    """

    # Home directory
    home = Path.home()

    # Destination of PDK you need to link to it
    dest_dir = os.path.join(home, ".klayout", "tech")
    dest_path = Path(dest_dir)
    dest_path.mkdir(exist_ok=True, parents=True)

    # Creating symlink to klayout tech
    dest_tech = os.path.join(dest_dir, tech_name)
    src_tech = os.path.expanduser(tech_path)
    
    # Check paths
    if not os.path.exists(dest_tech) and os.path.isdir(dest_tech):
        logging.error(f"Destination path {dest_tech} doesn't exist, please recheck")
        exit(1)

    if not os.path.exists(src_tech) and os.path.isdir(src_tech):
        logging.error(f"Tech path {src_tech} doesn't exist, please recheck")
        exit(1)

    make_link(src=src_tech, dest=dest_tech)

# ================================================================
# -------------------------- MAIN --------------------------------
# ================================================================


if __name__ == "__main__":

    # Args
    arguments = docopt(__doc__, version="TECH-INSTALL: 0.1")

    tech_name = arguments["--tech_name"]
    tech_path = arguments["--tech_path"]

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    main(tech_name, tech_path)
