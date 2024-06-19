# utils/sidebar.py

import panel as pn
from functionality.LightCurve.LightCurveAnalysisPanel import (
    create_light_curve_analysis_panel,
)
from functionality.LightCurve.DataIngestion import create_data_ingestion_tab


def create_sidebar(main):
    # Create sidebar with dropdown menus for navigation
    core_stingray_dropdown = pn.widgets.Select(
        name="Quicklook",
        options=[
            "Select an Option",
            "Light Curve",
            "Powerspectra",
            "CrossCorrelation"
        ],
    )

    working_with_event_data_dropdown = pn.widgets.Select(
        name="Working with Event Data",
        options=[
            "Select an Option",
            "Setup",
            "Creating EventList",
            "Loading EventList",
            "Simulating EventList",
            "Joining EventLists",
        ],
    )

    working_with_lightcurves_dropdown = pn.widgets.Select(
        name="Working with Lightcurves",
        options=[
            "Select an Option",
            "Creating Light Curve",
            "Properties",
            "Operations",
            "Methods",
            "Plotting",
        ],
    )

    fourier_analysis_dropdown = pn.widgets.Select(
        name="Fourier Analysis",
        options=[
            "Select an Option",
            "Powerspectra",
            "Dynamical Power Spectra",
            "Cross Spectra",
        ],
    )

    cross_autocorrelations_dropdown = pn.widgets.Select(
        name="Cross and Autocorrelations",
        options=["Select an Option", "CrossCorrelation", "AutoCorrelation"],
    )

    bispectra_dropdown = pn.widgets.Select(
        name="Bispectra",
        options=["Select an Option", "Bispectrum Tutorial", "Window Functions"],
    )

    bayesian_excess_variance_dropdown = pn.widgets.Select(
        name="Bayesian Excess Variance",
        options=["Select an Option", "Theoretical Background", "Examples"],
    )

    multitaper_periodogram_dropdown = pn.widgets.Select(
        name="Multi-taper Periodogram",
        options=[
            "Select an Option",
            "Multitaper Spectral Estimator",
            "Comparing Powerspectrum and Multitaper",
        ],
    )

    lomb_scargle_spectra_dropdown = pn.widgets.Select(
        name="Lomb Scargle Spectra",
        options=[
            "Select an Option",
            "Lomb Scargle Powerspectrum",
            "Lomb Scargle Crossspectrum",
        ],
    )

    # Define button behaviors
    def show_content(event):
        content_mapping = {
            "Light Curve": create_light_curve_analysis_panel(),
            "Overview": pn.pane.Markdown(
                "### Overview\n\nThis is the content for Core Stingray Functionality Overview."
            ),
            "Working with Event Data": pn.pane.Markdown(
                "### Working with Event Data\n\nThis is the content for Working with Event Data."
            ),
            "Working with Lightcurves": pn.pane.Markdown(
                "### Working with Lightcurves\n\nThis is the content for Working with Lightcurves."
            ),
            "Fourier Analysis": pn.pane.Markdown(
                "### Fourier Analysis\n\nThis is the content for Fourier Analysis."
            ),
            "Cross and Autocorrelations": pn.pane.Markdown(
                "### Cross and Autocorrelations\n\nThis is the content for Cross and Autocorrelations."
            ),
            "Bispectra": pn.pane.Markdown(
                "### Bispectra\n\nThis is the content for Bispectra."
            ),
            "Bayesian Excess Variance": pn.pane.Markdown(
                "### Bayesian Excess Variance\n\nThis is the content for Bayesian Excess Variance."
            ),
            "Multi-taper Periodogram": pn.pane.Markdown(
                "### Multi-taper Periodogram\n\nThis is the content for Multi-taper Periodogram."
            ),
            "Lomb Scargle Spectra": pn.pane.Markdown(
                "### Lomb Scargle Spectra\n\nThis is the content for Lomb Scargle Spectra."
            ),
        }

        # Mapping sub-functions to their respective content
        sub_function_mapping = {
            "Setup": pn.pane.Markdown("### Setup\n\nThis is the content for Setup."),
            "Creating EventList": pn.pane.Markdown(
                "### Creating EventList\n\nThis is the content for Creating EventList."
            ),
            "Loading EventList": pn.pane.Markdown(
                "### Loading EventList\n\nThis is the content for Loading EventList."
            ),
            "Simulating EventList": pn.pane.Markdown(
                "### Simulating EventList\n\nThis is the content for Simulating EventList."
            ),
            "Joining EventLists": pn.pane.Markdown(
                "### Joining EventLists\n\nThis is the content for Joining EventLists."
            ),
            "Creating Light Curve": pn.pane.Markdown(
                "### Creating Light Curve\n\nThis is the content for Creating Light Curve."
            ),
            "Properties": pn.pane.Markdown(
                "### Properties\n\nThis is the content for Properties."
            ),
            "Operations": pn.pane.Markdown(
                "### Operations\n\nThis is the content for Operations."
            ),
            "Plotting": pn.pane.Markdown(
                "### Plotting\n\nThis is the content for Plotting."
            ),
            "Powerspectra": pn.pane.Markdown(
                "### Powerspectra\n\nThis is the content for Powerspectra."
            ),
            "Dynamical Power Spectra": pn.pane.Markdown(
                "### Dynamical Power Spectra\n\nThis is the content for Dynamical Power Spectra."
            ),
            "Cross Spectra": pn.pane.Markdown(
                "### Cross Spectra\n\nThis is the content for Cross Spectra."
            ),
            "CrossCorrelation": pn.pane.Markdown(
                "### CrossCorrelation\n\nThis is the content for CrossCorrelation."
            ),
            "AutoCorrelation": pn.pane.Markdown(
                "### AutoCorrelation\n\nThis is the content for AutoCorrelation."
            ),
            "Bispectrum Tutorial": pn.pane.Markdown(
                "### Bispectrum Tutorial\n\nThis is the content for Bispectrum Tutorial."
            ),
            "Window Functions": pn.pane.Markdown(
                "### Window Functions\n\nThis is the content for Window Functions."
            ),
            "Theoretical Background": pn.pane.Markdown(
                "### Theoretical Background\n\nThis is the content for Theoretical Background."
            ),
            "Examples": pn.pane.Markdown(
                "### Examples\n\nThis is the content for Examples."
            ),
            "Multitaper Spectral Estimator": pn.pane.Markdown(
                "### Multitaper Spectral Estimator\n\nThis is the content for Multitaper Spectral Estimator."
            ),
            "Comparing Powerspectrum and Multitaper": pn.pane.Markdown(
                "### Comparing Powerspectrum and Multitaper\n\nThis is the content for Comparing Powerspectrum and Multitaper."
            ),
            "Lomb Scargle Powerspectrum": pn.pane.Markdown(
                "### Lomb Scargle Powerspectrum\n\nThis is the content for Lomb Scargle Powerspectrum."
            ),
            "Lomb Scargle Crossspectrum": pn.pane.Markdown(
                "### Lomb Scargle Crossspectrum\n\nThis is the content for Lomb Scargle Crossspectrum."
            ),
        }

        selected_option = event.new
        if selected_option and selected_option != "Select an Option":
            if selected_option in sub_function_mapping:
                main[:] = [sub_function_mapping[selected_option]]
            else:
                main[:] = [content_mapping[selected_option]]
        else:
            main[:] = []  # Clear the main content if "Select an item" is selected

    # Create button to load data
    load_data_button = pn.widgets.Button(name="Load Data", button_type="primary")

    def load_data(event):
        main[:] = [create_data_ingestion_tab()]

    load_data_button.on_click(load_data)

    # Attach the event handler to the dropdowns
    core_stingray_dropdown.param.watch(show_content, "value")
    working_with_event_data_dropdown.param.watch(show_content, "value")
    working_with_lightcurves_dropdown.param.watch(show_content, "value")
    fourier_analysis_dropdown.param.watch(show_content, "value")
    cross_autocorrelations_dropdown.param.watch(show_content, "value")
    bispectra_dropdown.param.watch(show_content, "value")
    bayesian_excess_variance_dropdown.param.watch(show_content, "value")
    multitaper_periodogram_dropdown.param.watch(show_content, "value")
    lomb_scargle_spectra_dropdown.param.watch(show_content, "value")

    # Create a sidebar layout
    sidebar = pn.Column(
        pn.pane.Markdown("# Navigation"),
        load_data_button,
        core_stingray_dropdown,
        working_with_event_data_dropdown,
        working_with_lightcurves_dropdown,
        fourier_analysis_dropdown,
        cross_autocorrelations_dropdown,
        bispectra_dropdown,
        bayesian_excess_variance_dropdown,
        multitaper_periodogram_dropdown,
        lomb_scargle_spectra_dropdown,
        css_classes=["pn-Column"],  # Apply CSS class to sidebar
    )

    return sidebar
