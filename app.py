"""
VeerAI - Defence Aspirant Chatbot
Flask Backend
"""
import os
import sys
import json
import uuid
import random
from flask import Flask, render_template, request, jsonify, session

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

from modules.database import init_db, save_chat, get_current_affairs, save_quiz_score, get_quiz_scores
from modules.quiz import (get_quiz, get_wat_word, get_srt_situation, get_tat_situation,
                          get_ssb_question, get_olq_questions, analyze_olq, calculate_bmi)
from modules.chatbot import get_bot

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize database on startup
init_db()

def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

# ── MAIN ROUTES ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/ssb')
def ssb_page():
    return render_template('ssb.html')

@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html')

@app.route('/olq')
def olq_page():
    return render_template('olq.html')

@app.route('/fitness')
def fitness_page():
    return render_template('fitness.html')

@app.route('/current_affairs')
def current_affairs_page():
    return render_template('current_affairs.html')

@app.route('/career')
def career_page():
    return render_template('career.html')

@app.route('/psychology')
def psychology_page():
    return render_template('psychology.html')

# ── API ROUTES ─────────────────────────────────────────────────────────────

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    user_msg = data.get('message', '').strip()
    if not user_msg:
        return jsonify({'response': 'Please type a message.'})

    bot = get_bot()
    response = bot.get_response(user_msg)
    save_chat(get_session_id(), user_msg, response)
    return jsonify({'response': response})

@app.route('/api/quiz', methods=['GET'])
def api_quiz():
    category = request.args.get('category', 'Defence')
    num = int(request.args.get('num', 5))
    questions = get_quiz(category, num)
    return jsonify({'questions': questions, 'category': category})

@app.route('/api/quiz/submit', methods=['POST'])
def api_quiz_submit():
    data = request.json
    category = data.get('category', 'General')
    score = data.get('score', 0)
    total = data.get('total', 0)
    save_quiz_score(get_session_id(), category, score, total)
    percentage = round((score / total * 100) if total > 0 else 0, 1)
    if percentage >= 80:
        msg = "Excellent! Outstanding performance! 🏆"
    elif percentage >= 60:
        msg = "Good job! Keep practising! 💪"
    else:
        msg = "Keep studying! You'll improve! 📚"
    return jsonify({'percentage': percentage, 'message': msg})

@app.route('/api/wat', methods=['GET'])
def api_wat():
    return jsonify({'word': get_wat_word()})

@app.route('/api/srt', methods=['GET'])
def api_srt():
    return jsonify({'situation': get_srt_situation()})

@app.route('/api/tat', methods=['GET'])
def api_tat():
    return jsonify({'situation': get_tat_situation()})

@app.route('/api/ssb/question', methods=['GET'])
def api_ssb_question():
    stage = request.args.get('stage', 'personal')
    question = get_ssb_question(stage)
    return jsonify({'question': question, 'stage': stage})

