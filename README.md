# letsplay - in dev

letsplay is a minimal web app that teaches prompt engineering through task-based challenges. Users are given specific output goals (e.g., "Make the model return only 'hello'") and must craft prompts to achieve them. Responses are evaluated and scored for accuracy.

Built with Gradio and Hugging Face Transformers. No login required. Designed as a one-time, browser-based educational tool.

## Features

- Prompt-based challenge tasks
- Real-time model output via Hugging Face Inference API or local pipeline
- Automated scoring logic
- Stateless multiplayer via shared session link (optional)
