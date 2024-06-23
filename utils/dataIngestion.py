import panel as pn
from stingray.events import EventList
import asyncio
import warnings
from bokeh.models import Tooltip

# Initialize Panel extension
pn.extension()


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
        pn.Row(filename_input, tooltip_file),
        pn.Row(format_input, tooltip_format),
        file_selector,
        load_button,
        pn.Row(output, warning_output),
    )
    return tab_content


def create_data_ingestion_tab2():
    tab_content = pn.Column(
        pn.pane.Markdown(
            """
            ### Tab 2
            Content not available.
        """
        )
    )
    return tab_content


def create_data_ingestion_tab3():
    tab_content = pn.Column(
        pn.pane.Markdown(
            """
            ### Tab 3
            Content not available.
        """
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
        ("Tab 2", create_data_ingestion_tab2()),
        ("Tab 3", create_data_ingestion_tab3()),
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
