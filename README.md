# AI-Powered Config Scanner: Enhancing Cybersecurity with Gemini

## 1. Overview: Unveiling the AI-Powered Config Scanner

The **AI-Powered Config Scanner** is an web-based application designed to elevate cybersecurity posture by meticulously analyzing configuration files for potential vulnerabilities. Leveraging a sophisticated blend of traditional scanning tools and cutting-edge artificial intelligence, this proof-of-concept tool identifies exposed secrets, sensitive data, and critical misconfigurations across various file formats, including JSON, YAML, INI, and `.env` files.

In today's complex development landscape, configuration files are often overlooked yet can be a goldmine for attackers if not secured. This tool addresses that critical gap by:

*   **Comprehensive Scanning:** Integrating industry-leading open-source tools like **TruffleHog** and **Gitleaks**, alongside a robust **custom regex-based scanner**, to detect a wide array of secret types and misconfigurations.
*   **Intelligent Analysis:** Utilizing a powerful **Large Language Model (LLM)**, powered by **Gemini**, to provide contextual analysis of findings. This AI component doesn't just list issues; it explains *why* they are risks, references established security principles (such as OWASP Top 10), and offers actionable, detailed remediation steps.
*   **User-Centric Design:** Offering a user-friendly web interface for easy file uploads, dynamic selection of scanning engines, and clear presentation of results.

This project showcases a proactive approach to security, combining automated detection with intelligent, human-like reasoning to provide invaluable insights for developers and security professionals.

## 2. A Personal Journey: Combining AI with Cybersecurity (Proof of Concept Disclaimer)

This **AI-Powered Config Scanner** is a testament to my passion for bridging the innovative world of Artificial Intelligence with the critical domain of Cybersecurity. Conceived as a proof-of-concept, this project allowed me to explore and demonstrate how advanced AI capabilities, specifically large language models, can significantly augment traditional security tools to create more intelligent and effective defense mechanisms.

