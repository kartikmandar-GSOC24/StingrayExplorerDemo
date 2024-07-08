import panel as pn
from stingray.events import EventList
from stingray import Lightcurve
import asyncio
import warnings
import os
import stat
import numpy as np
from bokeh.models import Tooltip
from .globals import loaded_event_data

# Initialize Panel extension
pn.extension()

# Path to the topmost directory for loaded-data
loaded_data_path = os.path.join(os.getcwd(), "demo", "loaded-data")

# Create the loaded-data directory if it doesn't exist
os.makedirs(loaded_data_path, exist_ok=True)


# Custom warning handler
class WarningHandler:
    def __init__(self):
        self.warnings = []

    def warn(
        self, message, category=None, filename=None, lineno=None, file=None, line=None
    ):
        warning_message = f"Message: {message}\nCategory: {category.__name__ if category else 'N/A'}\nFile: {filename if filename else 'N/A'}\nLine: {lineno if lineno else 'N/A'}\n"
        self.warnings.append(warning_message)


# Create an instance of the warning handler
warning_handler = WarningHandler()

# Redirect warnings to the custom handler
warnings.showwarning = warning_handler.warn

# # Global list to store event data
# loaded_event_data = []


async def load_event_data(
    event,
    file_selector,
    filename_input,
    format_input,
    format_checkbox,
    output,
    warning_output,
):
    if not file_selector.value:
        output.value = "No file selected. Please select a file to upload."
        return

    file_paths = file_selector.value
    filenames = (
        [name.strip() for name in filename_input.value.split(",")]
        if filename_input.value
        else []
    )
    formats = (
        [fmt.strip() for fmt in format_input.value.split(",")]
        if format_input.value
        else []
    )

    if format_checkbox.value:
        formats = ["ogip" for _ in range(len(file_paths))]

    if len(filenames) < len(file_paths):
        filenames.extend(
            [
                os.path.basename(path).split(".")[0]
                for path in file_paths[len(filenames) :]
            ]
        )
    if len(formats) < len(file_paths):
        output.value = (
            "Please specify formats for all files or check the default format option."
        )
        return

    try:
        loaded_files = []
        loop = asyncio.get_event_loop()
        for file_path, file_name, file_format in zip(file_paths, filenames, formats):
            if any(file_name == event[0] for event in loaded_event_data):
                output.value = f"A file with the name '{file_name}' already exists in memory. Please provide a different name."
                return

            event_list = await loop.run_in_executor(
                None, EventList.read, file_path, file_format
            )
            loaded_event_data.append((file_name, event_list))
            loaded_files.append(
                f"File '{file_path}' loaded successfully as '{file_name}' with format '{file_format}'."
            )

        output.value = "\n".join(loaded_files)
        if warning_handler.warnings:
            warning_output.value = "\n".join(warning_handler.warnings)
        else:
            warning_output.value = "No warnings."
    except Exception as e:
        output.value = f"An error occurred: {e}"

    # Clear the warnings after displaying them
    warning_handler.warnings.clear()


