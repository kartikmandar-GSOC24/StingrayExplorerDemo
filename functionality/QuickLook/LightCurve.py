import holoviews as hv
import panel as pn
from utils.globals import loaded_event_data
import numpy as np
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt

hv.extension("bokeh")


def create_quicklook_lightcurve():
    pn.extension()

    if not loaded_event_data:
        tab1_content = pn.pane.Markdown(
            "### No loaded items available.\n\nPlease go to the Loading tab to load items."
        )
    else:
        event_list_dropdown = pn.widgets.Select(
            name="Select Event List",
            options={name: i for i, (name, event) in enumerate(loaded_event_data)},
        )

        dt_slider = pn.widgets.FloatSlider(
            name="Select dt",
            start=0.1,
            end=100,
            step=0.1,
            value=1,
        )

        line_output_hv = pn.pane.HoloViews(width=500, height=300)
        dataframe_output = pn.pane.DataFrame(width=500, height=300)
        line_output_matplotlib = pn.pane.Matplotlib(width=500, height=300)

        def create_dataframe(selected_event_list_index, dt):
            if selected_event_list_index is not None:
                event_list = loaded_event_data[selected_event_list_index][1]
                lc_new = event_list.to_lc(dt=dt)

                df = pd.DataFrame(
                    {
                        "Time": lc_new.time,
                        "Counts": lc_new.counts,
                    }
                )
                return df
            return None

        def generate_lightcurve(event=None):
            selected_event_list_index = event_list_dropdown.value
            dt = dt_slider.value
            df = create_dataframe(selected_event_list_index, dt)
            if df is not None:
                # Creating the line plot with HoloViews (Bokeh)
                line_plot_hv = df.hvplot.line(x="Time", y="Counts")
                line_output_hv.object = line_plot_hv

                # Creating the line plot with Matplotlib
                fig, ax = plt.subplots()
                ax.plot(df["Time"], df["Counts"], label="Light Curve")
                ax.set_xlabel("Time")
                ax.set_ylabel("Counts")
                ax.legend()
                line_output_matplotlib.object = fig

        def show_dataframe(event=None):
            selected_event_list_index = event_list_dropdown.value
            dt = dt_slider.value
            df = create_dataframe(selected_event_list_index, dt)
            if df is not None:
                # Display the DataFrame
                dataframe_output.object = df

        generate_lightcurve_button = pn.widgets.Button(
            name="Generate Light Curve", button_type="primary"
        )
        generate_lightcurve_button.on_click(generate_lightcurve)

        show_dataframe_button = pn.widgets.Button(
            name="Show DataFrame", button_type="primary"
        )
        show_dataframe_button.on_click(show_dataframe)

        tab1_content = pn.Column(
            event_list_dropdown,
            dt_slider,
            pn.Row(generate_lightcurve_button, show_dataframe_button),
            pn.Row(line_output_hv, dataframe_output),
            line_output_matplotlib,
        )

    tabs = pn.Tabs(
        ("Light Curve", tab1_content), dynamic=True, sizing_mode="stretch_width"
    )

    return tabs


# Uncomment for testing purposes
# pane = create_quicklook_lightcurve()
# pn.serve(pane)
