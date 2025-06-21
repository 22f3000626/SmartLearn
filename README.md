# SmartLearn - AI-Powered Learning Platform

SmartLearn is a comprehensive AI-powered learning platform that combines social learning communities, AI-driven content recommendation, automated learning path generation, and multimedia resource aggregation.

## Features

- 🤖 **AI-Powered Learning**: Intelligent content recommendations and personalized learning paths
- 👥 **Learning Communities**: Join communities, share knowledge, and collaborate with other learners
- 📚 **Multi-Source Content**: Videos, books, PDFs, and community-generated content
- 🎯 **Personalized Roadmaps**: AI-generated step-by-step learning paths
- 🔍 **Smart Video Search**: AI-filtered YouTube content recommendations with pagination
- ⚡ **Load More Videos**: Dynamically load additional videos without page refresh
- 📊 **Real-time Video Stats**: View counts, duration, and engagement metrics

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SmartLearn
   ```

2. **Install dependencies**
   ```bash
   pip install -r newreqirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   # Copy the template and modify as needed
   cp env_template.txt .env
   ```

4. **Run the application**
   ```bash
   # Option 1: Use the startup script (recommended)
   python run.py
   
   # Option 2: Run directly
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to: http://localhost:5000
   - Create an account and start learning!

## Configuration

### Environment Variables

You can configure the application using environment variables. See `env_template.txt` for available options:

- `ENABLE_AI_CLASSIFICATION`: Enable/disable AI content classification (default: true)
- `ENABLE_OLLAMA`: Enable/disable Ollama integration for roadmap generation (default: true)
- `DATABASE_URL`: Database connection string (default: SQLite)
- `LOG_LEVEL`: Logging level (default: INFO)

### Database Configuration

**SQLite (Default)**
- No additional setup required
- Database file: `instance/smartlearn.db`

**PostgreSQL (Optional)**
```bash
# Set the database URL
export DATABASE_URL=postgresql://username:password@localhost:5432/smartlearn

# Create the database
createdb smartlearn
```

## Troubleshooting

### Common Issues

1. **Connection Error on Startup**
   - The application tries to download AI models on first run
   - If you have network issues, the app will fall back to basic features
   - Check your internet connection and try again

2. **AI Features Not Working**
   - Ensure you have a stable internet connection
   - AI models are downloaded automatically on first use
   - You can disable AI features by setting `ENABLE_AI_CLASSIFICATION=false`

3. **YouTube Search Not Working**
   - Check your internet connection
   - YouTube API may have rate limits
   - The app will show an error message if the service is unavailable

4. **Database Errors**
   - Ensure you have write permissions in the project directory
   - For PostgreSQL, check your database connection settings
   - Try deleting the database file and restarting (SQLite only)

### Dependency Issues

If you encounter dependency-related errors:

```bash
# Update pip
python -m pip install --upgrade pip

# Install dependencies with verbose output
pip install -r newreqirements.txt -v

# If specific packages fail, try installing them individually
pip install flask
pip install yt-dlp
pip install requests
```

### Running Without AI Features

If you want to run the application without AI features:

1. Set environment variables:
   ```bash
   export ENABLE_AI_CLASSIFICATION=false
   export ENABLE_OLLAMA=false
   ```

2. Or modify the `.env` file:
   ```
   ENABLE_AI_CLASSIFICATION=false
   ENABLE_OLLAMA=false
   ```

## Project Structure

```
SmartLearn/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── models.py              # Database models
├── extensions.py          # Flask extensions
├── run.py                 # Startup script
├── routes/                # Route handlers
│   ├── mainroutes.py      # Main application routes
│   └── communityroutes.py # Community features
├── services/              # Business logic services
│   ├── youtubescrapper.py # YouTube content scraping
│   ├── roadmap.py         # Learning path generation
│   ├── booksearch.py      # Book recommendations
│   └── bookspdf.py        # PDF resource search
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS, images)
└── migrations/            # Database migrations
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Look at the application logs for error details
3. Create an issue in the repository with:
   - Your operating system
   - Python version
   - Error message
   - Steps to reproduce the issue