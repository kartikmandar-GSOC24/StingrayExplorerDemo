import panel as pn

from functionality.QuickLook.LightCurve import create_quicklook_lightcurve
from utils.dataIngestion import create_data_ingestion_tabs


def create_sidebar(main):
    menu_items_quicklook_stingray = [
        ("Light Curve", "QuickLookLightCurve"),
        ("Powerspectra", "QuickLookPowerspectra"),
        ("CrossCorrelation", "QuickLookCrossCorrelation"),
    ]

    # Load Button
    load_data_button = pn.widgets.Button(
        name="Load Data", button_type="warning", styles={"width": "100%"}
    )

    # Create MenuButtons
    quicklook_stingray_button = pn.widgets.MenuButton(
        name="Quicklook",
        items=menu_items_quicklook_stingray,
        button_type="primary",
        styles={"width": "100%"},
    )

    # Load Button changing main content
    def load_data(event):
        main[:] = [create_data_ingestion_tabs()]

    load_data_button.on_click(load_data)

    # Quicklook Button changing main content
    def handle_quicklook_button_selection(event):
        clicked = event.new
        if clicked == "QuickLookLightCurve":
            main[:] = [create_quicklook_lightcurve()]
        elif clicked == "QuickLookPowerspectra":
            main[:] = [pn.pane.Markdown("### Powerspectra\n\nThis is the content for Powerspectra.")]
        elif clicked == "QuickLookCrossCorrelation":
            main[:] = [pn.pane.Markdown("### CrossCorrelation\n\nThis is the content for CrossCorrelation.")]
        else:
            main[:] = [pn.pane.Markdown(f"### {clicked}\n\nContent not found.")]

    # Attach the event handler to the MenuButtons
    quicklook_stingray_button.on_click(handle_quicklook_button_selection)

    sidebar = pn.Column(
        pn.pane.Markdown("# Navigation"),
        load_data_button,
        quicklook_stingray_button
    )

    return sidebar
