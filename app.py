import panel as pn
from utils.textual_strings import WELCOME_MESSAGE, HEADER_STRING
from utils.sidebar import create_sidebar  # Import the create_sidebar function

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

# Create main content layout
main = pn.Column(
    header,
    welcome_message,
    css_classes=['main-content'],  # Apply CSS class to main content
)

# Create sidebar using the create_sidebar function and pass the main content layout
sidebar = create_sidebar(main)

# Create a template with a sidebar that can be toggled with a hamburger menu
layout = pn.template.FastListTemplate(
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
