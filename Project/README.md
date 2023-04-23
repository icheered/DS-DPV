# Project: Time table insights

## Folder Structure

The project consists of the following folders and files:

- `data`: This folder contains the raw and processed data used in the project. The data is organized by the institution where it was collected, with subfolders for each institution. For example, the `saxion` subfolder contains the original unprocessed data and processed data for Saxion.
- `intermediate`: This folder contains intermediate files generated during the project, such as files derived from the original data containing only the data of interest for a specific question.
- `rawdata`: This folder contains the original unprocessed data for each institution.
- `src`: This folder contains the source code used in the project. The source code is organized by function, with subfolders for preprocessing and visualization.
  - `preprocess`: This folder contains the scripts used to preprocess the data for each institution. There is a separate script for each institution, named `preprocess_saxion.py` and `preprocess_utwente.py`.
  - `visualize`: This folder contains the scripts used to visualize the data for each institution. There is a separate script for each institution, named `saxion.py` and `utwente.py`. The `utils` subfolder contains helper functions for loading data, `data_loading.py`, and specific utility functions for `utwente.py` named `utwente_utils.py`.
