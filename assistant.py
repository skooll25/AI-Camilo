from flask import Flask, request, jsonify
import datetime
import json

app = Flask(__name__)

class AIAssistant:
    def __init__(self):
        self.tasks = []
        self.reminders = []

    def add_task(self, task_name, due_date):
        task = {
            'task': task_name,
            'due_date': due_date,
            'status': 'pending'
        }
        self.tasks.append(task)
        return {'message': f'Tarea \"{task_name}\" agendada para {due_date}.'}

    def list_tasks(self):
        if not self.tasks:
            return {"message": "No hay tareas pendientes."}
        return {'tasks': self.tasks}

    def mark_task_done(self, task_name):
        for task in self.tasks:
            if task['task'] == task_name:
                task['status'] = 'done'
                return {'message': f'Tarea \"{task_name}\" marcada como completada.'}
        return {'error': f'No se encontró la tarea \"{task_name}\".'}

    def add_reminder(self, reminder_name, remind_date):
        reminder = {
            'reminder': reminder_name,
            'remind_date': remind_date
        }
        self.reminders.append(reminder)
        return {'message': f'Recordatorio \"{reminder_name}\" programado para {remind_date}.'}

    def list_reminders(self):
        if not self.reminders:
            return {"message": "No hay recordatorios programados."}
        return {'reminders': self.reminders}

    def check_reminders(self):
        today = datetime.date.today().isoformat()
        due_reminders = [r for r in self.reminders if r['remind_date'] == today]
        if due_reminders:
            return {'message': f'Tienes {len(due_reminders)} recordatorios para hoy.', 'reminders': due_reminders}
        return {"message": "No hay recordatorios para hoy."}

assistant = AIAssistant()

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    return jsonify(assistant.add_task(data['task_name'], data['due_date']))

@app.route('/list_tasks', methods=['GET'])
def list_tasks():
    return jsonify(assistant.list_tasks())

@app.route('/mark_task_done', methods=['POST'])
def mark_task_done():
    data = request.json
    return jsonify(assistant.mark_task_done(data['task_name']))

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    data = request.json
    return jsonify(assistant.add_reminder(data['reminder_name'], data['remind_date']))

@app.route('/list_reminders', methods=['GET'])
def list_reminders():
    return jsonify(assistant.list_reminders())

@app.route('/check_reminders', methods=['GET'])
def check_reminders():
    return jsonify(assistant.check_reminders())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)   



