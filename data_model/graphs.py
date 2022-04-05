from typing import Sequence

import plotly.graph_objects as go
import plotly.express as px


def pie_chart(title: str, labels: Sequence, values: Sequence) -> go.Figure:
    return go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            textinfo="label+percent",
            textfont={"size": 12},
            hoverinfo="label+value",
            textposition='inside',
            showlegend=False,
        ),
        go.Layout(
            title={
                "text": title,
                "font": {"color": "white", "size": 24},
            },
            colorway=px.colors.qualitative.Antique,
            width=640,
            height=640,
            paper_bgcolor="#333333",
        ),
    )
