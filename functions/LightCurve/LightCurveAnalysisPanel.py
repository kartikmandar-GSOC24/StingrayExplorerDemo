import panel as pn
from .DataIngestion import create_data_ingestion_tab

def create_light_curve_analysis_panel():
    # Initialize Panel extension
    pn.extension()

    # Tab 1: Data ingestion (using content from DataIngesion.py)
    tab_data_ingestion = create_data_ingestion_tab()

    # Tab 2: Light Curve
    tab2_content = pn.pane.Markdown("### Light Curve\n\nThis is the content for Light Curve.")
    tab2 = pn.Column(tab2_content, name="Light Curve")

    # Tab 3: GTI
    tab3_content = pn.pane.Markdown("### GTI\n\nThis is the content for GTI.")
    tab3 = pn.Column(tab3_content, name="GTI")

    # Tab 4: tab4
    tab4_content = pn.pane.Markdown("### tab4\n\nThis is the content for tab4.")
    tab4 = pn.Column(tab4_content, name="tab4")

    # Tab 5: tab5
    tab5_content = pn.pane.Markdown("### tab5\n\nThis is the content for tab5.")
    tab5 = pn.Column(tab5_content, name="tab5")

    # Tab 6: tab6
    tab6_content = pn.pane.Markdown("### tab6\n\nThis is the content for tab6.")
    tab6 = pn.Column(tab6_content, name="tab6")

    # Tab 7: tab7
    tab7_content = pn.pane.Markdown("### tab7\n\nThis is the content for tab7.")
    tab7 = pn.Column(tab7_content, name="tab7")

    # Tab 8: tab8
    tab8_content = pn.pane.Markdown("### tab8\n\nThis is the content for tab8.")
    tab8 = pn.Column(tab8_content, name="tab8")

    # Tab 9: tab9
    tab9_content = pn.pane.Markdown("### tab9\n\nThis is the content for tab9.")
    tab9 = pn.Column(tab9_content, name="tab9")

    # Tab 10: tab10
    tab10_content = pn.pane.Markdown("### tab10\n\nThis is the content for tab10.")
    tab10 = pn.Column(tab10_content, name="tab10")

    # Tab 11: tab11
    tab11_content = pn.pane.Markdown("### tab11\n\nThis is the content for tab11.")
    tab11 = pn.Column(tab11_content, name="tab11")

    # Tab 12: tab12
    tab12_content = pn.pane.Markdown("### tab12\n\nThis is the content for tab12.")
    tab12 = pn.Column(tab12_content, name="tab12")

    # Create Tabs
    tabs = pn.Tabs(
        ("Data ingestion", tab_data_ingestion),
        ("Light Curve", tab2),
        ("GTI", tab3),
        ("tab4", tab4),
        ("tab5", tab5),
        ("tab6", tab6),
        ("tab7", tab7),
        ("tab8", tab8),
        ("tab9", tab9),
        ("tab10", tab10),
        ("tab11", tab11),
        ("tab12", tab12),
        dynamic=True,
        sizing_mode="stretch_width"
    )

    return tabs
