from flask import Blueprint, request, render_template, redirect, url_for, flash, Response

from app.config import column_labels, ru_ru, ru_ru_more_than_1, ru_ru_1, postfix_schedules, postfix_appointments, \
    postfix_labtest, postfix_prescription, postfix_doctors, postfix_reviews, ru_ru_bullshit
from app.models import db, models, Specialization, Doctor, Patient, Service

bp = Blueprint('common', __name__, template_folder='../templates')

# Данные для авторизации
USERNAME = 'admin'
PASSWORD = 'password123'

# Функция проверки учетных данных
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

# Функция для запроса авторизации
def authenticate():
    return Response(
        'Вы должны войти в систему', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


@bp.route('/')
def index():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    return render_template('index.html', title='Главная')

# база для всех
@bp.route('/<model>')
def list_items(model):
    model_db = models.get(model.lower())
    if not model_db:
        flash(f"Модель '{model}' не найдена!", "error")
        return redirect(url_for('common.index'))

    items = model_db.query.all()
    title = f"Список {ru_ru_more_than_1.get(model, model)}"
    return render_template('list.html', title=title, items=items, column_labels=column_labels)

# Добавление записи
@bp.route('/add/<model>', methods=['GET', 'POST'])
def add(model):
    model_db = models.get(model.lower())
    if not model_db:
        flash('Модель не найдена!', 'error')
        return redirect(url_for('common.index'))

    if request.method == 'POST':
        try:
            record = model_db()

            for field in request.form:
                if hasattr(record, field):
                    setattr(record, field, request.form[field])

            if model.lower() == 'doctor' and 'specialization_id' in request.form:
                specialization = Specialization.query.get(request.form['specialization_id'])
                if specialization:
                    record.specialization_id = specialization.id
                else:
                    flash('Указанная специализация не найдена!', 'error')
                    return redirect(url_for('common.add', model=model))

            if model.lower() in ['schedule', 'appointment', 'review'] and 'doctor_id' in request.form:
                doctor = Doctor.query.get(request.form['doctor_id'])
                if doctor:
                    record.doctor_id = doctor.id
                else:
                    flash('Указанный врач не найден!', 'error')
                    return redirect(url_for('common.add', model=model))

            if model.lower() in ['appointment', 'review'] and 'patient_id' in request.form:
                patient = Patient.query.get(request.form['patient_id'])
                if patient:
                    record.patient_id = patient.id
                else:
                    flash('Указанный призывник не найден!', 'error')
                    return redirect(url_for('common.add', model=model))

            if model.lower() == 'review' and 'service_id' in request.form:
                service = Service.query.get(request.form['service_id'])
                if service:
                    record.service_id = service.id
                else:
                    flash('Указанная услуга не найдена!', 'error')
                    return redirect(url_for('common.add', model=model))

            db.session.add(record)
            db.session.commit()
            flash(f'Запись \"{ru_ru_1.get(model, model)}\" успешно добавлена!', 'success')

            return redirect(url_for('common.list_items', model=model.lower()))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка добавления записи: {e}', 'error')

    related_fields = []
    if hasattr(model_db, 'specialization_id'):
        related_fields.append('specialization')
    if hasattr(model_db, 'doctor_id'):
        related_fields.append('doctor')
    if hasattr(model_db, 'patient_id'):
        related_fields.append('patient')
    if hasattr(model_db, 'service_id'):
        related_fields.append('service')

    return render_template(
        'add.html',
        model=ru_ru.get(model),
        columns=model_db.__table__.columns,
        column_labels=column_labels,
        related_fields=related_fields,
        Specialization=Specialization,
        Doctor=Doctor,
        Patient=Patient,
        Service=Service
    )

@bp.route('/delete/<model>/<int:id>', methods=['GET', 'POST'])
def delete(model, id):
    model_db = models.get(model.lower())
    if not model_db:
        flash('Модель не найдена!', 'error')
        return redirect(url_for('common.list_items', model=model.lower()))

    record = model_db.query.get(id)
    if not record:
        flash('Запись не найдена!', 'error')
        return redirect(url_for('common.list_items', model=model.lower()))

    if check_all_relations(model, record):
        return redirect(url_for('common.list_items', model=model.lower()))

    try:
        db.session.delete(record)
        db.session.commit()
        flash('Запись успешно удалена!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка удаления записи: {e}', 'error')

    return redirect(url_for('common.list_items', model=model.lower()))

# Редактирование записи
@bp.route('/edit/<model>/<int:id>', methods=['GET', 'POST'])
def edit(model, id):
    model_db = models.get(model.lower())
    if not model_db:
        flash('Модель не найдена!', 'error')
        return redirect(url_for('common.index'))

    record = model_db.query.get_or_404(id)

    if request.method == 'POST':
        try:
            for field in request.form:
                if hasattr(record, field):
                    setattr(record, field, request.form[field])

            if model.lower() == 'doctor' and 'specialization_id' in request.form:
                specialization = Specialization.query.get(request.form['specialization_id'])
                if specialization:
                    record.specialization_id = specialization.id
                else:
                    flash('Указанная специализация не найдена!', 'error')
                    return redirect(url_for('common.edit', model=model, id=id))

            if model.lower() in ['schedule', 'appointment', 'review'] and 'doctor_id' in request.form:
                doctor = Doctor.query.get(request.form['doctor_id'])
                if doctor:
                    record.doctor_id = doctor.id
                else:
                    flash('Указанный врач не найден!', 'error')
                    return redirect(url_for('common.edit', model=model, id=id))

            if model.lower() in ['appointment', 'review'] and 'patient_id' in request.form:
                patient = Patient.query.get(request.form['patient_id'])
                if patient:
                    record.patient_id = patient.id
                else:
                    flash('Указанный призывник не найден!', 'error')
                    return redirect(url_for('common.edit', model=model, id=id))

            if model.lower() == 'review' and 'service_id' in request.form:
                service = Service.query.get(request.form['service_id'])
                if service:
                    record.service_id = service.id
                else:
                    flash('Указанная услуга не найдена!', 'error')
                    return redirect(url_for('common.edit', model=model, id=id))

            db.session.commit()
            flash(f'Запись \"{ru_ru.get(model, model)}\" успешно обновлена!', 'success')

            return redirect(url_for('common.list_items', model=model.lower()))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка обновления записи: {e}', 'error')

    related_fields = []
    if hasattr(model_db, 'specialization_id'):
        related_fields.append('specialization')
    if hasattr(model_db, 'doctor_id'):
        related_fields.append('doctor')
    if hasattr(model_db, 'patient_id'):
        related_fields.append('patient')
    if hasattr(model_db, 'service_id'):
        related_fields.append('service')

    # Передача в шаблон
    return render_template(
        'edit.html',
        record=record,
        model=ru_ru.get(model),
        column_labels=column_labels,
        related_fields=related_fields,
        Specialization=Specialization,
        Doctor=Doctor,
        Patient=Patient,
        Service=Service
    )

def check_all_relations(model_name, record):
    relations_map = {
        'specialization': [('doctors', postfix_doctors)],
        'doctor': [
            ('schedules', postfix_schedules),
            ('appointments', postfix_appointments),
            ('prescription', postfix_prescription),
            ('review', postfix_reviews)
        ],
        'patient': [
            ('appointments', postfix_appointments),
            ('labtest', postfix_labtest),
            ('prescription', postfix_prescription),
            ('review', postfix_reviews)
        ],
        'service': [('review', postfix_reviews)]
    }

    related_checks = relations_map.get(model_name.lower(), [])
    for attr, postfix in related_checks:
        related_items = getattr(record, attr, [])
        if related_items:
            item_count = len(related_items)
            item_postfix = owl_postfix(item_count, *postfix)
            flash(
                f"Невозможно удалить {ru_ru_bullshit.get(model_name, model_name)}, "
                f"так как он(а) используется в {item_count} {item_postfix}.",
                'error'
            )
            return True
    return False

def owl_postfix(num: int, end_1: str = 'участник', end_2: str = 'участника', end_3: str = 'участников'):
    num = num % 10 if num > 20 else num
    return end_1 if num == 1 else end_2 if 1 < num < 5 else end_3
