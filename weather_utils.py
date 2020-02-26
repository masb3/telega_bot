from telegram import InlineKeyboardButton


regions_list = ['eu', 'ru', 'usa', 'asia']
eu_list = ['Tallinn', 'London', 'Oslo', 'Paris']
ru_list = ['Moscow', 'Novosibirsk', 'Sochi']
usa_list = ['Chicago', 'Boston']
asia_list = ['Tokio', 'Taiwan', 'Beijing']


def create_keyboard(data_list, buttons_in_row=2):
    i = 0
    keyboard = [[]]
    for data in data_list:
        if len(keyboard[i]) == buttons_in_row:
            i += 1
            keyboard.append([])

        keyboard[i].append(InlineKeyboardButton(data.upper(), callback_data=data))
    return keyboard


def create_regions_keyboard():
    return create_keyboard(regions_list)


def create_cities_keyboard(region):
    if region == 'eu':
        region_list = eu_list[:]
    elif region == 'ru':
        region_list = ru_list[:]
    elif region == 'usa':
        region_list = usa_list[:]
    elif region == 'asia':
        region_list = asia_list[:]
    else:
        region_list = []

    return create_keyboard(region_list)