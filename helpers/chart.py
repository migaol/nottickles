import pandas as pd
import numpy as np
from quickchart import QuickChart, QuickChartFunction
import datetime as dt

def create_chart_url(data: pd.Series, axis_adj: int) -> str:
    qc = QuickChart()
    qc.width = 1280
    qc.height = 720
    qc.device_pixel_ratio = 2.0

    labels = [dt.datetime.strptime(date, "%Y%m%d").strftime("%b %d") for date in list(data.index)]
    yvals = list(data.values)

    qc.config = {
        "type": 'line',
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": data.name.title().replace('_', ' '),
                    "steppedLine": "true",
                    "spanGaps": "true",
                    "radius": 5,
                    "data": yvals,
                    "borderColor": "rgb(54, 162, 235)",
                    "backgroundColor": "rgb(54, 162, 235)",
                    "fill": "false"
                },
            ],
        },
        "options": {
            "scales": {
                "yAxes": [
                    {
                        "ticks": {
                            "min": nearest_x_below(np.nanmin(yvals), axis_adj),
                            "max": nearest_x_above(np.nanmax(yvals), axis_adj),
                            "callback": QuickChartFunction("(val) => val.toLocaleString()")
                        },
                    },
                ]
            }
        }
    }

    url = qc.get_url()
    return url

def nearest_x_below(num: int, x: int):
    return (num // x) * x

def nearest_x_above(num: int, x: int):
    return (num // x + 1) * x