def save_loaded_files(
    event, filename_input, format_input, format_checkbox, output, warning_output
):
    if not loaded_event_data:
        output.value = "No files loaded to save."
        return

    filenames = (
        [name.strip() for name in filename_input.value.split(",")]
        if filename_input.value
        else [event[0] for event in loaded_event_data]
    )
    formats = (
        [fmt.strip() for fmt in format_input.value.split(",")]
        if format_input.value
        else []
    )

    if format_checkbox.value:
        formats = ["hdf5" for _ in range(len(loaded_event_data))]

    if len(filenames) < len(loaded_event_data):
        output.value = "Please specify names for all loaded files."
        return
    if len(filenames) != len(loaded_event_data):
        output.value = (
            "Please ensure that the number of names matches the number of loaded files."
        )
        return
    if len(formats) < len(loaded_event_data):
        output.value = "Please specify formats for all loaded files or check the default format option."
        return

    saved_files = []
    try:
        for (loaded_name, event_list), file_name, file_format in zip(
            loaded_event_data, filenames, formats
        ):
            if os.path.exists(
                os.path.join(loaded_data_path, f"{file_name}.{file_format}")
            ):
                output.value = f"A file with the name '{file_name}' already exists. Please provide a different name."
                return

            save_path = os.path.join(loaded_data_path, f"{file_name}.{file_format}")
            if file_format == 'hdf5':
                event_list.to_astropy_table().write(save_path, format=file_format, path='data')
            else:
                event_list.write(save_path, file_format)

            saved_files.append(
                f"File '{file_name}' saved successfully to '{save_path}'."
            )

        output.value = "\n".join(saved_files)
        if warning_handler.warnings:
            warning_output.value = "\n".join(warning_handler.warnings)
        else:
            warning_output.value = "No warnings."
    except Exception as e:
        output.value = f"An error occurred while saving files: {e}"

    # Clear the warnings after displaying them
    warning_handler.warnings.clear()



def delete_selected_files(event, file_selector, output, warning_output):
    if not file_selector.value:
        output.value = "No file selected. Please select a file to delete."
        return

    file_paths = file_selector.value
    deleted_files = []
    for file_path in file_paths:
        if file_path.endswith(".py"):
            deleted_files.append(
                f"Cannot delete file '{file_path}': Deleting .py files is not allowed."
            )
            continue

        try:
            # Change the file permissions to ensure it can be deleted
            os.chmod(file_path, stat.S_IWUSR | stat.S_IREAD | stat.S_IWRITE)
            os.remove(file_path)
            deleted_files.append(f"File '{file_path}' deleted successfully.")
        except Exception as e:
            deleted_files.append(f"An error occurred while deleting '{file_path}': {e}")

    output.value = "\n".join(deleted_files)
    if warning_handler.warnings:
        warning_output.value = "\n".join(warning_handler.warnings)
    else:
        warning_output.value = "No warnings."

    warning_handler.warnings.clear()


def preview_loaded_files(event, output, warning_output, time_limit=10):
    if not loaded_event_data:
        output.value = "No files loaded to preview."
        return

    preview_data = []
    for file_name, event_list in loaded_event_data:
        try:
            time_data = f"Times (first {time_limit}): {event_list.time[:time_limit]}"
            mjdref = f"MJDREF: {event_list.mjdref}"
            gti = f"GTI: {event_list.gti}"
            preview_data.append(f"File: {file_name}\n{time_data}\n{mjdref}\n{gti}\n")
        except Exception as e:
            warning_handler.warn(str(e), category=RuntimeWarning)

    if preview_data:
        output.value = "\n\n".join(preview_data)
    else:
        output.value = "No valid files loaded for preview."

    if warning_handler.warnings:
        warning_output.value = "\n".join(warning_handler.warnings)
    else:
        warning_output.value = "No warnings."

    warning_handler.warnings.clear()


