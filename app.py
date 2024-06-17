import panel as pn
from functions.LightCurve.LightCurveAnalysisPanel import create_light_curve_analysis_panel

# Load external stylesheet
external_stylesheets = ['./assets/stylesheets/app.css']

# Initialize Panel extension
pn.extension(notifications=True)

# Create header
header = pn.pane.Markdown(
    "<h1 style='text-align: center'>Welcome to the Stingray Explorer Dashboard</h1>",
)

# Create a welcome message
welcome_message = pn.pane.Markdown(
    """
    <div style='text-align: center'>
        <p>Welcome to the Stingray Explorer Dashboard! This dashboard is designed to provide a comprehensive toolset for X-ray astronomy data analysis. Here are the main features:</p>
        <ul>
            <li><b>Light Curve Analysis:</b> Visualize and analyze light curves to study the variability of X-ray sources over time.</li>
            <li><b>Power Spectrum Analysis:</b> Generate power spectra to investigate the periodic signals and frequency components of your data.</li>
            <li><b>Cross Spectrum Analysis:</b> Cross-correlate different light curves to explore phase lags and coherence between signals.</li>
        </ul>
        <p>Please use the sidebar to navigate to the different analysis tools. Each tool comes with interactive widgets to customize your analysis and generate plots on the fly.</p>
        <p>We hope you find this dashboard useful for your research!</p>
    </div>
    """,
    styles={"font-size": "16px"}
)

# Create sidebar with buttons for navigation
light_curve_button = pn.widgets.Button(name="Light Curve", button_type="primary")

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
        css_classes=['main-content']  # Apply CSS class to main content
    ),
    sizing_mode="stretch_width"
)

# Create a template with a sidebar that can be toggled with a hamburger menu
template = pn.template.MaterialTemplate(
    title="Stingray Explorer",
    logo="./assets/images/stingray_logo.png",
    collapsed_sidebar=True,
    sidebar=[sidebar],
    main=[main],
    header_background="#000000",
    sidebar_width=200,
)

# Serve the template
template.servable()

if __name__ == "__main__":
    pn.serve(template)
