import panel as pn
from stingray.events import EventList
import asyncio
import warnings
import os
import numpy as np
import random
from bokeh.models import Tooltip

# Initialize Panel extension
pn.extension()

# Path to the topmost directory for loaded-data
loaded_data_path = os.path.join(os.getcwd(), "loaded-data")

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

# Global list to store event data
loaded_event_data = []


async def load_event_data(
    event, file_selector, filename_input, format_input, output, warning_output
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

    if len(filenames) < len(file_paths):
        filenames.extend(
            [f"default{i+1}" for i in range(len(filenames), len(file_paths))]
        )
    if len(formats) < len(file_paths):
        formats.extend(["ogip" for _ in range(len(formats), len(file_paths))])

    try:
        loaded_files = []
        loop = asyncio.get_event_loop()
        for file_path, file_name, file_format in zip(file_paths, filenames, formats):
            event_list = await loop.run_in_executor(
                None, EventList.read, file_path, file_format
            )
            loaded_event_data.append((file_name, event_list))
            loaded_files.append(
                f"File '{file_path}' loaded successfully as '{file_name}' with format '{file_format}'."
            )

            # Save the event list to the loaded-data directory
            save_path = os.path.join(loaded_data_path, f"{file_name}.npz")
            np.savez(
                save_path,
                time=event_list.time,
                gti=event_list.gti,
                mjdref=event_list.mjdref,
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


def create_data_ingestion_tab1():
    file_selector = pn.widgets.FileSelector(
        "/", only_files=True, name="Select File", show_hidden=True
    )
    filename_input = pn.widgets.TextInput(
        name="Enter File Names",
        placeholder="Enter file names, comma-separated",
        width=700,
    )
    format_input = pn.widgets.TextInput(
        name="Enter Formats",
        placeholder="Enter formats (e.g., ogip, pickle, hdf5), comma-separated",
        width=700,
    )
    load_button = pn.widgets.Button(name="Load Event Data", button_type="primary")
    output = pn.widgets.TextAreaInput(
        name="Output", value="", disabled=True, height=200
    )
    warning_output = pn.widgets.TextAreaInput(
        name="Warnings", value="", disabled=True, height=200
    )

    tooltip_format = pn.widgets.TooltipIcon(
        value=Tooltip(
            content="""Specify the correct format (e.g., 'ogip', 'pickle', 'hdf5').<br>For HEASoft-supported missions, use 'ogip'.<br>Using 'fits' directly might cause issues with Astropy tables.""",
            position="bottom",
        )
    )

    tooltip_file = pn.widgets.TooltipIcon(
        value=Tooltip(
            content="""Ensure the file contains at least a 'time' column.""",
            position="bottom",
        )
    )

    def on_click(event):
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
                output,
                warning_output,
            )
        )

    load_button.on_click(on_click)

    tab_content = pn.Column(
        pn.layout.HSpacer(height=40),
        pn.pane.Markdown("# Select Files"),
        pn.Row(filename_input, tooltip_file),
        pn.Row(format_input, tooltip_format),
        file_selector,
        load_button,
        pn.Row(output, warning_output),
    )
    return tab_content


def display_loaded_data(event, output, warning_output, time_limit):
    display_data = []
    if not os.listdir(loaded_data_path):
        output.value = "No files in the loaded-data directory."
        return

    for file_name in os.listdir(loaded_data_path):
        if file_name.endswith(".npz"):
            try:
                file_path = os.path.join(loaded_data_path, file_name)
                data = np.load(file_path)
                time_data = f"Times (first {time_limit}): {data['time'][:time_limit]}"
                mjdref = f"MJDREF: {data['mjdref']}"
                gti = f"GTI: {data['gti']}"
                display_data.append(
                    f"File: {file_name}\n{time_data}\n{mjdref}\n{gti}\n"
                )
            except Exception as e:
                warning_handler.warn(str(e), category=RuntimeWarning)

    if display_data:
        output.value = "\n\n".join(display_data)
    else:
        output.value = "No files in the loaded-data directory."

    if warning_handler.warnings:
        warning_output.value = "\n".join(warning_handler.warnings)
    else:
        warning_output.value = "No warnings."

    warning_handler.warnings.clear()