def create_loading_tab():
    file_selector = pn.widgets.FileSelector(
        os.getcwd(), only_files=True, name="Select File", show_hidden=True
    )
    filename_input = pn.widgets.TextInput(
        name="Enter File Names",
        placeholder="Enter file names, comma-separated",
        width=400,
    )
    format_input = pn.widgets.TextInput(
        name="Enter Formats",
        placeholder="Enter formats (e.g., ogip, pickle, hdf5), comma-separated",
        width=400,
    )
    format_checkbox = pn.widgets.Checkbox(
        name="Use default format (ogip for loading, hdf5 for saving)", value=False
    )
    load_button = pn.widgets.Button(name="Load Event Data", button_type="primary")
    save_button = pn.widgets.Button(name="Save Loaded Data", button_type="success")
    delete_button = pn.widgets.Button(
        name="Delete Selected Files", button_type="danger"
    )
    preview_button = pn.widgets.Button(
        name="Preview Loaded Files", button_type="default"
    )
    output = pn.widgets.TextAreaInput(
        name="Output", value="", disabled=True, height=200
    )
    warning_output = pn.widgets.TextAreaInput(
        name="Warnings", value="", disabled=True, height=200
    )

    tooltip_format = pn.widgets.TooltipIcon(
        value=Tooltip(
            content="""For HEASoft-supported missions, use 'ogip'. Using 'fits' directly might cause issues with Astropy tables. default = ogip (for reading), hdf5 (for saving)""",
            position="bottom",
        )
    )

    tooltip_file = pn.widgets.TooltipIcon(
        value=Tooltip(
            content="""Ensure the file contains at least a 'time' column.""",
            position="bottom",
        )
    )

    def on_load_click(event):
        # Clear previous outputs and warnings
        output.value = ""
        warning_output.value = ""
        warning_handler.warnings.clear()
        warnings.resetwarnings()

        asyncio.create_task(
            load_event_data(
                event,
                file_selector,
                filename_input,
                format_input,
                format_checkbox,
                output,
                warning_output,
            )
        )


        

    def on_save_click(event):
        # Clear previous outputs and warnings
        output.value = ""
        warning_output.value = ""
        warning_handler.warnings.clear()
        warnings.resetwarnings()

        save_loaded_files(
            event, filename_input, format_input, format_checkbox, output, warning_output
        )
        line_output_hv = pn.pane.HoloViews(height=300, width=500)


    def on_delete_click(event):
        # Clear previous outputs and warnings
        output.value = ""
        warning_output.value = ""
        warning_handler.warnings.clear()
        warnings.resetwarnings()

        delete_selected_files(event, file_selector, output, warning_output)

    def on_preview_click(event):
        # Clear previous outputs and warnings
        output.value = ""
        warning_output.value = ""
        warning_handler.warnings.clear()
        warnings.resetwarnings()

        preview_loaded_files(event, output, warning_output)

    load_button.on_click(on_load_click)
    save_button.on_click(on_save_click)
    delete_button.on_click(on_delete_click)
    preview_button.on_click(on_preview_click)

    first_column = pn.Column(
        pn.pane.Markdown("# Load Files"),
        file_selector,
        pn.Row(filename_input, tooltip_file),
        pn.Row(format_input, tooltip_format),
        format_checkbox,
        pn.Row(load_button, save_button, delete_button, preview_button),
        width_policy="min",
    )

    second_column = pn.Column(
        pn.pane.Markdown("# Output and Warnings"),
        pn.Column(output, warning_output),
        width_policy="min",
    )

    tab_content = pn.Row(first_column, pn.Spacer(width=40), second_column)
    return tab_content


def create_event_list(
    event,
    times_input,
    energy_input,
    gti_input,
    mjdref_input,
    name_input,
    output,
    warning_output,
):
    try:
        if not times_input.value or not mjdref_input.value:
            output.value = "Please enter Photon Arrival Times and MJDREF."
            return

        times = [float(t) for t in times_input.value.split(",")]
        mjdref = float(mjdref_input.value)
        energy = (
            [float(e) for e in energy_input.value.split(",")]
            if energy_input.value
            else None
        )
        gti = (
            [
                [float(g) for g in interval.split()]
                for interval in gti_input.value.split(";")
            ]
            if gti_input.value
            else None
        )

        if name_input.value:
            name = name_input.value
            if any(name == event[0] for event in loaded_event_data):
                output.value = f"A file with the name '{name}' already exists in memory. Please provide a different name."
                return
        else:
            name = f"event_list_{len(loaded_event_data)}"

        event_list = EventList(times, energy=energy, gti=gti, mjdref=mjdref)

        loaded_event_data.append((name, event_list))

        output.value = f"""
        Event List created successfully!
        Saved as: {name}
        Times: {event_list.time}
        MJDREF: {event_list.mjdref}
        GTI: {event_list.gti}
        Energy: {event_list.energy if energy else 'Not provided'}
        """
    except ValueError as ve:
        warning_handler.warn(str(ve), category=ValueError)
    except Exception as e:
        warning_handler.warn(str(e), category=RuntimeError)

    if warning_handler.warnings:
        warning_output.value = "\n".join(warning_handler.warnings)
    else:
        warning_output.value = "No warnings."

    warning_handler.warnings.clear()

