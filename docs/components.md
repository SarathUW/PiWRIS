### PyWRIS Components

#### 1. **Authentication**
   - **Functionality:** Manages authentication if India WRIS requires credentials, handling token generation, saving, and renewal.
   - **Inputs:** Username and password, or API keys (if provided by WRIS).
   - **Outputs:** Authentication token or session cookies.
   - **Usage:** Use this component to start a session before data download if required.
   - **Side Effects:** Temporary storage of tokens/cookies; sensitive info should be encrypted to ensure security.

#### 2. **Data Download**
   - **Functionality:** Fetches hydrology datasets (e.g., rainfall, groundwater levels, reservoir data) based on filters like date range, state, and basin.
   - **Inputs:** Data type (e.g., rainfall, groundwater), date range, spatial filters (e.g., state or basin).
   - **Outputs:** Data in Pandas DataFrame format with metadata, if any.
   - **Usage:** Users specify parameters to retrieve the requested dataset.
   - **Side Effects:** Large downloads (like raster data) may take time or exceed request limits if the server restricts requests.

