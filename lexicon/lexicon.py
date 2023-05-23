LEXICON_RU: dict[str, str] = {
     '/start': 'Этот бот для записи к специалисту\n\n'
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
                              'Пожалуйста, введите имя и фамилию\n\n'
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

       'date':'Выберите желаемую дату визита',
       'time': 'Выберете желаемое время визита',
       'choice_specialist':'Пожалуйста выберите специалиста',
       'choice_speciality':'Пожалуйста выберите специальность',
       'confirm':'Подтвердить',
       'back':'Вернуться',
       '/add_specialist': 'Для добавления специалиста введите его фамилию и имя:',
       '/edit_specialist': 'Для редактирования специалиста введите его фамилию и имя:',
       'expiriencne': 'Пожалуйста введите стаж работы по специальности',
       '/start_manager': 'Для управления базой данных используйте слудуюущие команды:\n\n '
                          '/add_specialist - добавление специалиста в базу данных\n'
                          '/add_speciality - добавление специальности в базу данных\n'
                          '/show_specialist - просомтр данных о специалисте\n'
                          '/edit_speciality - редактирование специальности',
        'edit_speciality':'Для редактирования специальности нажмите соответсвующую кнопку',
       '/add_speciality': 'Введите наименование специальности',

       '/manage_db': 'Это бот для администратора бд.\n\n'
                     'Для управления БД введите команду\n /manage_db',
       'wrong_exp': 'Опыт работы должен быть числом от 0 до 70\n\n'
                            'Пожалуйста введите опыт работы.\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel',
        'edit':'Редактировать',
        'wrong_but':'Пожалуйста, воспользуйтесь кнопками!\n\n'
                              'Если вы хотите прервать операцию '
                              'отправьте команду /cancel',
        'delete': 'Удалить',
        'shure_del_spec':'Вы уверены, что хотите удлаить специалиста:',
        'choice_action':'Выберите необходимое действие',
        'shure_del_speciality': 'Вы уверены, что хотите удлаить специальность: ',





    }

LEXICON_COMMANDS_RU: dict[str, str] = {
      '/start': 'Запуск бота',
      '/fillform': 'Заполение анкеты',
      '/cancel': 'Отмена',
      '/showdata':'Просмотреть данные'

    }
