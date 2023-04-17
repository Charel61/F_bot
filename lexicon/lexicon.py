LEXICON_RU: dict[str, str] = {
     '/start': 'Этот бот демонстрирует работу FSM\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform',
      '/cancel':'Отменять нечего.\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform',
      '/fillform':            'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте команду /fillform',
      'name': 'Пожалуйста введите ваше имя и фамилию',
      'age':'Спасибо!\n\nА теперь введите ваш возраст',
      'wrong_age':'Возраст должен быть целым числом от 4 до 120\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel',
      'wrong_name': 'То, что вы отправили не похоже на имя и фамилию\n\n'
                              'Пожалуйста, введите ваше имя\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel',
      'male':'Мужской ♂',
      'female':'Женский ♀',
      'undefined_gender':'🤷 Пока не ясно',
      'gender': 'Спасибо!\n\nУкажите ваш пол',
      'wrong':'Пожалуйста, воспользуйтесь кнопками!\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel',
      'photo': 'Спасибо! А теперь загрузите, '
                                       'пожалуйста, ваше фото',
      'secondary':'Среднее',
      'higher':'Высшее',
      'no_edu':'🤷 Нету',
      'edu': 'Спасибо!\n\nУкажите ваше образование',
      'wrong_photo': 'Пожалуйста, на этом шаге отправьте '
                              'ваше фото\n\nЕсли вы хотите прервать '
                              'заполнение анкеты - отправьте команду /cancel',
      'news':'Спасибо!\n\n'
                                          'Остался последний шаг.\n'
                                          'Хотели бы вы получать новости?',
      'yes':'Да',
      'no':'Нет, спасибо',
      'saved_data': 'Спасибо! Ваши данные сохранены!',
      'sent_data': 'Спасибо! Ваши данные отправлены!',
      'do_not_send':'Не отправлять',
      'send': 'Отправить',
      'didnt_fill':'Вы еще не заполняли анкету. '
                                  'Чтобы приступить - отправьте '
                                  'команду /fillform',
       'dont_understand': 'Не понимаю, воспользуйтесь кнопками меню',
       'date':'Выберите желаемую даут визита'



    }

LEXICON_COMMANDS_RU: dict[str, str] = {
      '/start': 'Запуск бота',
      '/fillform': 'Заполение анкеты',
      '/cancel': 'Отмена',
      '/showdata':'Просмотреть данные'

    }