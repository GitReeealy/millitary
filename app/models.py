from app import db


# Призывникы
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    birth_date = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    medical_record = db.Column(db.String(50), nullable=False)
    oms_policy = db.Column(db.String(50))
    blood_group = db.Column(db.String(10))
    chronic_diseases = db.Column(db.String(255))

# Специализации
class Specialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Название специализации
    description = db.Column(db.String(255))  # Описание специализации

# Добавление связи к модели Doctor
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    specialization_id = db.Column(db.String(50), db.ForeignKey('specialization.id'), nullable=False)
    office_number = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

    specialization = db.relationship('Specialization', backref='doctors')

# Расписание
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    end_time = db.Column(db.String(20), nullable=False)
    slots_available = db.Column(db.String(10), nullable=False)

# Приемы
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date_time = db.Column(db.String(50), nullable=False)
    diagnosis = db.Column(db.String(255))
    treatment = db.Column(db.String(255))
    comments = db.Column(db.String(255))

    doctor = db.relationship('Doctor', backref='appointments')
    patient = db.relationship('Patient', backref='appointments')

# Медицинские услуги
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    cost = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(10), nullable=False)


# Рецепты
class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    medication_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    comments = db.Column(db.String(255))

    doctor = db.relationship('Doctor', backref='prescription')
    patient = db.relationship('Patient', backref='prescription')

# Уведомления
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255))
    message = db.Column(db.String(255))

# Словарь моделей для роутов
models = {
    'patient': Patient,
    'doctor': Doctor,
    'schedule': Schedule,
    'appointment': Appointment,
    'service': Service,
    'prescription': Prescription,
    'specialization': Specialization,
    'review': Review,
}

# Инициализация базы данных
def init_db():
    db.create_all()
