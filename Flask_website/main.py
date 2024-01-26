from flask import Flask, render_template, redirect, request
import os
import json

app = Flask(__name__)

# Сначала пишем нужные для сохранения данных функции

# Сохраняем данные в файл
def save_data(answer):
    path = 'Flask_website/data.json'
    if not os.path.exists(path):
        data = {'answers': []}
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['answers'].append(answer)
    
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Читаем данные из файла
def load_data():
    if not os.path.exists('Flask_website/data.json'):
        data = {'answers': []}
        with open('Flask_website/data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    with open('Flask_website/data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# Переходим к сайту

@app.route('/')
def menu():
    heading = "Приветствуем!"
    text = 'Мы - команда студентов "Фундаментальной и компьютерной лингвистики НИУ ВШЭ", и мы проводим исследование, связанное с вариативностью постановки ударения в различных словах. Пожалуйста, пройдите наш опрос, мы будем очень благодарны. Заранее спасибо!'

    return render_template('menu.html', heading=heading, text=text)


@app.route('/statistics')
def statistics():
    # Загружаем данные из файла
    with open('Flask_website/data.json', 'r', encoding='utf-8') as file:
        data = load_data()

    # Считаем статистику
    counts = {}
    for i in ['age', 'gender', 'answer1', 'answer2', 'answer3', 'answer4', 'answer5',
              'answer6', 'answer7', 'answer8', 'user']:
            for j in data['answers']:
                response = j.get(i)
                if response is not None:
                    if response in counts:
                        counts[response] += 1
                    else:
                        counts[response] = 1
    del counts['Выберите опцию']

    heading = "Общая статистика ответов"
    text = "Здесь вы можете посмотреть статистику по каждому вопросу анкеты. Слева будет написана опция, которая была доступа в анкете, а справа - количество человек, который эту опцию выбрали."
    return render_template('statistics.html', heading=heading, text=text, statistics=counts)


@app.route('/form', methods=['GET', 'POST'])
def form():

    if request.method == 'POST':  # если запрос отправляется, то:

        # Получаем данные из формы:
        gender = request.form.get('gender')
        age = request.form.get('age')
        answer1 = request.form.get('answer1')
        answer2 = request.form.get('answer2')
        answer3 = request.form.get('answer3')
        answer4 = request.form.get('answer4')
        answer5 = request.form.get('answer5')
        answer6 = request.form.get('answer6')
        answer7 = request.form.get('answer7')
        answer8 = request.form.get('answer8')

        # Создаем словарь с данными:
        answer = {
            'gender': gender,
            'age': age,
            'answer1': answer1,
            'answer2': answer2,
            'answer3': answer3,
            'answer4': answer4,
            'answer5': answer5,
            'answer6': answer6,
            'answer7': answer7,
            'answer8': answer8,
            'user': "yes"
            # пригодится при подсчете прошедших опрос людей, которые могли не ответить на какой-либо вопрос, но ответить на остальные
        }

        save_data(answer)

        return redirect('/statistics')

    heading = "Пожалуйста, пройдите анкету"
    text = 'Сначала Вам предстоит ответить на несколько вопросов о себе. Далее Вам нужно будет отметить, с каким ударением Вы произносите те или иные слова. Пожалуйста, не оставляйте поля для ответов пустыми!'
    form = """  
    <form action="/form" method = 'POST'>

    <div class="mb-3 row text-start">
        <label class="col-form-label col-form-label-lg text-start">Пожалуйста, отметьте свой пол:</label>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="gender" value="male">
            <label class="custom-control-label" for="customRadio1">Мужской</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="gender" value="female">
            <label class="custom-control-label" for="customRadio2">Женский</label>
        </div>
    </div>

 <div class="mb-3 row text-start">
    <label class="col-form-label col-form-label-lg">Пожалуйста, укажите, к какой возрастной категории вы относитесь:</label>
    <select class="form-select" aria-label="Default select example" name="age">
        <option selected>Выберите опцию</option>
        <option value="<18">До 18 лет</option>
        <option value="18-25">18-25 лет</option>
        <option value="26-35">26-35 лет</option>
        <option value="36-45">36-45 лет</option>
        <option value="46-55">46-55 лет</option>
        <option value="55<">55 лет и выше</option>
    </select>
</div>

<br>
<h4>Пожалуйста, отметьте, с каким ударением Вы обычно произносите следующие слова:</h4>

    <div class="mb-3 row text-start">
        <label class="col-form-label col-form-label-lg text-start">баржа:</label>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer1" value="бАржа">
            <label class="custom-control-label" for="customRadio1">бАржа</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer1" value="баржА">
            <label class="custom-control-label" for="customRadio2">баржА</label>
        </div>
    </div>

    <div class="mb-3 row text-start">
        <label class="col-form-label col-form-label-lg text-start">кирзовый:</label>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer2" value="кИрзовый">
            <label class="custom-control-label" for="customRadio1">кИрзовый</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer2" value="кирзОвый">
            <label class="custom-control-label" for="customRadio2">кирзОвый</label>
        </div>
    </div>


        <div class="mb-3 row text-start">
        <label class="col-form-label col-form-label-lg text-start">ржаветь:</label>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer3" value="ржАветь">
            <label class="custom-control-label" for="customRadio1">ржАветь</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer3" value="ржавЕть">
            <label class="custom-control-label" for="customRadio2">ржавЕть</label>
        </div>
    </div>

    <div class="mb-3 row text-start">
        <label class="col-form-label col-form-label-lg text-start">петля:</label>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer4" value="петлЯ">
            <label class="custom-control-label" for="customRadio1">петлЯ</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer4" value="пЕтля">
            <label class="custom-control-label" for="customRadio2">пЕтля</label>
        </div>
    </div>

    <div class="mb-3 row text-start">
        <label class="col-form-label col-form-label-lg text-start">иначе:</label>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer5" value="Иначе">
            <label class="custom-control-label" for="customRadio1">Иначе</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer5" value="инАче">
            <label class="custom-control-label" for="customRadio2">инАче</label>
        </div>
    </div>

    <div class="mb-3 row text-start">
        <label class="col-form-label col-form-label-lg text-start">гофрировать:</label>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer6" value="гофрировАть">
            <label class="custom-control-label" for="customRadio1">гофрировАть</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer6" value="гофрИровать">
            <label class="custom-control-label" for="customRadio2">гофрИровать</label>
        </div>
    </div>
    
    <div class="mb-3 row text-start">
        <label class="col-form-label col-form-label-lg text-start">искриться:</label>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer7" value="искрИться">
            <label class="custom-control-label" for="customRadio1">искрИться</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer7" value="Искриться">
            <label class="custom-control-label" for="customRadio2">Искриться</label>
        </div>
    </div>

    <div class="mb-3 row text-start">
        <label class="col-form-label col-form-label-lg text-start">окислиться:</label>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer8" value="окислИться">
            <label class="custom-control-label" for="customRadio1">окислИться</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" name="answer8" value="окИслиться">
            <label class="custom-control-label" for="customRadio2">окИслиться</label>
        </div>
    </div>

    <br>
    <h5>Огромное спасибо за участие в опросе! Как только Вы нажмёте на кнопку "отправить", сайт автоматически перебросит Вас на страницу с общей статистикой ответов всех прошедших опрос.</h5>
    <br>
    <button type="submit" class="btn btn-primary">Отправить</button>
    </form>

    """

    return render_template('form.html', heading=heading, text=text, form=form)


if __name__ == '__main__':
    app.run(debug=True)