def delete_selected_files(event, file_selector, output):
    if not file_selector.value:
        output.value = "No file selected. Please select a file to delete."
        return

    file_paths = file_selector.value
    deleted_files = []
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        try:
            os.remove(os.path.join(loaded_data_path, file_name))
            deleted_files.append(f"File '{file_name}' deleted successfully.")
        except Exception as e:
            deleted_files.append(f"An error occurred while deleting '{file_name}': {e}")

    output.value = "\n".join(deleted_files)


def create_data_ingestion_tab2():
    display_button = pn.widgets.Button(
        name="Display Loaded Data", button_type="primary"
    )
    time_limit_input = pn.widgets.IntInput(
        name="No of time intervals", value=10, start=1
    )
    display_output = pn.widgets.TextAreaInput(
        name="Loaded Data", value="", disabled=True, height=400
    )
    display_warning_output = pn.widgets.TextAreaInput(
        name="Warnings", value="", disabled=True, height=200
    )

    display_button.on_click(
        lambda event: display_loaded_data(
            event, display_output, display_warning_output, time_limit_input.value
        )
    )

    delete_file_selector = pn.widgets.FileSelector(
        loaded_data_path,
        only_files=True,
        name="Select File to Delete",
        show_hidden=True,
    )
    delete_button = pn.widgets.Button(
        name="Delete Selected Files", button_type="danger"
    )
    delete_output = pn.widgets.TextAreaInput(
        name="Delete Output", value="", disabled=True, height=200
    )

    delete_button.on_click(
        lambda event: delete_selected_files(event, delete_file_selector, delete_output)
    )

    tab_content = pn.Column(
        pn.layout.HSpacer(height=40),
        pn.Row(
            pn.Column(
                pn.pane.Markdown("# Preview Files"),
                display_button,
                time_limit_input,
                display_output,
                display_warning_output,
            ),
            pn.Spacer(width=40),
            pn.Column(
                pn.pane.Markdown("# Delete Files"),
                delete_file_selector,
                delete_button,
                delete_output,
            ),
        ),
    )
    return tab_content


def create_event_list(
    event, times_input, energy_input, gti_input, mjdref_input, name_input, output, warning_output
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
        
        name = name_input.value if name_input.value else ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=7))

        event_list = EventList(times, energy=energy, gti=gti, mjdref=mjdref)

        save_path = os.path.join(loaded_data_path, f"{name}.npz")
        np.savez(
            save_path,
            time=event_list.time,
            gti=event_list.gti,
            mjdref=event_list.mjdref,
            energy=event_list.energy if energy else []
        )

        output.value = f"""
        Event List created successfully!
        Saved as: {name}.npz
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


def create_data_ingestion_tab3():
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
        name="Event List Name (optional)", placeholder="e.g., my_event_list"
    )
    create_button = pn.widgets.Button(name="Create Event List", button_type="primary")
    output = pn.widgets.TextAreaInput(
        name="Event List Output", value="", disabled=True, height=200
    )
    warning_output = pn.widgets.TextAreaInput(
        name="Warnings", value="", disabled=True, height=200
    )

    create_button.on_click(
        lambda event: create_event_list(
            event, times_input, energy_input, gti_input, mjdref_input, name_input, output, warning_output
        )
    )

    tab_content = pn.Column(
        pn.layout.HSpacer(height=40),
        pn.pane.Markdown("# Create Event List"),
        pn.Row(
            pn.Column(
                times_input,
                mjdref_input,
                energy_input,
                gti_input,
                name_input,
                create_button,
            ),
            pn.Spacer(width=40),
            pn.Column(output, warning_output)
        )
    )
    return tab_content


def create_data_ingestion_tab4():
    tab_content = pn.Column(
        pn.pane.Markdown(
            """
            ### Tab 4
            Content not available.
        """
        )
    )
    return tab_content


def create_data_ingestion_tabs():
    tabs = pn.Tabs(
        ("Select File", create_data_ingestion_tab1()),
        ("Display File", create_data_ingestion_tab2()),
        ("Create Event List", create_data_ingestion_tab3()),
        ("Tab 4", create_data_ingestion_tab4()),
    )
    return tabs


# Example usage in your main script (e.g., app.py)
layout = pn.Column(
    pn.pane.Markdown("# Dynamic Tabs Example"), create_data_ingestion_tabs()
)

# Serve the layout
layout.servable()

if __name__ == "__main__":
    pn.serve(layout)
