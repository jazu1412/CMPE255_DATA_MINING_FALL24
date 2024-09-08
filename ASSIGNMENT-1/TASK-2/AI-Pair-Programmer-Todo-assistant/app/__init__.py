from flask import Flask, render_template, request, jsonify
from app.models.task import Task, session, TaskStatus, TaskPriority 
from app.utils.planner import generate_daily_plan, adjust_plan
from app.utils.calendar_sync import sync_calendar_events
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    tasks = session.query(Task).all()
    return render_template('index.html', tasks=tasks, TaskStatus=TaskStatus, TaskPriority=TaskPriority)

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    try:
        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            priority=TaskPriority(data['priority']),
            estimated_time=float(data['estimated_time']) if data['estimated_time'] is not None else None,
            deadline=datetime.fromisoformat(data['deadline']) if data['deadline'] else None,
            flexibility=float(data['flexibility']) if data['flexibility'] is not None else None,  
            status=TaskStatus.TODO
        )
        session.add(new_task)
        session.commit()
        return jsonify({'success': True, 'task_id': new_task.id})
    except (KeyError, ValueError) as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json
    wake_up_time = datetime.strptime(data['wake_up_time'], '%H:%M').time()
    print(f"Received wake up time: {wake_up_time}")  # Added logging statement
    tasks = session.query(Task).all()
    daily_plan = generate_daily_plan(wake_up_time, tasks)
    print(f"Generated plan: {daily_plan}")  # Added logging statement
    return jsonify({'success': True, 'plan': daily_plan})

@app.route('/adjust_plan', methods=['POST'])
def adjust_plan_route():
    data = request.json
    current_plan = data['current_plan']
    changes = data['changes']
    adjusted_plan = adjust_plan(current_plan, changes)
    return jsonify({'success': True, 'adjusted_plan': adjusted_plan})

@app.route('/sync_calendar', methods=['POST'])
def sync_calendar():
    data = request.json
    calendar_events = data['calendar_events']
    synced_events = sync_calendar_events(calendar_events)
    return jsonify({'success': True, 'synced_events': synced_events})

@app.route('/get_stats', methods=['GET'])
def get_stats():
    tasks = session.query(Task).all()
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task.status == TaskStatus.DONE])
    high_priority = len([task for task in tasks if task.priority == TaskPriority.HIGH])
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'high_priority': high_priority
    })

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    data = request.json
    task = session.query(Task).get(task_id)
    if task:
        if 'status' in data:
            status = data['status']
            if status == 'DONE':
                status = "Done"
            task.status = TaskStatus(status)
        if 'completed' in data:
            task.completed = data['completed']
            if data['completed']:
                task.status = TaskStatus.DONE
        if 'priority' in data:
            task.priority = TaskPriority(data['priority'])
        if 'estimated_time' in data:
            task.estimated_time = float(data['estimated_time']) if data['estimated_time'] is not None else None
        if 'deadline' in data:
            task.deadline = datetime.fromisoformat(data['deadline']) if data['deadline'] else None
        if 'flexibility' in data:
            task.flexibility = float(data['flexibility']) if data['flexibility'] is not None else None
        session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Task not found'}), 404

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Task not found'}), 404

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    tasks = session.query(Task).all()
    task_list = [
        {
            'id': task.id, 
            'title': task.title,
            'description': task.description,
            'priority': task.priority.value,
            'estimated_time': task.estimated_time,
            'deadline': task.deadline.isoformat() if task.deadline else None,
            'flexibility': task.flexibility,
            'status': task.status.value
        }
        for task in tasks
    ]
    return jsonify({'success': True, 'tasks': task_list})
    
if __name__ == '__main__':
    app.run(debug=True)