# PS2 Cover Downloader

![Application Screenshot](https://i.imgur.com/ZW70463.jpeg)

## Description

The PS2 Cover Downloader is a Python-based application that automates the process of downloading cover art for PlayStation 2 games. The application scans a specified directory for PS2 game files, retrieves the corresponding cover art from an online repository, and saves the images to a designated output directory.

## Features

- Scans a directory for PS2 game files (`.iso`, `.bin`, `.img`, `.nrg`, `.mdf`).
- Downloads cover art for the detected games.
- Displays a progress bar to indicate the download status.
- Provides a graphical user interface (GUI) for easy interaction.

## Requirements

- Python 3.x (if running from source)
- `tkinter` for the GUI (if running from source)
- `requests` for HTTP requests (if running from source)
- `ttkbootstrap` for enhanced GUI styling (if running from source)

## Installation

### Running from Source

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ps2-cover-downloader.git
    cd ps2-cover-downloader
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the application:
    ```sh
    python ps2_cover_downloader.py
    ```

### Using the Executable

1. Download the executable file from the [releases page](https://github.com/yourusername/ps2-cover-downloader/releases).

2. Run the executable file.

## Usage

1. Use the GUI to:
    - Select the directory containing your PS2 game files.
    - Select the directory where you want to save the downloaded cover art.
    - Click the "Start" button to begin the download process.

## Credits

- Cover arts are sourced from the [xlenore/ps2-covers](https://github.com/xlenore/ps2-covers) repository.
- Game titles and serial numbers are sourced from the [VTSTech/PS2-OPL-CFG](https://github.com/VTSTech/PS2-OPL-CFG/tree/master) repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

This project is open source and contributions are welcome! Feel free to fork the repository and submit pull requests to add or amend any features.