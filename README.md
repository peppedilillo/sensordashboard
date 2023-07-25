# Sensor dashboard

A simple serial real-time dashboard made with [click](https://click.palletsprojects.com/en/8.1.x/) and [dash](https://plotly.com/dash/).

## Setup
To download this repository click on the `Code` green button at top right, then `Download ZIP`.

Unzip the archive somewhere. This will become your installation folder. It will contain the code and the measurements logs.

To create a conda environment needed for launching the app, move to the installation folder from your terminal and type:

`conda env create -f env.yml`

## Running
Activate the environment with:

`conda activate sensordashboard`

You are expected to launch the application specifying the serial device address.
Find your device name (say `COM3`), move to the installation folder and launch with:

`python main.py --dev=COM3`

The terminal will meet you with a localhost address, write it in a browser url bar or `ctrl+click` it. 
Logs are saved in CSV format in the `output` subdirectory of the installation folder.

## Uninstalling

`conda remove -n sensordashboard --all`

Should do.

## Screenshot

![sensordemo](assets/demo.gif)
