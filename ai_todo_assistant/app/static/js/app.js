document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('task-form');
    const generatePlanBtn = document.getElementById('generate-plan-btn');
    const wakeUpInput = document.getElementById('wake-up-input');
    const planList = document.getElementById('plan-list');
    const taskList = document.getElementById('tasks');

    function updateTaskStats() {
        fetch('/get_stats')
            .then(response => response.json())
            .then(data => {
                animateValue('total-tasks', data.total_tasks);
                animateValue('completed-tasks', data.completed_tasks);
                animateValue('high-priority-tasks', data.high_priority);
            });
    }

    function animateValue(id, value) {
        const obj = document.getElementById(id);
        const current = parseInt(obj.innerHTML);
        const duration = 1000;
        const start = Date.now();

        const step = () => {
            const elapsed = Date.now() - start;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = Math.floor(current + progress * (value - current));
            obj.innerHTML = currentValue;

            if (progress < 1) {
                requestAnimationFrame(step);
            }
        };

        requestAnimationFrame(step);
    }

    function updateTaskList() {
        fetch('/get_tasks')
            .then(response => response.json())
            .then(data => {
                taskList.innerHTML = '';
                data.tasks.forEach(task => {
                    const taskItem = createTaskItem(task);
                    taskList.appendChild(taskItem);
                    setTimeout(() => taskItem.classList.add('fade-in'), 10);
                });
            });
    }

    function createTaskItem(task) {
        const item = document.createElement('li');
        item.className = 'task-item';
        item.dataset.taskId = task.id;
        item.innerHTML = `
            <h4>${task.title}</h4>
            <p>Priority: ${task.priority}</p>
            <p>Estimated Time: ${task.estimated_time} hours</p>
            <p>Deadline: ${task.deadline ? new Date(task.deadline).toLocaleString() : 'Not set'}</p>
            <p>Flexibility: ${task.flexibility} hours</p>
            <button class="complete-task-btn" data-task-id="${task.id}">Complete</button>
            <button class="delete-task-btn" data-task-id="${task.id}">Delete</button>
        `;
        return item;
    }

    updateTaskStats();
    updateTaskList();

    taskForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(taskForm);
        const taskData = {
            title: formData.get('title').trim(),
            description: formData.get('description').trim(),
            priority: formData.get('priority'),
            estimated_time: parseFloat(formData.get('estimated_time')) || null,
            deadline: formData.get('deadline') ? new Date(formData.get('deadline')).toISOString() : null,
            flexibility: parseFloat(formData.get('flexibility')) || null
        };

        // Validate required fields
        if (!taskData.title || !taskData.priority) {
            alert('Please fill in all required fields (Title and Priority)');
            return;
        }

        fetch('/add_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                taskForm.reset();
                updateTaskStats();
                updateTaskList();
            } else {
                alert('Error adding task: ' + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    generatePlanBtn.addEventListener('click', function() {
        const wakeUpTime = wakeUpInput.value;
        if (!wakeUpTime) {
            alert('Please set a wake-up time');
            return;
        }

        fetch('/generate_plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ wake_up_time: wakeUpTime })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                planList.innerHTML = '';
                data.plan.forEach(item => {
                    const planItem = document.createElement('li');
                    planItem.innerHTML = `
                        <strong>${item.title}</strong> (${item.priority})
                        <br>
                        ${item.start_time} - ${item.end_time}
                    `;
                    planList.appendChild(planItem);
                    setTimeout(() => planItem.classList.add('slide-in'), 10);
                });
            }
        })
        .catch(error => console.error('Error:', error));
    });

    taskList.addEventListener('click', function(e) {
        if (e.target.classList.contains('complete-task-btn')) {
            const taskId = e.target.dataset.taskId;
            completeTask(taskId);
        } else if (e.target.classList.contains('delete-task-btn')) {
            const taskId = e.target.dataset.taskId;
            deleteTask(taskId);
        }
    });

    function completeTask(taskId) {
        fetch(`/update_task/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: 'DONE', completed: true })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateTaskStats();
                updateTaskList();
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function deleteTask(taskId) {
        if (confirm('Are you sure you want to delete this task?')) {
            fetch(`/delete_task/${taskId}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateTaskStats();
                    updateTaskList();
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }

});

// Add subtle background animation
const canvas = document.createElement('canvas');
document.body.appendChild(canvas);
canvas.style.position = 'fixed';
canvas.style.top = '0';
canvas.style.left = '0';
canvas.style.width = '100vw';
canvas.style.height = '100vh';
canvas.style.zIndex = '-1';
canvas.style.opacity = '0.1';

const ctx = canvas.getContext('2d');
let particlesArray;

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class Particle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.size = Math.random() * 5 + 1;
        this.speedX = Math.random() * 3 - 1.5;
        this.speedY = Math.random() * 3 - 1.5;
    }
    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        if (this.size > 0.2) this.size -= 0.1;
    }
    draw() {
        ctx.fillStyle = '#4a90e2';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function init() {
    particlesArray = [];
    for (let i = 0; i < 100; i++) {
        let x = Math.random() * canvas.width;
        let y = Math.random() * canvas.height;
        particlesArray.push(new Particle(x, y));
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
        particlesArray[i].draw();
        if (particlesArray[i].size <= 0.2) {
            particlesArray.splice(i, 1);
            i--;
            let x = Math.random() * canvas.width;
            let y = Math.random() * canvas.height;
            particlesArray.push(new Particle(x, y));
        }
    }
    requestAnimationFrame(animate);
}

init();
animate();