def simulate_event_list(event, time_slider, count_slider, dt_input, name_input, method_selector, output, warning_output):
    try:
        if not name_input.value:
            output.value = "Please provide a name for the simulated event list."
            return

        if any(name_input.value == event[0] for event in loaded_event_data):
            output.value = f"A file with the name '{name_input.value}' already exists in memory. Please provide a different name."
            return

        times = np.arange(time_slider.value)
        counts = np.floor(np.random.rand(time_slider.value) * count_slider.value)
        dt = dt_input.value
        lc = Lightcurve(times, counts, dt=dt, skip_checks=True)
        
        if method_selector.value == "Standard Method":
            event_list = EventList.from_lc(lc)
        else:
            event_list = EventList()
            event_list.simulate_times(lc)
        
        name = name_input.value
        loaded_event_data.append((name, event_list))
        
        output.value = f"""
        Event List simulated successfully!
        Saved as: {name}
        Times: {event_list.time}
        Counts: {counts}
        """
    except Exception as e:
        warning_handler.warn(str(e), category=RuntimeError)
    
    if warning_handler.warnings:
        warning_output.value = "\n".join(warning_handler.warnings)
    else:
        warning_output.value = "No warnings."
    
    warning_handler.warnings.clear()


def create_event_list_tab():
    output = pn.widgets.TextAreaInput(
        name="Output", value="", disabled=True, height=200
    )
    warning_output = pn.widgets.TextAreaInput(
        name="Warnings", value="", disabled=True, height=200
    )

    # Column 1: Create Event List
    times_input = pn.widgets.TextInput(
        name="Photon Arrival Times", placeholder="e.g., 0.5, 1.1, 2.2, 3.7"
    )
    mjdref_input = pn.widgets.TextInput(name="MJDREF", placeholder="e.g., 58000.")
    energy_input = pn.widgets.TextInput(
        name="Energy (optional)", placeholder="e.g., 0., 3., 4., 20."
    )
    gti_input = pn.widgets.TextInput(
        name="GTIs (optional)", placeholder="e.g., 0 4; 5 10"
    )
    name_input = pn.widgets.TextInput(
        name="Event List Name", placeholder="e.g., my_event_list"
    )
    create_button = pn.widgets.Button(name="Create Event List", button_type="primary")

    create_button.on_click(
        lambda event: create_event_list(
            event,
            times_input,
            energy_input,
            gti_input,
            mjdref_input,
            name_input,
            output,
            warning_output,
        )
    )

    # Column 2: Simulating Event Lists (from Light Curves)
    simulation_title = pn.pane.Markdown("# Simulating Event Lists")
    time_slider = pn.widgets.IntSlider(name="Number of Time Bins", start=1, end=10000, value=10)
    count_slider = pn.widgets.IntSlider(name="Max Counts per Bin", start=1, end=10000, value=5)
    dt_input = pn.widgets.FloatSlider(name="Delta Time (dt)", start=0.0001, end=10000., step=0.001, value=1.0)
    method_selector = pn.widgets.Select(name="Method", options=["Standard Method", "Inverse CDF Method"])
    sim_name_input = pn.widgets.TextInput(name="Simulated Event List Name", placeholder="e.g., my_sim_event_list") 
    simulate_button = pn.widgets.Button(name="Simulate Event List", button_type="primary")

    simulate_button.on_click(
        lambda event: simulate_event_list(
            event,
            time_slider,
            count_slider,
            dt_input,
            sim_name_input,
            method_selector,
            output,
            warning_output,
        )
    )

    tab_content = pn.Column(
        
        pn.Row(
            pn.Column(
                pn.pane.Markdown("# Create Event List"),
                times_input,
                mjdref_input,
                energy_input,
                gti_input,
                name_input,
                create_button,
            ),
            pn.Spacer(width=40),
            pn.Column(
                simulation_title,
                time_slider,
                count_slider,
                dt_input,
                method_selector,
                sim_name_input,
                simulate_button,
            ),
        ),
        pn.Row(
            pn.Column(output),
            pn.Column(warning_output), 

        )
    )
    return tab_content


