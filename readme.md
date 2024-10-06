# E.A.R.T.H. - Environmental Action & Response Through Human-AI Technology

Welcome to the E.A.R.T.H. project! This application allows users to report and visualize environmental issues using AI-powered image analysis and geolocation.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Report environmental issues with location and image upload
- AI-powered image analysis for environmental impact assessment
- Interactive map visualization of reported issues
- Geolocation support for automatic location detection
- Data storage using Supabase

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- A Supabase account and project
- An ipinfo.io API key
- A Google Cloud account with the Gemini API enabled

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/earth-project.git
   cd earth-project
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root and add the following environment variables:
   ```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_project_api_key
   IPINFO_API_KEY=your_ipinfo_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

2. Replace the placeholders with your actual API keys and URLs.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the sidebar to add new environmental reports:
   - Enter a title and description
   - Upload an image of the environmental issue
   - The latitude and longitude will be automatically filled based on your location, but you can adjust them if needed
   - Click "Submit Report" to analyze the image and add the report

4. View the interactive map to see all reported environmental issues.

5. Check the "Recent Reports" section to see the latest submissions.

## Contributing

Contributions to the E.A.R.T.H. project are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/awesome-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add an awesome feature'`)
5. Push to the branch (`git push origin feature/awesome-feature`)
6. Create a new Pull Request

Please make sure to update tests as appropriate and adhere to the project's coding standards.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for your interest in the E.A.R.T.H. project! If you have any questions or issues, please open an issue on the GitHub repository.