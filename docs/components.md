### PyWRIS Use Cases and Components

#### 1. **Authentication**
   - **Functionality:** Manages authentication if India WRIS requires credentials, handling token generation, saving, and renewal.
   - **Inputs:** Username and password, or API keys (if provided by WRIS).
   - **Outputs:** Authentication token or session cookies.
   - **Usage:** Use this component to start a session before data download if required.
   - **Side Effects:** Temporary storage of tokens/cookies; sensitive info should be encrypted to ensure security.

#### 2. **Data Download**
   - **Functionality:** Fetches hydrology related datasets for India (e.g., rainfall, groundwater levels, reservoir data) based on filters like date range, state, and basin.
   - **Inputs:** Data type (e.g., rainfall, groundwater), date range, spatial filters (e.g., state or basin).
   - **Outputs:** Data in Pandas DataFrame format with metadata, if any.
   - **Usage:** Users specify parameters to retrieve the requested dataset.
   - **Side Effects:** Large downloads (like raster data) may take time or exceed request limits if the server restricts requests.

#### 3. WRIS India Database  
   - **What it does**: Provides water related information such as water elevation, discharge for lakes, rivers and reservoirs.  
   - **Inputs**: ID of the reservoir, lake or river, time of interest, variable of interest.  
   - **Outputs**: Gives a timeseries data for the desired parameters
   - **Usage:** Information from this database is automatically retrieved for use in the software

#### 4. Search component  
  - **What it does**: Search within the database with desired parameters  
  - **Inputs**: Time filter component and space filter component, interested variable or dataset (optional)  
  - **Ouptuts**: Outputs number of data points with respect to the requested parameters.
  - **Usage:** User can specify names, dates, regions, and other parameters to limit the scope of the data 



