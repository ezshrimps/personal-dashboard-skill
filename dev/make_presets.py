"""Generates templates/presets/*.json. Edit the table below and re-run; the JSON files are what the skill reads."""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / 'templates' / 'presets'


def tpl(week, wkend):
    return {k: [week[k]] * 5 + [wkend[k]] * 2 for k in ('zh', 'en')}


MEALS_WKEND = {'zh': '09:30-10:00 起床、早餐 #rest\n12:00-13:00 午饭 #rest\n18:00-19:00 晚饭 #rest',
               'en': '09:30-10:00 Wake up, breakfast #rest\n12:00-13:00 Lunch #rest\n18:00-19:00 Dinner #rest'}

P = {
    'student': dict(
        name={'zh': '学生', 'en': 'Student'},
        desc={'zh': '上课、作业、考试倒计时、生活费', 'en': 'Classes, homework, exam countdowns, allowance budget'},
        pages=[('home', ['entry', 'now', 'todos', 'deadlines', 'checks', 'timeline']), ('money', ['spend', 'txns', 'recurring']), ('plan', ['week', 'review', 'calendar'])],
        checks=[('study', {'zh': '自习 / 复习', 'en': 'Study session'}, 5), ('read', {'zh': '阅读', 'en': 'Reading'}, 5), ('plan', {'zh': '做明天的计划', 'en': 'Plan tomorrow'}, 7)],
        trackers=[dict(id='tvocab', name={'zh': '背单词', 'en': 'Vocabulary'}, kind='count', unit={'zh': '个', 'en': 'words'}, goal=30, period='day', chart='bar')],
        goals={'workout': 2}, workouts={'zh': ['跑步', '球类', '健身'], 'en': ['Run', 'Sports', 'Gym']},
        templates=tpl({'zh': '08:00-08:30 起床、早餐 #rest\n09:00-12:00 上课 #study\n12:00-13:00 午饭 #rest\n14:00-17:00 上课 / 实验 #study\n18:00-19:00 晚饭 #rest\n19:30-21:30 自习 #study',
                       'en': '08:00-08:30 Wake up, breakfast #rest\n09:00-12:00 Classes #study\n12:00-13:00 Lunch #rest\n14:00-17:00 Classes / lab #study\n18:00-19:00 Dinner #rest\n19:30-21:30 Study #study'}, MEALS_WKEND),
        brief=['focus', 'calendar', 'deadlines', 'todos', 'checks', 'trackers', 'spend']),
    'worker': dict(
        name={'zh': '上班族', 'en': 'Office worker'},
        desc={'zh': '会议日程、待办、运动、记账、睡眠', 'en': 'Meetings, to-dos, exercise, spending, sleep'},
        pages=[('home', ['entry', 'now', 'todos', 'timeline', 'checks', 'sleep']), ('money', ['spend', 'txns', 'recurring', 'savings', 'insight']), ('health', ['workout', 'sleep', 'weight', 'week'])],
        checks=[('read', {'zh': '阅读', 'en': 'Reading'}, 5), ('plan', {'zh': '做明天的计划', 'en': 'Plan tomorrow'}, 5)],
        trackers=[], goals={'workout': 3}, workouts={'zh': ['健身', '跑步', '瑜伽', '游泳'], 'en': ['Gym', 'Run', 'Yoga', 'Swim']},
        templates=tpl({'zh': '07:30-08:00 起床、早餐 #rest\n08:30-09:15 通勤 #transit\n09:30-12:00 专注工作 #work\n12:00-13:00 午饭 #rest\n13:00-18:00 工作 #work\n18:00-18:45 通勤 #transit\n19:00-20:00 晚饭 #rest',
                       'en': '07:30-08:00 Wake up, breakfast #rest\n08:30-09:15 Commute #transit\n09:30-12:00 Focus work #work\n12:00-13:00 Lunch #rest\n13:00-18:00 Work #work\n18:00-18:45 Commute #transit\n19:00-20:00 Dinner #rest'}, MEALS_WKEND),
        brief=['focus', 'calendar', 'todos', 'sleep', 'workout', 'spend']),
    'jobseeker': dict(
        name={'zh': '求职者', 'en': 'Job seeker'},
        desc={'zh': '投递追踪、截止日、每日投递数', 'en': 'Application tracker, deadlines, daily application count'},
        pages=[('home', ['entry', 'todos', 'jobs', 'deadlines', 'checks']), ('money', ['spend', 'txns', 'recurring']), ('plan', ['week', 'timeline', 'calendar', 'review'])],
        checks=[('apply', {'zh': '投递', 'en': 'Apply'}, 5), ('prep', {'zh': '刷题 / 练面试', 'en': 'Interview practice'}, 5), ('net', {'zh': '联系一个人', 'en': 'Reach out to one person'}, 3)],
        trackers=[dict(id='tapps', name={'zh': '今日投递', 'en': 'Applications'}, kind='count', unit={'zh': '份', 'en': ''}, goal=5, period='day', chart='bar')],
        goals={'workout': 2}, workouts={'zh': ['健身', '跑步'], 'en': ['Gym', 'Run']},
        templates=tpl({'zh': '08:30-09:00 起床、早餐 #rest\n09:00-11:30 投递和改简历 #work\n12:00-13:00 午饭 #rest\n13:30-16:00 刷题 / 练面试 #study\n18:00-19:00 晚饭 #rest',
                       'en': '08:30-09:00 Wake up, breakfast #rest\n09:00-11:30 Applications, resume #work\n12:00-13:00 Lunch #rest\n13:30-16:00 Interview practice #study\n18:00-19:00 Dinner #rest'}, MEALS_WKEND),
        brief=['focus', 'calendar', 'jobs', 'deadlines', 'todos', 'trackers', 'spend']),
    'freelancer': dict(
        name={'zh': '自由职业 / 创业', 'en': 'Freelancer / founder'},
        desc={'zh': '收入、项目截止日、待办、开票提醒', 'en': 'Income, project deadlines, to-dos, invoice reminders'},
        pages=[('home', ['entry', 'now', 'todos', 'deadlines', 'timeline']), ('money', ['income', 'spend', 'txns', 'recurring', 'savings', 'insight']), ('plan', ['week', 'calendar', 'review'])],
        checks=[('deep', {'zh': '2 小时深度工作', 'en': '2h deep work'}, 5), ('plan', {'zh': '做明天的计划', 'en': 'Plan tomorrow'}, 5)],
        trackers=[dict(id='tbill', name={'zh': '可计费时长', 'en': 'Billable hours'}, kind='number', unit={'zh': '小时', 'en': 'h'}, goal=25, period='week', chart='bar')],
        goals={'workout': 3}, workouts={'zh': ['健身', '跑步', '瑜伽'], 'en': ['Gym', 'Run', 'Yoga']},
        templates=tpl({'zh': '08:00-08:30 起床、早餐 #rest\n09:00-11:30 深度工作 #work\n12:00-13:00 午饭 #rest\n13:30-15:00 沟通和会议 #meet\n15:00-17:30 项目 #work\n18:30-19:30 晚饭 #rest',
                       'en': '08:00-08:30 Wake up, breakfast #rest\n09:00-11:30 Deep work #work\n12:00-13:00 Lunch #rest\n13:30-15:00 Calls and meetings #meet\n15:00-17:30 Projects #work\n18:30-19:30 Dinner #rest'}, MEALS_WKEND),
        brief=['focus', 'calendar', 'deadlines', 'todos', 'income', 'spend', 'trackers']),
    'health': dict(
        name={'zh': '健康优先', 'en': 'Health first'},
        desc={'zh': '睡眠、运动、饮食、体重、吃药', 'en': 'Sleep, exercise, food, weight, medication'},
        pages=[('home', ['entry', 'sleep', 'workout', 'food', 'checks', 'todos']), ('health', ['weight', 'week', 'timeline']), ('money', ['spend', 'txns', 'recurring'])],
        checks=[('water', {'zh': '喝够水', 'en': 'Enough water'}, 7), ('stretch', {'zh': '拉伸', 'en': 'Stretch'}, 5), ('nosugar', {'zh': '不喝含糖饮料', 'en': 'No sugary drinks'}, 7)],
        trackers=[dict(id='tmeds', name={'zh': '吃药 / 维生素', 'en': 'Meds / vitamins'}, kind='check', unit={'zh': '', 'en': ''}, goal=1, period='day', chart='streak')],
        goals={'workout': 4}, workouts={'zh': ['力量', '有氧', '瑜伽', '散步'], 'en': ['Strength', 'Cardio', 'Yoga', 'Walk']},
        food={'protein': 100, 'kcal': 2000},
        templates=tpl({'zh': '07:00-07:30 起床、早餐 #rest\n12:00-13:00 午饭 #rest\n18:00-19:00 运动 #sport\n19:00-20:00 晚饭 #rest\n22:30-23:00 准备睡觉 #rest',
                       'en': '07:00-07:30 Wake up, breakfast #rest\n12:00-13:00 Lunch #rest\n18:00-19:00 Exercise #sport\n19:00-20:00 Dinner #rest\n22:30-23:00 Wind down #rest'},
                      {'zh': '08:00-08:30 起床、早餐 #rest\n10:00-11:00 运动 #sport\n12:00-13:00 午饭 #rest\n18:00-19:00 晚饭 #rest',
                       'en': '08:00-08:30 Wake up, breakfast #rest\n10:00-11:00 Exercise #sport\n12:00-13:00 Lunch #rest\n18:00-19:00 Dinner #rest'}),
        brief=['focus', 'sleep', 'workout', 'food', 'trackers', 'todos']),
    'family': dict(
        name={'zh': '家庭 / 年长用户', 'en': 'Family / older users'},
        desc={'zh': '吃药与复诊提醒、固定支出、大字号、精简界面', 'en': 'Medication and appointment reminders, bills, large text, fewer blocks'},
        pages=[('home', ['entry', 'todos', 'calendar', 'spend'])],
        checks=[], scale=1.3,
        trackers=[dict(id='tmeds', name={'zh': '按时吃药', 'en': 'Took my medicine'}, kind='check', unit={'zh': '', 'en': ''}, goal=1, period='day', chart='streak'),
                  dict(id='tbp', name={'zh': '血压（高压）', 'en': 'Blood pressure (systolic)'}, kind='number', unit={'zh': 'mmHg', 'en': 'mmHg'}, goal=0, period='day', chart='bar')],
        goals={'workout': 0}, workouts={'zh': [], 'en': []},
        templates=tpl({'zh': '', 'en': ''}, {'zh': '', 'en': ''}),
        brief=['focus', 'calendar', 'todos', 'trackers', 'spend']),
}

for pid, p in P.items():
    out = {
        'id': pid, 'name': p['name'], 'desc': p['desc'],
        'layout': {'pages': [{'id': i, 'name': '', 'blocks': b + (['tracker:' + t['id'] for t in p['trackers']] if i == 'home' else [])} for i, b in p['pages']]},
        'checks': [{'k': k, 'n': n, 'goal': g} for k, n, g in p['checks']],
        'trackers': p['trackers'], 'goals': p['goals'], 'workouts': p['workouts'], 'rotation': [],
        'food': p.get('food', {'protein': 0, 'kcal': 0}), 'ui': {'scale': p.get('scale', 1)},
        'templates': p['templates'], 'brief': p['brief'],
    }
    (OUT / f'{pid}.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(sorted(P))
