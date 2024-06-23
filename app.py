import panel as pn
from utils.textualStrings import WELCOME_MESSAGE, HEADER_STRING
from utils.sidebar import create_sidebar  # Import the create_sidebar function

# Initialize Panel extension
pn.extension(notifications=True)

# Create header
header = pn.pane.Markdown(HEADER_STRING, styles={"font-size": "20px"})

# Create a welcome message
welcome_message = pn.pane.Markdown(WELCOME_MESSAGE, styles={"font-size": "18px"})

# Create main content layout
main = pn.Column(
    header,
    welcome_message
    )

# Create sidebar using the create_sidebar function and pass the main content layout
sidebar = create_sidebar(main)


# Create a template with a sidebar that can be toggled with a hamburger menu
layout = pn.template.FastListTemplate(
    title="Stingray Explorer",
    logo="./assets/images/stingray_explorer.png",
    favicon="./assets/images/stingray_explorer.png",
    collapsed_sidebar=False,
    sidebar=[sidebar],
    main_max_width="100%",
    theme="default",
    accent_base_color="#00A170",
    theme_toggle=True,
    meta_description="Stingray Explorer Dashboard",
    meta_keywords="Stingray, Explorer, Dashboard, Astronomy",
    header_accent_base_color="#00A170",
    neutral_color="#D3D3D3",
    corner_radius=5,
    main=[main],
    header_background="#000000",
    sidebar_width=250,
    meta_author="Kartik Mandar",
    font="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap",
    shadow=True,
)

# Serve the layout
layout.servable()

if __name__ == "__main__":
    pn.serve(layout)
