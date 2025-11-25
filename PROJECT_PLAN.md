# AI Scanner Project Plan

This document outlines the development plan, core architectural decisions, and task breakdown for the AI-Powered Configuration Scanner project.

## 1. Core Decision: Local vs. Online AI Model

This is the most critical decision and impacts cost, security, and performance. Here’s a breakdown to address your concerns:

| Feature | Online Model (e.g., Google Gemini API) | Local Model (e.g., Llama 3, Mistral via Ollama) |
| :--- | :--- | :--- |
| **Cost** | **Potential cost per API call.** However, many services like Google's AI Platform have a generous **free tier** that is more than enough for development and testing. | **No cost per call.** The only cost is the electricity to run your hardware. |
| **Security** | Data (the config file contents) is sent to a third-party service for analysis. While connections are secure, the data leaves your machine. | **Maximum security.** All data and analysis remain on your local machine. Nothing is ever sent over the internet. |
| **Performance** | State-of-the-art reasoning and instruction-following capabilities. Significantly more powerful and accurate. | Performance is limited by your hardware (CPU/GPU, VRAM). Smaller models may struggle with complex reasoning tasks. |
| **Setup** | Very easy. Import a library, get an API key, and you're ready to make calls. | Can be complex. Requires installing tools like Ollama or LM Studio, downloading multi-gigabyte model files, and managing hardware resources. |

### **Recommendation: Hybrid Approach**

1.  **Start with an Online Model on a Free Tier.** For the development and testing phase, we should use the Gemini API. The free tier is designed for this purpose and will prevent any costs while giving us access to a powerful model to build our logic against.
2.  **Build for Abstraction.** We will design the "Orchestrator" component in a way that the AI model is a swappable component.
3.  **Evaluate a Local Model Later.** Once the application is fully functional, we can then explore integrating a local model. By that point, we'll have a working system and can easily benchmark if a local model meets the performance and accuracy requirements for this task.

This approach gives us the best of both worlds: no cost and high performance during development, with a clear path to a fully local and secure solution.

## 2. Project Phases & Tasks

Here is a high-level breakdown of the work required.

### Phase 1: Foundation (✓ Complete)
- [x] Set up `AIScanner` project directory.
- [x] Initialize Python virtual environment (`venv`).
- [x] Install core dependencies (`fastapi`, `uvicorn`, `google-generativeai`).
- [x] Create basic FastAPI application and confirm it's running.

### Phase 2: Backend API Development
- [ ] Create a FastAPI endpoint (`POST /scan`) that accepts file uploads.
- [ ] Implement logic to save the uploaded file temporarily for analysis.
- [ ] Create a placeholder endpoint (`GET /scan/{scan_id}`) to eventually retrieve scan results.

### Phase 3: Tool Development
- [ ] Create the first tool: `secret_scanner`. This tool will take file content as input and use regex to find potential secrets.
- [ ] Create a second tool: `file_type_identifier`. This will determine what kind of configuration file was uploaded (e.g., Dockerfile, `.env`).
- [ ] Create a third tool: `yaml_parser`. This will validate and parse YAML files.

### Phase 4: AI Orchestrator & Integration
- [ ] Build the main orchestrator module.
- [ ] Implement logic for the orchestrator to receive a file path.
- [ ] The orchestrator will first use the `file_type_identifier` tool.
- [ ] Based on the file type, it will then decide which other tools to call (e.g., for a YAML file, it would call `secret_scanner` and `yaml_parser`).
- [ ] Integrate the orchestrator with the Gemini API to make these decisions and analyze the tool outputs.

### Phase 5: Frontend Development
- [ ] Create a simple `index.html` file.
- [ ] Add a file upload form to the HTML.
- [ ] Write JavaScript to handle the form submission, send the file to the `/scan` endpoint, and poll for results.
- [ ] Display the results returned from the AI in a user-friendly format on the page.

## 3. Leveraging the Existing 'SecureConfigAI' Project

We don't have to start everything from scratch. We can strategically reuse assets from the old project.

### What to Reuse:
-   **Scanning Logic & Rules:** The `SecureConfigAI/scan_engine/data/rules.json` file is a goldmine. It contains the regular expressions and patterns for detecting a wide variety of secrets and misconfigurations. We can directly port this logic into our new Python-based tools.
-   **Frontend UI:** The HTML, CSS, and JavaScript from the old Flask templates can be adapted for our new, simple frontend. The file upload UI is likely reusable.
-   **Test Files:** The old project has numerous test configuration files (e.g., `test.yaml`, `.env.example`). These are perfect for testing our new scanner.

### What to Leave Behind:
-   **Application Architecture:** We are intentionally leaving the Flask, Celery, and Redis architecture behind in favor of a simpler, single FastAPI application for now.
-   **Database Models:** We will not use the old database structure. For now, we will perform scans in-memory and return results directly. We can consider adding a database later if we need to store scan history.

## 5. Future Enhancements

-   **Retrieval-Augmented Generation (RAG):** Integrate a knowledge base of security best practices and vulnerability information. The AI Orchestrator would retrieve relevant documents and use them to augment its analysis and reporting, leading to more accurate, detailed, and context-aware security reports. This would involve:
    -   Building a knowledge base of security documents.
    -   Implementing a vector database and embedding models for efficient retrieval.
    -   Modifying the AI Orchestrator to perform retrieval before generating reports.



curl -X POST -F "file=@test_config.txt" http://localhost:8000/scan

AIzaSyD5HQabGpB1CY7DmRvJZoSigo0PYeXokgY

