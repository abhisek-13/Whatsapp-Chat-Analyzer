# WhatsApp Chat Analyzer

## Overview
The WhatsApp Chat Analyzer is a data analysis project designed to provide insights into both individual and group WhatsApp chats. This tool analyzes chat data to provide various metrics such as the number of lines, most used letter, chatting duration on a daily, monthly, and yearly basis, media files shared, most used emojis, and group member activity. The results are displayed on a dashboard interface built with Streamlit, making it easy to visualize and interact with the analysis.

## Features
- **Individual Chat Analysis:** Analyze individual chats to get detailed metrics.
- **Group Chat Analysis:** Analyze group chats to understand group dynamics and individual participation.
- **Chat Metrics:**
  - Number of lines of chat
  - Most used letter
  - Chatting duration (daily, monthly, yearly)
  - Number of media files shared
  - Most used emojis
  - Most active group member
- **Streamlit Dashboard:** A user-friendly dashboard to showcase chat analysis with interactive visualizations.

## Technologies Used
- **Python:** Programming language used for data analysis and model development.
- **Streamlit:** Framework for building the dashboard interface.
- **Pandas:** Library for data manipulation and analysis.
- **Matplotlib/Seaborn:** Libraries for data visualization.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
    cd whatsapp-chat-analyzer
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Export your WhatsApp chat as a text file and place it in the `data/` directory.
2. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
3. Open the provided local URL in your web browser.
4. Use the dashboard to upload your chat file and view the analysis.

## Project Structure
- `app.py`: Main application file for running the Streamlit interface.
- `requirements.txt`: List of dependencies required to run the project.

## How to Use
1. Open the application in your browser.
2. Upload your WhatsApp chat text file using the provided interface.
3. Select whether you want to analyze an individual chat or a group chat.
4. View the analysis on the dashboard, including various metrics and visualizations.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any questions or feedback, please contact [abhisekmaharana9861@gmail.com](abhisekmaharana9861@gmail.com).
