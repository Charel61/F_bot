from aiogram.filters.state import State, StatesGroup





# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем

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



class FSMAddSpecialist(StatesGroup):


    fill_name = State()
    fill_speciality = State()
    fill_expirience = State()
    add_data = State()

class FSMManager(StatesGroup):

     manage_db = State()

class FSMAddSpeciality