# def convert_eventlist_to_astropy_table(
#     event, file_selector, filename_input, output, warning_output
# ):
    if not file_selector.value:
        output.value = "No file selected. Please select a file to convert."
        return

    file_paths = file_selector.value
    filenames = (
        [name.strip() for name in filename_input.value.split(",")]
        if filename_input.value
        else []
    )

    if len(filenames) < len(file_paths):
        filenames.extend(
            [
                generate_unique_filename_converted(prefix="AstropyTable_")
                for _ in range(len(filenames), len(file_paths))
            ]
        )

    try:
        converted_files = []
        for file_path, file_name in zip(file_paths, filenames):
            if os.path.exists(os.path.join(conversions_data_path, f"{file_name}.csv")):
                output.value = f"A file with the name '{file_name}' already exists. Please provide a different name."
                return

            # Load the data from the .npz file
            data = np.load(file_path)
            if "time" not in data or "gti" not in data or "mjdref" not in data:
                output.value = f"Invalid data format in file '{file_path}'."
                return

            event_list = EventList(data["time"], gti=data["gti"], mjdref=data["mjdref"])
            table = event_list.to_astropy_table()

            save_path = os.path.join(conversions_data_path, f"{file_name}.csv")
            table.write(save_path, format="csv")

            converted_files.append(
                f"File '{file_path}' converted successfully as '{file_name}.csv'"
            )

        output.value = "\n".join(converted_files)
        if warning_handler.warnings:
            warning_output.value = "\n".join(warning_handler.warnings)
        else:
            warning_output.value = "No warnings."

        # Display the converted tables
        tables_preview = []
        for file_name in filenames:
            table = Table.read(os.path.join(conversions_data_path, f"{file_name}.csv"))
            tables_preview.append(str(table))

        output.value += "\n\n" + "\n\n".join(tables_preview)

    except Exception as e:
        output.value = f"An error occurred: {e}"

    # Clear the warnings after displaying them
    warning_handler.warnings.clear()


