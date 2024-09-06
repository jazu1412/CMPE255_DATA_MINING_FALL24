
from app.database import init_db, get_session
from app.models.task import Task, TaskStatus

def test_database():
    init_db()
    session = get_session()
    
    # Try to create a task
    new_task = Task(
        title="Test Task",
        description="This is a test task",
        priority="High",
        estimated_time=30,
        status=TaskStatus.TODO
    )
    session.add(new_task)
    session.commit()
    
    # Try to query tasks
    tasks = session.query(Task).all()
    print(f"Number of tasks: {len(tasks)}")
    for task in tasks:
        print(f"Task: {task.title}, Status: {task.status}")

if __name__ == "__main__":
    test_database()
