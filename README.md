# Chatbot RAG: A Document-Based Chat System

Welcome to the Chatbot project! This web application allows users to upload their own documents and interact with them through a chat interface. Each user's documents are securely managed and kept separate from others. The system leverages Django, PostgreSQL vector database, and OpenAI APIs for embeddings and LLM capabilities.

## Features

### Authentication System
- User login and signup functionality.
- Secure authentication using Django's built-in auth module.

### Document Upload
- Users can upload their own documents.
- Each user's documents are stored and managed separately.

### Chat Module
- Users can interact with their uploaded documents through a chat interface.
- Queries are processed using OpenAI embeddings and LLM APIs.

### Vector Database
- Uses PostgreSQL vector database for efficient document embedding and retrieval.

### Dockerized Deployment
- Fully configured with Docker for easy setup and deployment.

## Tech Stack

- **Backend**: Django
- **Database**: PostgreSQL (vector database enabled)
- **LLM Integration**: OpenAI embeddings and LLM API
- **Containerization**: Docker

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.
- OpenAI API key for embedding and LLM functionalities.
- PostgreSQL with vector extension installed.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/qamarsatti/chatbot.git
   cd chatbot
   ```

2. Set up the environment variables:
   - Create a `.env` file in the root directory.
   - Use the following template for your `.env` file:
     ```env
     OPENAI_API_KEY=your_openai_key

     SECRET_KEY=your_django_secure_key
     DEBUG=True
     ALLOWED_HOSTS=*
     CSRF_TRUSTED_ORIGINS=http://localhost

     # Enable Postgres
     DB_NAME=chatbot_db
     DB_USER=postgres
     DB_PASSWORD=your_password
     DB_HOST=chatdb
     DB_PORT=5432
     ```
     > **Note**: Keep your credentials private and secure. Do not share or commit the `.env` file to version control systems.

3. Build and run the application with Docker:
   ```bash
   docker-compose up --build
   ```

4. Access the application in your browser:
   - Visit [http://localhost:8000](http://localhost:8000).



## Usage

1. **Sign Up and Login**: Create an account or log in using your credentials.
2. **Upload Documents**: Upload documents through the interface.
3. **Chat**: Interact with your uploaded documents via the chat module.

## File Structure

```plaintext
chatbot/
├── app/                # Django application folder
|__ chatbot/
├── docker/             # Docker configurations
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker Compose file
├── README.md           # Project documentation
└── env.example        # Example environment variables file
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or support, please reach out to **qamarsatti**.

Happy chatting with your documents! 🚀
