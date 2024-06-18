# utils/sidebar.py

import panel as pn
from functions.LightCurve.LightCurveAnalysisPanel import create_light_curve_analysis_panel

def create_sidebar(main):
    # Create sidebar with buttons for navigation
    light_curve_button = pn.widgets.Button(name="Light Curve")

    # Define button behaviors
    def show_light_curve(event):
        main[:] = [create_light_curve_analysis_panel()]  # Replace main content with light curve analysis pane

    light_curve_button.on_click(show_light_curve)

    # Create a sidebar layout
    sidebar = pn.Column(
        light_curve_button,
        css_classes=['pn-Column']  # Apply CSS class to sidebar
    )
    
    return sidebar
