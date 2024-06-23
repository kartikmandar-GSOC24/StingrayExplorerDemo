import panel as pn
from functionality.LightCurve.LightCurveAnalysisPanel import (
    create_light_curve_analysis_panel,
)
from utils.dataIngestion import create_data_ingestion_tabs

def create_sidebar(main):
    menu_items_core_stingray = [
        ("Light Curve", "Light Curve"), 
        ("Powerspectra", "Powerspectra"), 
        ("CrossCorrelation", "CrossCorrelation")
    ]

    menu_items_event_data = [
        ("Setup", "Setup"),
        ("Creating EventList", "Creating EventList"),
        ("Loading EventList", "Loading EventList"),
        ("Simulating EventList", "Simulating EventList"),
        ("Joining EventLists", "Joining EventLists")
    ]

    menu_items_lightcurves = [
        ("Creating Light Curve", "Creating Light Curve"),
        ("Properties", "Properties"),
        ("Operations", "Operations"),
        ("Methods", "Methods"),
        ("Plotting", "Plotting")
    ]

    menu_items_fourier_analysis = [
        ("Powerspectra", "Powerspectra"),
        ("Dynamical Power Spectra", "Dynamical Power Spectra"),
        ("Cross Spectra", "Cross Spectra")
    ]

    menu_items_cross_autocorrelations = [
        ("CrossCorrelation", "CrossCorrelation"), 
        ("AutoCorrelation", "AutoCorrelation")
    ]

    menu_items_bispectra = [
        ("Bispectrum Tutorial", "Bispectrum Tutorial"), 
        ("Window Functions", "Window Functions")
    ]

    menu_items_bayesian_excess_variance = [
        ("Theoretical Background", "Theoretical Background"), 
        ("Examples", "Examples")
    ]

    menu_items_multitaper_periodogram = [
        ("Multitaper Spectral Estimator", "Multitaper Spectral Estimator"), 
        ("Comparing Powerspectrum and Multitaper", "Comparing Powerspectrum and Multitaper")
    ]

    menu_items_lomb_scargle_spectra = [
        ("Lomb Scargle Powerspectrum", "Lomb Scargle Powerspectrum"), 
        ("Lomb Scargle Crossspectrum", "Lomb Scargle Crossspectrum")
    ]

    # Define button behaviors
    def show_content(event):
        content_mapping = {
            "Light Curve": create_light_curve_analysis_panel(),
            "Powerspectra": pn.pane.Markdown("### Powerspectra\n\nThis is the content for Powerspectra."),
            "CrossCorrelation": pn.pane.Markdown("### CrossCorrelation\n\nThis is the content for CrossCorrelation."),
            "Setup": pn.pane.Markdown("### Setup\n\nThis is the content for Setup."),
            "Creating EventList": pn.pane.Markdown("### Creating EventList\n\nThis is the content for Creating EventList."),
            "Loading EventList": pn.pane.Markdown("### Loading EventList\n\nThis is the content for Loading EventList."),
            "Simulating EventList": pn.pane.Markdown("### Simulating EventList\n\nThis is the content for Simulating EventList."),
            "Joining EventLists": pn.pane.Markdown("### Joining EventLists\n\nThis is the content for Joining EventLists."),
            "Creating Light Curve": pn.pane.Markdown("### Creating Light Curve\n\nThis is the content for Creating Light Curve."),
            "Properties": pn.pane.Markdown("### Properties\n\nThis is the content for Properties."),
            "Operations": pn.pane.Markdown("### Operations\n\nThis is the content for Operations."),
            "Methods": pn.pane.Markdown("### Methods\n\nThis is the content for Methods."),
            "Plotting": pn.pane.Markdown("### Plotting\n\nThis is the content for Plotting."),
            "Dynamical Power Spectra": pn.pane.Markdown("### Dynamical Power Spectra\n\nThis is the content for Dynamical Power Spectra."),
            "Cross Spectra": pn.pane.Markdown("### Cross Spectra\n\nThis is the content for Cross Spectra."),
            "AutoCorrelation": pn.pane.Markdown("### AutoCorrelation\n\nThis is the content for AutoCorrelation."),
            "Bispectrum Tutorial": pn.pane.Markdown("### Bispectrum Tutorial\n\nThis is the content for Bispectrum Tutorial."),
            "Window Functions": pn.pane.Markdown("### Window Functions\n\nThis is the content for Window Functions."),
            "Theoretical Background": pn.pane.Markdown("### Theoretical Background\n\nThis is the content for Theoretical Background."),
            "Examples": pn.pane.Markdown("### Examples\n\nThis is the content for Examples."),
            "Multitaper Spectral Estimator": pn.pane.Markdown("### Multitaper Spectral Estimator\n\nThis is the content for Multitaper Spectral Estimator."),
            "Comparing Powerspectrum and Multitaper": pn.pane.Markdown("### Comparing Powerspectrum and Multitaper\n\nThis is the content for Comparing Powerspectrum and Multitaper."),
            "Lomb Scargle Powerspectrum": pn.pane.Markdown("### Lomb Scargle Powerspectrum\n\nThis is the content for Lomb Scargle Powerspectrum."),
            "Lomb Scargle Crossspectrum": pn.pane.Markdown("### Lomb Scargle Crossspectrum\n\nThis is the content for Lomb Scargle Crossspectrum."),
        }

        selected_option = event.new
        if selected_option in content_mapping:
            main[:] = [content_mapping[selected_option]]
        else:
            main[:] = [pn.pane.Markdown(f"### {selected_option}\n\nContent not found.")]

    # Create button to load data
    load_data_button = pn.widgets.Button(name="Load Data", button_type="primary", styles={'width': '100%'})

    def load_data(event):
        main[:] = [create_data_ingestion_tabs()]

    load_data_button.on_click(load_data)

    # Create MenuButtons
    core_stingray_button = pn.widgets.MenuButton(name='Quicklook', items=menu_items_core_stingray, button_type='primary', styles={'width': '100%'})
    event_data_button = pn.widgets.MenuButton(name='Working with Event Data', items=menu_items_event_data, button_type='default', styles={'width': '100%'})
    lightcurves_button = pn.widgets.MenuButton(name='Working with Lightcurves', items=menu_items_lightcurves, button_type='default', styles={'width': '100%'})
    fourier_analysis_button = pn.widgets.MenuButton(name='Fourier Analysis', items=menu_items_fourier_analysis, button_type='default', styles={'width': '100%'})
    cross_autocorrelations_button = pn.widgets.MenuButton(name='Cross and Autocorrelations', items=menu_items_cross_autocorrelations, button_type='default', styles={'width': '100%'})
    bispectra_button = pn.widgets.MenuButton(name='Bispectra', items=menu_items_bispectra, button_type='default', styles={'width': '100%'})
    bayesian_excess_variance_button = pn.widgets.MenuButton(name='Bayesian Excess Variance', items=menu_items_bayesian_excess_variance, button_type='default', styles={'width': '100%'})
    multitaper_periodogram_button = pn.widgets.MenuButton(name='Multi-taper Periodogram', items=menu_items_multitaper_periodogram, button_type='default', styles={'width': '100%'})
    lomb_scargle_spectra_button = pn.widgets.MenuButton(name='Lomb Scargle Spectra', items=menu_items_lomb_scargle_spectra, button_type='default', styles={'width': '100%'})

    # Attach the event handler to the MenuButtons
    core_stingray_button.param.watch(show_content, "clicked")
    event_data_button.param.watch(show_content, "clicked")
    lightcurves_button.param.watch(show_content, "clicked")
    fourier_analysis_button.param.watch(show_content, "clicked")
    cross_autocorrelations_button.param.watch(show_content, "clicked")
    bispectra_button.param.watch(show_content, "clicked")
    bayesian_excess_variance_button.param.watch(show_content, "clicked")
    multitaper_periodogram_button.param.watch(show_content, "clicked")
    lomb_scargle_spectra_button.param.watch(show_content, "clicked")

    # Create a sidebar layout
    sidebar = pn.Column(
        pn.pane.Markdown("# Navigation"),
        load_data_button,
        event_data_button,
        lightcurves_button,
        fourier_analysis_button,
        cross_autocorrelations_button,
        bispectra_button,
        bayesian_excess_variance_button,
        multitaper_periodogram_button,
        lomb_scargle_spectra_button,
        core_stingray_button,

    )

    return sidebar
