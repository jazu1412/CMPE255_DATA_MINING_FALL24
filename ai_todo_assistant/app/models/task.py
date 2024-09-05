from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum, Float, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum

Base = declarative_base()

class TaskStatus(enum.Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class TaskPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    estimated_time = Column(Float)  # in hours
    deadline = Column(DateTime)
    flexibility = Column(Float)  # flexibility in hours
    completed = Column(Boolean, default=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

engine = create_engine('sqlite:///ai_todo_assistant.db')

def create_or_update_task_table():
    inspector = inspect(engine)
    if not inspector.has_table('tasks'):
        Base.metadata.create_all(engine)
        print("Tasks table created.")
    else:
        columns = inspector.get_columns('tasks')
        column_names = [col['name'] for col in columns]
        
        with engine.connect() as conn:
            if 'title' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN title VARCHAR NOT NULL"))
            if 'description' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN description VARCHAR"))
            if 'priority' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN priority VARCHAR(10)"))
            if 'estimated_time' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN estimated_time FLOAT"))
            if 'deadline' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN deadline DATETIME"))
            if 'flexibility' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN flexibility FLOAT"))
            if 'completed' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN completed BOOLEAN DEFAULT 0"))
            if 'status' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN status VARCHAR(20)"))
            if 'created_at' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
            if 'updated_at' not in column_names:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
            
            conn.commit()
        print("Task table updated successfully.")

create_or_update_task_table()

Session = sessionmaker(bind=engine)
session = Session()