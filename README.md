---

# 📊 Tableau Server Subscription Cleanup Script

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.3%2B-green.svg)
![Tableau Server Client](https://img.shields.io/badge/Tableau%20Server%20Client-0.15%2B-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

## 🛠️ Overview

This script is designed to automate the cleanup of subscriptions on Tableau Server. It connects to the Tableau Server, fetches all subscriptions across specified sites, and removes subscriptions based on predefined criteria. Additionally, it performs housekeeping tasks by deleting old log files that are more than 10 days old.

## 🚀 Features

- **Log Management**: Automatically deletes log files older than 10 days to free up space.
- **Subscription Cleanup**: Identifies and removes subscriptions across Tableau sites with detailed logging of operations.
- **Data Export**: Saves a record of all deleted subscriptions in an Excel file for auditing purposes.
- **Error Handling**: Robust logging and error handling ensure smooth execution.

## 📦 Prerequisites

- Python 3.8+
- Pandas
- Tableau Server Client Library (`tableauserverclient`)
- Basic knowledge of Tableau Server and its subscription management

## 📝 Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/swapnilyavalkar/Tableau-Delete-Subscriptions.git
   cd Tableau-Delete-Subscriptions
   ```

2. **Install Dependencies**:
   ```bash
   pip install pandas tableauserverclient
   ```

3. **Configure the Script**:
   - Update the `server_url`, `username`, `password`, and `sites` variables with your Tableau Server details.
   - Adjust the `directory_path` and `threshold_time` if needed.

## 🖥️ Usage

Run the script to perform the cleanup:

```bash
python main.py
```

### Example Output

- Logs will be generated in the `logs/` directory.
- Deleted subscription details will be saved in `data/df_all_subscriptions.xlsx`.

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/swapnilyavalkar/Tableau-Delete-Subscriptions/issues) or open a pull request.

---
