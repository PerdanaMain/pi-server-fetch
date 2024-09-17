from app import app
from app.controllers.fetch_controller import index
import os
import threading

if __name__ == "__main__":
  # background_thread = threading.Thread(target=index)
  # background_thread.daemon = True
  # background_thread.start()
  app.run(debug=True, port=os.getenv("APP_PORT", 5000),host="0.0.0.0")