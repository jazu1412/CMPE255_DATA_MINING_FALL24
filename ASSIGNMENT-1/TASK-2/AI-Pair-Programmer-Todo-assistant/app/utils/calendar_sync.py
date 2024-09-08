from datetime import datetime, timedelta

def sync_calendar_events(calendar_events):
    """
    Synchronize calendar events with the task planner.
    
    :param calendar_events: List of calendar events from external calendar
    :return: List of synchronized events
    """
    synced_events = []
    
    for event in calendar_events:
        start_time = datetime.fromisoformat(event['start'])
        end_time = datetime.fromisoformat(event['end'])
        
        synced_events.append({
            'title': event['summary'],
            'start_time': start_time.strftime('%H:%M'),
            'end_time': end_time.strftime('%H:%M'),
            'type': 'calendar_event',
            'id': event['id']
        })
    
    return synced_events

def check_conflicts(tasks, calendar_events):
    """
    Check for conflicts between tasks and calendar events.
    
    :param tasks: List of tasks
    :param calendar_events: List of calendar events
    :return: List of conflicts
    """
    conflicts = []
    
    for task in tasks:
        task_start = datetime.strptime(task['start_time'], '%H:%M')
        task_end = datetime.strptime(task['end_time'], '%H:%M')
        
        for event in calendar_events:
            event_start = datetime.strptime(event['start_time'], '%H:%M')
            event_end = datetime.strptime(event['end_time'], '%H:%M')
            
            if (task_start < event_end and task_end > event_start):
                conflicts.append({
                    'task': task,
                    'event': event,
                    'type': 'overlap'
                })
    
    return conflicts

def suggest_reschedule(task, conflicts, available_slots):
    """
    Suggest rescheduling options for conflicting tasks.
    
    :param task: The task to reschedule
    :param conflicts: List of conflicts
    :param available_slots: List of available time slots
    :return: List of rescheduling suggestions
    """
    suggestions = []
    task_duration = datetime.strptime(task['end_time'], '%H:%M') - datetime.strptime(task['start_time'], '%H:%M')
    
    for slot in available_slots:
        slot_duration = datetime.strptime(slot['end_time'], '%H:%M') - datetime.strptime(slot['start_time'], '%H:%M')
        if slot_duration >= task_duration:
            suggestions.append({
                'task': task,
                'new_start_time': slot['start_time'],
                'new_end_time': (datetime.strptime(slot['start_time'], '%H:%M') + task_duration).strftime('%H:%M')
            })
    
    return suggestions