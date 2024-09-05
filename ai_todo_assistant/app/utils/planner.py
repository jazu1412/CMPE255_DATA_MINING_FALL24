from datetime import datetime, timedelta
from app.models.task import TaskPriority

def generate_daily_plan(wake_up_time, tasks, calendar_events=[]):
    current_time = datetime.combine(datetime.today(), wake_up_time)
    end_time = current_time.replace(hour=22, minute=0)  # Assume end of day at 10 PM
    plan = []

    # Add calendar events to the plan
    for event in calendar_events:
        plan.append({
            'title': event['title'],
            'start_time': event['start_time'],
            'end_time': event['end_time'],
            'type': 'calendar_event'
        })

    # Sort tasks by priority (High, Medium, Low) and then by deadline
    sorted_tasks = sorted(tasks, key=lambda x: (priority_order(x.priority), x.deadline or datetime.max))

    for task in sorted_tasks:
        task_duration = timedelta(hours=task.estimated_time)
        slot_start = find_free_slot(plan, current_time, end_time, task_duration)
        
        if slot_start:
            plan.append({
                'title': task.title,
                'start_time': slot_start.strftime('%H:%M'),
                'end_time': (slot_start + task_duration).strftime('%H:%M'),
                'priority': task.priority.value,
                'type': 'task',
                'id': task.id
            })
            current_time = slot_start + task_duration

    return sorted(plan, key=lambda x: x['start_time'])

def priority_order(priority):
    order = {TaskPriority.HIGH: 0, TaskPriority.MEDIUM: 1, TaskPriority.LOW: 2}
    return order.get(priority, 3)  # Default to lowest priority if not found

def find_free_slot(plan, start_time, end_time, duration):
    plan_sorted = sorted(plan, key=lambda x: x['start_time'])
    current = start_time

    for item in plan_sorted:
        item_start = datetime.strptime(item['start_time'], '%H:%M').replace(year=start_time.year, month=start_time.month, day=start_time.day)
        if current + duration <= item_start:
            return current
        current = max(current, datetime.strptime(item['end_time'], '%H:%M').replace(year=start_time.year, month=start_time.month, day=start_time.day))

    if current + duration <= end_time:
        return current

    return None

def adjust_plan(current_plan, changes):
    adjusted_plan = current_plan.copy()

    for change in changes:
        if change['type'] == 'move':
            task = next((t for t in adjusted_plan if t['id'] == change['task_id']), None)
            if task:
                new_start = datetime.strptime(change['new_start_time'], '%H:%M')
                task_duration = datetime.strptime(task['end_time'], '%H:%M') - datetime.strptime(task['start_time'], '%H:%M')
                task['start_time'] = new_start.strftime('%H:%M')
                task['end_time'] = (new_start + task_duration).strftime('%H:%M')
        elif change['type'] == 'remove':
            adjusted_plan = [t for t in adjusted_plan if t['id'] != change['task_id']]
        elif change['type'] == 'add':
            new_task = {
                'title': change['title'],
                'start_time': change['start_time'],
                'end_time': change['end_time'],
                'priority': change['priority'],
                'type': 'task',
                'id': change['task_id']
            }
            adjusted_plan.append(new_task)

    return sorted(adjusted_plan, key=lambda x: x['start_time'])