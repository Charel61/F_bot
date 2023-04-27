from aiogram.filters.state import State, StatesGroup





# Cоздаем класс, наследуемый от StatesGroup, для группы состояний заполнения анкеты
class FSMFillForm(StatesGroup):


    fill_name = State()        # Состояние ожидания ввода имени
    fill_age = State()         # Состояние ожидания ввода возраста
    fill_date = State()        #Состояние ожидания выбора даты
    fill_time = State()        #Состояние ожидания выбора времени
    fill_age = State()         # Состояние ожидания ввода возраста
    fill_gender = State()      # Состояние ожидания выбора пола
    fill_speciality = State() # Состояние ожидания выбора специальности
    fill_specialist = State() # Состояние ожидания выбора специалиста
    fill_education = State()   # Состояние ожидания выбора образования
    fill_wish_news = State()   # Состояние ожидания выбора получать ли новости
    fill_send_data = State()   # Состояние ожидания выбора отправлять ли анкету администратору


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний управления БД
class FSMManager(StatesGroup):

    manage_db = State() #Состояние управления БД
    choice_specialities = State() #Состояние просмотра списка специальности
    choice_specialist = State()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний добавления спцеалиста в БД
class FSMAddSpecialist(StatesGroup):


    fill_name = State()
    fill_speciality = State()
    fill_expirience = State()
    add_data = State()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний добавления спцеальности в БД
class FSMAddSpeciality(StatesGroup):

    add_data = State()
    add_speciality = State()