@app.route('/api/ssb/feedback', methods=['POST'])
def api_ssb_feedback():
    data = request.json
    answer = data.get('answer', '')
    stage = data.get('stage', 'personal')
    word_count = len(answer.split())

    feedbacks = []
    if word_count < 20:
        feedbacks.append("Your answer is too brief. Elaborate more with specific examples.")
    elif word_count > 200:
        feedbacks.append("Good detail! But be concise - aim for 50-100 words in actual interview.")
    else:
        feedbacks.append("Good length! Be specific and confident in delivery.")

    positive_words = ['initiative', 'leadership', 'team', 'responsibility', 'nation', 'duty', 'honest', 'discipline']
    found = [w for w in positive_words if w in answer.lower()]
    if found:
        feedbacks.append(f"Good use of officer-like values: {', '.join(found)}.")
    else:
        feedbacks.append("Try to incorporate officer-like qualities: leadership, initiative, responsibility.")

    if stage == 'situation':
        if any(w in answer.lower() for w in ['call', 'inform', 'help', 'assist', 'organize', 'lead']):
            feedbacks.append("Good initiative shown in handling the situation!")
        else:
            feedbacks.append("Show more concrete action steps in situational answers.")

    score = min(10, word_count // 15 + len(found) * 2)
    return jsonify({'feedback': ' '.join(feedbacks), 'score': score})

@app.route('/api/olq', methods=['GET'])
def api_olq_questions():
    return jsonify({'questions': get_olq_questions()})

@app.route('/api/olq/analyze', methods=['POST'])
def api_olq_analyze():
    data = request.json
    answers = data.get('answers', [])
    report = analyze_olq(answers)
    return jsonify(report)

@app.route('/api/fitness/bmi', methods=['POST'])
def api_bmi():
    data = request.json
    height = float(data.get('height', 170))
    weight = float(data.get('weight', 70))
    result = calculate_bmi(height, weight)
    return jsonify(result)

@app.route('/api/current_affairs', methods=['GET'])
def api_current_affairs():
    category = request.args.get('category', None)
    affairs = get_current_affairs(category, limit=20)
    return jsonify({'affairs': affairs})

@app.route('/api/study_plan', methods=['POST'])
def api_study_plan():
    data = request.json
    exam = data.get('exam', 'NDA')
    months = int(data.get('months', 6))
    hours = float(data.get('hours', 4))

    plans = {
        "NDA": {
            "subjects": ["Mathematics (NCERT 11-12)", "English Grammar & Vocabulary", "Physics & Chemistry", "History & Geography", "General Science", "Current Affairs & Defence"],
            "monthly": [
                "Month 1-2: Foundation - NCERT basics for all subjects",
                "Month 3-4: Deep study - Previous year papers, topic-wise practice",
                "Month 5: Revision & Mock Tests - Full syllabus revision",
                "Month 6: Final Prep - Daily mock tests, current affairs revision"
            ]
        },
        "CDS": {
            "subjects": ["English (Grammar, Comprehension, Vocabulary)", "General Knowledge (History, Geography, Science, Economy)", "Elementary Mathematics (if IMA/AFA)", "Current Affairs & Defence"],
            "monthly": [
                "Month 1-2: NCERT revision for GK subjects",
                "Month 3-4: Previous papers + newspaper reading daily",
                "Month 5: Mock tests and weak area focus",
                "Month 6: Revision, current affairs, English practice"
            ]
        },
        "AFCAT": {
            "subjects": ["General Awareness", "Verbal Ability in English", "Numerical Ability", "Reasoning & Military Aptitude", "EKT (if Technical Branch)"],
            "monthly": [
                "Month 1-2: Strong English foundation + GK basics",
                "Month 3-4: Numerical and Reasoning practice daily",
                "Month 5: AFCAT mock tests + defence current affairs",
                "Month 6: Revision, GK updates, speed practice"
            ]
        }
    }

    plan = plans.get(exam, plans["NDA"])
    daily_schedule = {
        "Morning (1.5 hrs)": "Physical fitness training (running, pushups, situps)",
        f"Study Block 1 ({hours/2:.0f} hrs)": f"Primary subject: {plan['subjects'][0]}",
        f"Study Block 2 ({hours/2:.0f} hrs)": "Secondary subjects + current affairs",
        "Evening (30 min)": "Newspaper reading + defence news",
        "Night (30 min)": "Revision of the day's study"
    }

    return jsonify({
        "exam": exam,
        "duration_months": months,
        "daily_hours": hours,
        "subjects": plan["subjects"],
        "monthly_plan": plan["monthly"],
        "daily_schedule": daily_schedule,
        "tip": f"Consistency is key! Study {hours} hours daily without fail. Physical fitness is as important as academics for defence selection."
    })

if __name__ == '__main__':
    print("🎖️  Starting VeerAI - Defence Aspirant Chatbot")
    print("🌐 Open your browser at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
