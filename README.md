# URL Shortening Service

This is a simple URL shortening service built with Flask and SQLAlchemy. It allows you to shorten URLs and redirect to the original URL using a short code.

## Features

- Shorten any valid URL
- Redirect from short URL to the original URL
- Unique short codes for each URL
- Built with Flask, SQLAlchemy, and SQLite for simplicity

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/url-shortening-service.git
   cd url-shortening-service
   ```

2. **Install dependencies:**

   It is recommended to use a virtual environment to install the dependencies. If you don't have `virtualenv` installed, you can install it via pip:

   ```bash
   pip install virtualenv
   virtualenv venv
   source venv/bin/activate   # On Windows, use 'venv\Scripts\activate'
   ```

   Then, install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**

   The SQLite database is created automatically when the app is first run, but you can also manually initialize it by running the following command:

   ```bash
   python app.py
   ```

   This will create the `database.db` file and set up the necessary tables.

4. **Run the application:**

   Start the Flask development server by running:

   ```bash
   python app.py
   ```

   The application will be available at [http://localhost:5000](http://localhost:5000).

## API Endpoints

### 1. **Shorten a URL**

- **Endpoint**: `POST /shorten`
- **Request body**:
  
  ```json
  {
    "url": "http://example.com"
  }
  ```

- **Response**:

  ```json
  {
    "short_url": "http://localhost:5000/abc123"
  }
  ```

  This endpoint will return a shortened URL that can be used to redirect to the original URL.

### 2. **Redirect to the Original URL**

- **Endpoint**: `GET /<short_code>`
  
  Example: `GET /abc123` will redirect to the original URL.

- If the short code doesn't exist, it will return a 404 error:

  ```json
  {
    "error": "Short URL not found"
  }
  ```
  
## Dependencies

- Flask: A micro web framework for Python
- SQLAlchemy: A Python SQL toolkit and ORM for database management
- Validators: A library for URL validation
- SQLite: A lightweight disk-based database that doesn’t require a separate server process