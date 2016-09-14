import os
import sys
from app import app
from flask_script import Manager, Server


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=int(os.environ.get('PORT', 5000)))
)

if __name__ == "__main__":
    manager.run()