def create_help_tab():
    help_content = """
    # Help

    ## Loading Tab

    ### Functionality
    The "Loading" tab allows you to load, save, delete, and preview event data files. Here is a detailed explanation of each component and its functionality:

    - **File Selector**: Select files to load into the event data list.
    - **Enter File Names**: Specify custom names for the loaded files. If left blank, the names will be derived from the file paths.
    - **Enter Formats**: Specify the formats of the files being loaded. If left blank, the default format is used.
    - **Use default format**: Check this to use the default format ('ogip' for loading and 'hdf5' for saving).
    - **Load Event Data**: Load the selected files into the event data list.
    - **Save Loaded Data**: Save the loaded event data files to the specified directory.
    - **Delete Selected Files**: Delete the selected files from the file system.
    - **Preview Loaded Files**: Preview the contents of the loaded event data files.

    ### Precautions
    - Ensure the file contains at least a 'time' column when loading event data.
    - When specifying custom names or formats, ensure that the number of names/formats matches the number of files selected.
    - Deleting files with the ".py" extension is not allowed to prevent accidental deletion of script files.

    ### Examples
    #### Loading an Event List
    ```python
    from stingray import EventList
    ev = EventList.read('events.fits', 'ogip')
    print(ev.time)
    ```

    #### Saving an Event List
    ```python
    ev.write("events.hdf5", "hdf5")
    ```

    ## Creation Tab

    ### Functionality
    The "Creation" tab allows you to create new event lists or simulate event lists from light curves. Here is a detailed explanation of each component and its functionality:

    - **Photon Arrival Times**: Enter photon arrival times in seconds from a reference MJD.
    - **MJDREF**: Enter the MJD reference for the photon arrival times.
    - **Energy (optional)**: Enter the energy values associated with the photons.
    - **GTIs (optional)**: Enter the Good Time Intervals (GTIs) for the event list.
    - **Event List Name**: Specify a name for the new event list.
    - **Create Event List**: Create a new event list with the specified parameters.

    ### Simulation of Event Lists
    - **Number of Time Bins**: Specify the number of time bins for the simulation.
    - **Max Counts per Bin**: Specify the maximum counts per bin.
    - **Delta Time (dt)**: Specify the delta time for the light curve.
    - **Method**: Choose between "Standard Method" and "Inverse CDF Method" for simulating event lists.
    - **Simulated Event List Name**: Specify a name for the simulated event list.
    - **Simulate Event List**: Simulate an event list using the specified parameters.

    ### Precautions
    - Ensure that photon arrival times and MJDREF are provided when creating an event list.
    - When simulating event lists, ensure that the provided parameters (e.g., number of time bins, max counts per bin) are reasonable to avoid excessively large or small event lists.

    ### Examples
    #### Creating an Event List
    ```python
    from stingray import EventList
    times = [0.5, 1.1, 2.2, 3.7]
    mjdref = 58000.
    energy = [0., 3., 4., 20.]
    gti = [[0, 4]]
    ev = EventList(times, gti=gti, energy=energy, mjdref=mjdref)
    print(ev.time)
    ```

    #### Simulating an Event List from a Light Curve
    ```python
    from stingray import EventList, Lightcurve
    times = np.arange(3)
    counts = np.floor(np.random.rand(3) * 5)
    lc = Lightcurve(times, counts, skip_checks=True, dt=1.)
    ev = EventList.from_lc(lc)
    print(ev.time)
    ```

    ## Stingray Documentation References

    ### Creating EventList from Photon Arrival Times
    ```python
    from stingray import EventList
    times = [0.5, 1.1, 2.2, 3.7]
    mjdref = 58000.
    ev = EventList(times, mjdref=mjdref)
    print(ev.time)
    ```

    ### Transforming a Lightcurve into an EventList
    ```python
    from stingray import EventList, Lightcurve
    times = np.arange(3)
    counts = np.floor(np.random.rand(3) * 5)
    lc = Lightcurve(times, counts, skip_checks=True, dt=1.)
    ev = EventList.from_lc(lc)
    print(ev.time)
    ```

    ### Simulating EventList from Lightcurve
    ```python
    from stingray import EventList, Lightcurve
    times = np.arange(50)
    counts = np.floor(np.random.rand(50) * 50000)
    lc = Lightcurve(times, counts, skip_checks=True, dt=1.)
    ev = EventList()
    ev.simulate_times(lc)
    print(ev.time)
    ```

    ### Loading and Writing EventList Objects
    ```python
    from stingray import EventList
    ev = EventList.read('events.fits', 'ogip')
    ev.write("events.hdf5", "hdf5")
    ```

    ## Conclusion
    This help tab provides detailed information about the functionality of the "Loading" and "Creation" tabs, precautions to take while using them, and examples to illustrate their usage. For further information, refer to the Stingray documentation.
    """

    help_markdown = pn.pane.Markdown(help_content)
    return help_markdown

def create_data_ingestion_tabs():
    tabs = pn.Tabs(
        ("Loading", create_loading_tab()),
        ("Creation", create_event_list_tab()),
        ("Help", create_help_tab()),
        dynamic=True,
    )
    return tabs


# Example usage in your main script (e.g., app.py)
layout = pn.Column(create_data_ingestion_tabs())

# Serve the layout
layout.servable()

if __name__ == "__main__":
    pn.serve(layout)