Throughout the development process, **Gemini** (Google's AI model) served as an invaluable collaborator. Gemini helped me to brainstorm initial ideas, refine complex architectural decisions, troubleshoot challenging technical hurdles, and ultimately, transform abstract concepts into this tangible, working application. This collaboration was instrumental in shaping the tool's intelligent analysis capabilities and overall design.

This project represents my commitment to continuous learning and innovation in both AI and cybersecurity, and I believe it clearly illustrates my ability to conceptualize, develop, and deliver impactful solutions at the intersection of these two fields. I am actively seeking opportunities where I can apply and expand these skills to contribute to real-world challenges.

## 3. Getting Started: Setting Up Your SecureConfigAI Environment

This section guides you through setting up the AI-Powered Config Scanner on your local machine, specifically tailored for a Windows 11 environment utilizing WSL (Windows Subsystem for Linux).

### System Requirements

*   **Operating System:** Windows 11
*   **Virtualization:** WSL (Windows Subsystem for Linux) with an Ubuntu distribution (recommended).
*   **Version Control:** Git
*   **Python:** Python 3.11+ (while 3.11 was used during development, newer 3.x versions should also be compatible).
*   **Networking Tool:** `curl` (typically pre-installed on Ubuntu/WSL).

### Installation Steps

Follow these steps to get the project up and running:

#### Step 1: Clone the Repository

First, open your WSL (Ubuntu) terminal and clone the project repository from GitHub:

git clone https://github.com/rodneystanley2025/SecureConfigAI.git
cd SecureConfigAI


#### Step 2: Set Up Python Virtual Environment

It's highly recommended to use a Python virtual environment to manage dependencies and avoid conflicts with your system's Python packages.

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Python Dependencies

Install all required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

#### Step 4: Install TruffleHog CLI

TruffleHog is a powerful secret scanning tool. Install its CLI binary directly into your virtual environment's `bin` directory:

```bash
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b venv/bin
```

#### Step 5: Install Gitleaks CLI

Gitleaks is another essential secret scanning tool. Install its CLI binary by running the following commands, which automatically download the latest version for your architecture:

```bash
LATEST_GITLEAKS_VERSION=$(curl -s "https://api.github.com/repos/gitleaks/gitleaks/releases/latest" | grep -Po '"tag_name": "\K(v[0-9\.]+)')
GITLEAKS_URL="https://github.com/gitleaks/gitleaks/releases/download/${LATEST_GITLEAKS_VERSION}/gitleaks_${LATEST_GITLEAKS_VERSION#v}_linux_x64.tar.gz"
curl -LO $GITLEAKS_URL
tar -xzf gitleaks_*.tar.gz
mv gitleaks venv/bin/
rm gitleaks_*.tar.gz
```

*(Note: These commands are for Linux x64. If you are on a different architecture, you will need to adjust the URL accordingly. You can check the [Gitleaks GitHub Releases page](https://github.com/gitleaks/gitleaks/releases) for the correct URL.)*

#### Step 6: Configure Gemini API Key

The AI analysis component requires a Google Gemini API Key.

1.  Create a `.env` file in the root of your `SecureConfigAI` directory.
2.  Add your Gemini API key to this file:

    ```
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
    ```

    *(Replace `YOUR_GEMINI_API_KEY_HERE` with your actual key obtained from the Google AI Studio.)*

## 4. Running SecureConfigAI: Scan, Analyze, and Secure

Once all dependencies are installed and configured, you're ready to launch the application.

### Starting the Application

From your project's root directory in the WSL terminal, execute the `run.sh` script:

./run.sh

Alternatively, in a Powershell terminal, navigate to the project directory and run .\run.bat

This script will activate the virtual environment and start the FastAPI server using Uvicorn. You should see output indicating that the server is running, typically on `http://0.0.0.0:8001`.

### Accessing the Web Interface

Open your web browser and navigate to:

http://127.0.0.1:8000 (or the port shown in the output)


You will be greeted by the AI-Powered Config Scanner's user interface.

### Performing a Scan

1.  **Select a Configuration File:** Click "Choose File" and select any configuration file (`.env`, `.yaml`, `.json`, `.ini`, etc.) you wish to scan.
2.  **Choose Scan Engines:** In the "Scan Engine Settings" section, you can enable or disable various scanning engines. Each engine contributes uniquely to the analysis:
    *   **TruffleHog:** (Recommended) A powerful tool for detecting high-entropy secrets and over 700 types of credentials across various services.
    *   **Gitleaks:** (Recommended) Utilizes a comprehensive set of regex patterns to identify secrets based on known patterns and rule sets.
    *   *(Implicitly always active is your custom regex-based scanner, which is effective for custom patterns and common weak defaults like 'root' passwords in specific contexts.)*
    *   **Recommendation:** For the most thorough analysis, it is recommended to enable both TruffleHog and Gitleaks.
3.  **Initiate Scan:** Click the "Scan File" button. The file will be uploaded, and the scan will be queued as a background task.
4.  **View Results:** The "Scan History" section will update with your new scan. Click on a scan entry to expand it and view:
    *   **Tool Findings:** Raw findings from the active scanning engines, detailing detected secrets or misconfigurations.
    *   **AI Analysis:** A comprehensive, human-readable analysis generated by the Gemini LLM. This includes an overall security posture, detailed risk explanations (often referencing OWASP principles), and actionable remediation steps.

## 5. Contributing & Feedback: Shape the Future of SecureConfigAI

Your input and contributions are highly valued! This project is an ongoing exploration into advanced cybersecurity solutions, and community involvement can help it grow.

### How to Contribute

*   **Bug Reports:** If you encounter any issues or unexpected behavior, please open an issue on the GitHub repository, providing detailed steps to reproduce the problem.
*   **Feature Requests:** Have an idea for a new feature or an improvement? Feel free to suggest it by opening an issue on GitHub.
*   **Code Contributions:** Fork the repository, make your changes, and submit a pull request. All contributions are welcome!

### Sending Feedback

For any direct feedback, questions, or just to connect, please feel free to reach out to me:

**Email:** `rodney_stanley@hotmail.com`

Constructive criticism and suggestions are always appreciated as I continue to develop and refine this tool.

## 6. Important Notes & Future Enhancements

### Proof of Concept Disclaimer

This **AI-Powered Config Scanner** is a proof-of-concept project developed to demonstrate the synergistic potential of AI and traditional security tooling in configuration analysis. While built with best practices in mind, it is intended for educational and demonstrative purposes, and should not be used as a sole security solution in production environments without further development, hardening, and rigorous testing.

### Future Enhancements

*   **Secret Validation:** Implement real-time verification of detected secrets against their respective services (e.g., check if an AWS key is active).
*   **Custom Rule Management:** Provide a user interface to allow users to define, save, and manage their own custom regex rules for the scanner.
*   **Benchmarking Suite:** Develop a robust benchmarking framework to measure the scanner's performance (speed, resource usage) and effectiveness (recall, precision) against a diverse dataset of configuration files.
*   **Gitleaks/TruffleHog Configuration:** Explore more advanced configuration options for integrated tools, such as custom rules for Gitleaks or fine-tuning TruffleHog's detection.
*   **Expanded File Type Support:** Integrate more parsers for additional configuration file formats (e.g., TOML).

### License

This project is open-sourced under the [MIT License](https://opensource.org/licenses/MIT).