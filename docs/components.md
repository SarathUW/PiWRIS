### PyWRIS Components

#### 1. **Authentication**
   - **Functionality:** Manages authentication if India WRIS requires credentials, handling token generation, saving, and renewal.
   - **Inputs:** Username and password, or API keys (if provided by WRIS).
   - **Outputs:** Authentication token or session cookies.
   - **Usage:** Use this component to start a session before data download if required.
   - **Side Effects:** Temporary storage of tokens/cookies; sensitive info should be encrypted to ensure security.
