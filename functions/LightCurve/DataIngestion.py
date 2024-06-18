import panel as pn
from utils.ingest import DataIngestion
import os

# Initialize Panel extension
pn.extension()

def create_data_ingestion_tab():
    # Define variables
    filename = None
    data_ingestion = None
    detector_added = False

    # Function to handle detector information addition
    def handle_add_detector(event):
        nonlocal data_ingestion, detector_added
        detector_ids = detector_input.value.split(",")
        try:
            detector_ids = [int(det_id.strip()) for det_id in detector_ids]
            data_ingestion.add_detector_information(detector_ids)
            confirmation_text.object = "Detector information added successfully."
            detector_added = True  # Set flag to indicate detector info is added
        except ValueError as ve:
            confirmation_text.object = str(ve)

    # Function to handle file upload and processing
    def handle_file_upload(event):
        nonlocal filename, data_ingestion, detector_added
        # if not detector_added:
        #     confirmation_text.object = "Please add detector information first."
        #     return

        file_path = event.new
        filename = os.path.basename(file_path)

        # Check if the file path exists and is a file
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Initialize DataIngestion object
            data_ingestion = DataIngestion(file_path)

            # Load events from the file
            try:
                data_ingestion.load_events(additional_columns=["DET_ID"])
                # Display confirmation message
                confirmation_text.object = f"Successfully loaded events from {filename}"
            except Exception as e:
                confirmation_text.object = f"Error loading events from {filename}: {str(e)}"
        else:
            confirmation_text.object = f"File '{filename}' does not exist or is not a valid file."

    # Function to display first few elements of the loaded file
    def display_first_elements(event):
        nonlocal data_ingestion
        if data_ingestion and data_ingestion.events is not None:
            # Display first few elements
            first_elements_text.object = str(data_ingestion.events[:5])  # Assuming events support slicing
        else:
            first_elements_text.object = "No events loaded yet. Please load a file first."

    # Create widgets
    upload_button = pn.widgets.FileInput(
        accept=".fits,.txt,.npy,.evt,.evt.gz",
        name="Upload File",
        sizing_mode="stretch_width"
    )
    upload_button.param.watch(handle_file_upload, "value")

    confirmation_text = pn.pane.Markdown("")
    display_button = pn.widgets.Button(name="Display First Elements")
    display_button.on_click(display_first_elements)
    first_elements_text = pn.pane.Str()

    detector_input = pn.widgets.TextInput(placeholder="Enter comma-separated detector IDs")
    add_detector_button = pn.widgets.Button(name="Add Detector Information")
    add_detector_button.on_click(handle_add_detector)

    # Layout for data ingestion tab
    tab_content = pn.Column(
        "### Data Ingestion",
        "Add Detector Information:",
        detector_input,
        add_detector_button,
        pn.layout.Divider(),
        upload_button,
        confirmation_text,
        display_button,
        first_elements_text,
        sizing_mode="stretch_width"
    )

    tab = pn.Column(tab_content, name="Data ingestion")
    return tab
