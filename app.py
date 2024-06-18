import panel as pn
from functions.LightCurve.LightCurveAnalysisPanel import create_light_curve_analysis_panel
from utils.textual_strings import WELCOME_MESSAGE, HEADER_STRING


# Load external stylesheet
external_stylesheets = ['./assets/stylesheets/app.css']

# Initialize Panel extension
pn.extension(notifications=True)

# Create header
header = pn.pane.Markdown(
    HEADER_STRING
)

# Create a welcome message
welcome_message = pn.pane.Markdown(
    WELCOME_MESSAGE,
    styles={"font-size": "16px", "align": "start"}
)

# Create sidebar with buttons for navigation
light_curve_button = pn.widgets.Button(name="Light Curve")

# Define button behaviors
def show_light_curve(event):
    main[0] = create_light_curve_analysis_panel  # Replace main content with light curve analysis pane

light_curve_button.on_click(show_light_curve)


# Create a sidebar layout
sidebar = pn.Column(
    light_curve_button,
    css_classes=['pn-Column']  # Apply CSS class to sidebar
)

# Create main content layout
main = pn.Row(
    pn.Column(
        header,
        welcome_message,
        css_classes=['main-content'],  # Apply CSS class to main content
        align="center"
    ),
    sizing_mode="stretch_width"
)

# Create a template with a sidebar that can be toggled with a hamburger menu
layout = pn.template.MaterialTemplate(
    title="Stingray Explorer",
    logo="./assets/images/stingray_logo.png",
    collapsed_sidebar=True,
    sidebar=[sidebar],
    main=[main],
    header_background="#000000",
    sidebar_width=150,
)

# Serve the layout
layout.servable()

if __name__ == "__main__":
    pn.serve(layout)
