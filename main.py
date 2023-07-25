import time
from datetime import datetime
from pathlib import Path

import serial
from dash import Dash, dcc, html, Input, Output, callback
from plotly.subplots import make_subplots
import click

cached = {
    "times": [],
    "values": [],
}


app = Dash(__name__)
app.title = "Humidity sensor"
app.layout = html.Div(
    html.Div(
        [
            dcc.Store(id="signal"),
            html.H1("Humidity sensor real-time dashboard 👨‍🚒", id="title"),
            html.Div(
                [
                    html.Div("Right now..", id="container-label"),
                    html.Div(id="live-update-text"),
                ],
                id="container",
            ),
            dcc.Graph(id="live-update-graph"),
            dcc.Interval(
                id="interval-component",
                interval=1 * 1000,  # in milliseconds
                n_intervals=0,
            ),
            html.P("~p23", id="byline"),
        ]
    )
)


@callback(Output("signal", "data"), Input("interval-component", "n_intervals"))
def update(timer):
    t = round(time.time() - cached.setdefault("tstart", time.time()), 1)
    _, voltage = get_data()
    rh = 0.195 * float(voltage) / 5 - 38.5
    write_file(t, voltage, rh)
    cached["times"].append(t)
    cached["values"].append(rh)


@callback(Output("live-update-text", "children"), Input("signal", "data"))
def update_metrics(signal):
    t = cached["times"][-1]
    rh = cached["values"][-1]
    return [
        html.Span("⌛ {0:.1f} s ".format(t)),
        html.Span("☔ {0:.1f} RH%".format(rh)),
    ]


MAXDISPLAY = 1800  # half an hour


@callback(Output("live-update-graph", "figure"), Input("signal", "data"))
def update_graph_live(signal):
    fig = make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig["layout"] = {
        "template": "plotly_dark",
        "xaxis_title": "Time [s]",
        "yaxis_title": "Humidity [RH%]",
        "margin": {"l": 30, "r": 10, "b": 30, "t": 10},
        "legend": {"x": 0, "y": 1, "xanchor": "left"},
    }
    fig.add_trace(
        {
            "x": cached["times"][-MAXDISPLAY:],
            "y": cached["values"][-MAXDISPLAY:],
            "name": "values",
            "mode": "lines+markers",
            "type": "scatter",
        },
        1,
        1,
    )
    return fig


def get_data(cmd=b"!R\n"):
    def parse(r):
        try:
            t, voltage = r.split(", ")
            return float(t) / 1000, float(voltage)
        except ValueError:
            return None

    ser = cached["serial"]
    response = None
    while not response:
        ser.write(cmd)
        response = parse(ser.readline().decode())
    return response


def write_file(t, voltage, rh):
    with open(cached["filepath"], "a") as outfile:
        string = f"{t:.1f} {rh:.1f}\n"
        outfile.write(string)
        outfile.flush()


@click.command()
@click.option(
    "--dev", required=True, help="serial device name e.g., COM3 or dev//ttyUSB0"
)
@click.option(
    "--baud",
    default=115200,
    type=int,
    help="serial device name (e.g., COM3 or dev//ttyUSB0",
)
def main(dev, baud):
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_log.csv"
    outputdir = Path(__file__).parent.joinpath("output")
    outputdir.mkdir(exist_ok=True)
    cached["filepath"] = outputdir.joinpath(filename)
    with serial.Serial(dev, baudrate=baud, timeout=1) as ser:
        cached["serial"] = ser
        app.run_server(debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
