SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
SECRET_KEY = "supersecretkey"

postfix_schedules = "расписании", "расписаниях", "расписаниях"
postfix_appointments = "приёме", "приёмах", "приёмах"
postfix_labtest = "лабораторном испытании", "лабораторных испытаниях", "лабораторных испытаниях"
postfix_prescription = "рецепте", "рецептах", "рецептах"
postfix_doctors = "докторе", "докторах", "докторах"
postfix_reviews = "уведомление", "уведомлениях", "уведомлениях"

column_labels = {
    'id': 'ID',
    'full_name': 'ФИО',
    'birth_date': 'Дата рождения',
    'address': 'Адрес',
    'phone': 'Телефон',
    'email': 'Электронная почта',
    'medical_record': 'Номер медицинской карты',
    'oms_policy': 'Полис ОМС',
    'blood_group': 'Группа крови',
    'chronic_diseases': 'Хронические заболевания',

    'specialization': 'Специализация',
    'specialization_id': 'ID специализации',
    'office_number': 'Номер кабинета',

    'date': 'Дата',
    'start_time': 'Время начала',
    'end_time': 'Время окончания',
    'slots_available': 'Дополнительная информация',

    'message': 'Сообщение',

    'patient_id': 'Призывник',
    'doctor_id': 'Врач',
    'date_time': 'Дата и время приема',
    'diagnosis': 'Диагноз',
    'treatment': 'Назначенное лечение',
    'comments': 'Комментарии',

    'name': 'Название',
    'description': 'Описание',
    'cost': 'Стоимость',
    'duration': 'Длительность (минуты)',

    'test_type': 'Тип исследования',
    'results': 'Результаты',
    'doctor_recommendations': 'Рекомендации врача',

    'medication_name': 'Название лекарства',
    'dosage': 'Дозировка',
    'frequency': 'Частота приема',

    'rating': 'Оценка',
    'service_id': 'Услуга',

    'insurance_company': 'Страховая компания',
    'contact_info': 'Контактная информация',
}

model_to_bp = {
    "patient": "patients",
    "doctor": "doctors",
    "schedule": "schedules",
    "appointment": "appointments",
    "service": "services",
    "labtest": "labtests",
    "prescription": "prescriptions",
    "insurancecompany": "insurance",
    "specialization": "specializations",
    "review": "reviews"
}

ru_ru = {
    "patient": "призывника",
    "doctor": "врача",
    "schedule": "расписания",
    "appointment": "приема",
    "service": "услуги",
    "labtest": "лабораторного исследования",
    "prescription": "рецепта",
    "insurancecompany": "страховой компании",
    "specialization": "специализации",
    "review": "уведомления"
}

ru_ru_bullshit = {
    "patient": "призывника",
    "doctor": "врача",
    "schedule": "расписание событий",
    "appointment": "прием",
    "service": "услугу",
    "labtest": "лабораторное исследование",
    "prescription": "рецепт",
    "insurancecompany": "страховую компанию",
    "specialization": "специализацию",
    "review": "уведомление"
}

ru_ru_1 = {
    "patient": "призывник",
    "doctor": "врач",
    "schedule": "расписание событий",
    "appointment": "прием",
    "service": "услуга",
    "labtest": "лабораторное исследование",
    "prescription": "рецепт",
    "insurancecompany": "страховая компания",
    "specialization": "специализация",
    "review": "уведомление"
}

ru_ru_more_than_1 = {
    "patient": "призывников",
    "doctor": "врачей",
    "schedule": "расписания",
    "appointment": "приемов",
    "service": "услуг",
    "labtest": "лабораторных исследований",
    "prescription": "рецептов",
    "insurancecompany": "страховых компаниий",
    "specialization": "специализаций",
    "review": "уведомления"
}
