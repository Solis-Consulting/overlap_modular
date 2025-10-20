import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import json
import numpy as np
import os

# Resolve paths safely (works locally and on Vercel)
BASE = os.path.dirname(os.path.abspath(__file__))

# Load JSON data
with open(os.path.join(BASE, 'unc_major_requirements.json'), 'r') as file:
    jsonData = json.load(file)

# Load focus capacity data
with open(os.path.join(BASE, 'unc_focus_capacities.json'), 'r') as file:
    focusData = json.load(file)

# Merge both datasets
jsonData.extend(focusData)

# Extract available majors
available_majors = {
    major["major"]: major
    for major in jsonData
    if "major" in major and "requirements" in major
}
major_options = [{"label": major, "value": major} for major in available_majors.keys()]

# Initialize Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Major Overlap Comparison", style={"textAlign": "center", "color": "white"}),

    html.Label("Select multiple majors:", style={"color": "white"}),
    dcc.Dropdown(
        id="majors-dropdown",
        options=major_options,
        placeholder="Select majors",
        multi=True,
        style={"color": "black"}
    ),

    dcc.Graph(id='heatmap', style={"width": "90%", "height": "700px"}),

    html.Div(
        id='details',
        children=[
            html.P("Click on a cell to view overlap details.", style={"color": "white"}),
            html.Ul(id='overlap-details', style={"color": "white"})
        ],
        style={"marginTop": "20px"}
    )
], style={
    "backgroundColor": "black",
    "color": "white",
    "fontFamily": "Arial, sans-serif",
    "minHeight": "100vh",
    "padding": "20px"
})

@app.callback(
    Output('heatmap', 'figure'),
    [Input('majors-dropdown', 'value')]
)
def update_heatmap(selected_majors):
    if not selected_majors or len(selected_majors) < 2:
        return go.Figure()  # Empty figure if not enough selections

    # Extract course data for selected majors
    courseData = {
        major: set(req["code"].strip() for req in available_majors[major]["requirements"] if "code" in req)
        for major in selected_majors
    }

    # Generate overlap matrix
    overlapMatrix = np.zeros((len(selected_majors), len(selected_majors)), dtype=int)
    for i, major1 in enumerate(selected_majors):
        for j, major2 in enumerate(selected_majors):
            overlapMatrix[i, j] = len(courseData[major1].intersection(courseData[major2]))

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=overlapMatrix,
        x=selected_majors,
        y=selected_majors,
        colorscale='Greys',
        colorbar=dict(title='Overlap Count')
    ))
    fig.update_layout(
        title='Course Overlap Between Selected Majors',
        xaxis=dict(tickangle=-45),
        yaxis=dict(title=''),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )
    return fig

@app.callback(
    Output('overlap-details', 'children'),
    [Input('majors-dropdown', 'value')]
)
def display_overlap_details(selected_majors):
    if not selected_majors or len(selected_majors) < 2:
        return []

    overlap_text = []
    for i, major1 in enumerate(selected_majors):
        for j, major2 in enumerate(selected_majors):
            if i < j:  # Avoid duplicate calculations (symmetrical matrix)
                overlap_courses = list(
                    set(req["code"].strip() for req in available_majors[major1]["requirements"] if "code" in req)
                    .intersection(
                        set(req["code"].strip() for req in available_majors[major2]["requirements"] if "code" in req)
                    )
                )
                overlap_text.append(
                    html.Li(
                        f"Overlap between {major1} and {major2}: "
                        f"{', '.join(overlap_courses) if overlap_courses else 'No overlap'}"
                    )
                )

    return overlap_text

if __name__ == '__main__':
    app.run_server(debug=True)
