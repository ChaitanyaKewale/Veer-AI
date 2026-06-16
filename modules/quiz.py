import random

QUIZ_DATA = {
    "NDA": [
        {"q": "NDA exam is conducted by which body?", "options": ["UPSC", "SSC", "Ministry of Defence", "NDA Board"], "ans": 0},
        {"q": "NDA is located at?", "options": ["Pune", "Delhi", "Dehradun", "Chandigarh"], "ans": 0},
        {"q": "NDA written exam total marks are?", "options": ["600", "900", "1200", "1800"], "ans": 1},
        {"q": "Maximum age for NDA is?", "options": ["18 years", "19.5 years", "21 years", "23 years"], "ans": 1},
        {"q": "NDA training duration is?", "options": ["2 years", "3 years", "4 years", "1.5 years"], "ans": 1},
        {"q": "NDA is a joint services academy for?", "options": ["Army only", "Navy only", "Army and Navy", "Army, Navy and Air Force"], "ans": 3},
        {"q": "After NDA, Army cadets go to which academy?", "options": ["INA", "IMA", "AFA", "OTA"], "ans": 1},
        {"q": "NDA GAT paper carries how many marks?", "options": ["300", "400", "600", "900"], "ans": 2},
    ],
    "CDS": [
        {"q": "CDS stands for?", "options": ["Combined Defence Services", "Central Defence Squad", "Corps Defence Services", "Chief Defence Staff"], "ans": 0},
        {"q": "CDS OTA trains officers for which commission?", "options": ["Permanent Commission", "Short Service Commission", "Emergency Commission", "Special Commission"], "ans": 1},
        {"q": "CDS negative marking is?", "options": ["1/4", "1/3", "1/2", "No negative marking"], "ans": 1},
        {"q": "CDS IMA is located at?", "options": ["Pune", "Dehradun", "Gaya", "Chennai"], "ans": 1},
        {"q": "Age limit for CDS IMA is?", "options": ["19-23", "19-24", "20-25", "21-26"], "ans": 1},
        {"q": "CDS exam has how many papers for IMA?", "options": ["1", "2", "3", "4"], "ans": 2},
    ],
    "SSB": [
        {"q": "SSB interview is of how many days?", "options": ["3 days", "4 days", "5 days", "7 days"], "ans": 2},
        {"q": "In TAT, candidate is shown how many pictures?", "options": ["10", "11", "12", "15"], "ans": 2},
        {"q": "WAT stands for?", "options": ["Word Ability Test", "Written Aptitude Test", "Word Association Test", "Written Assessment Test"], "ans": 2},
        {"q": "SRT has how many situations?", "options": ["45", "50", "55", "60"], "ans": 3},
        {"q": "GTO stands for?", "options": ["Group Testing Officer", "General Training Officer", "Group Task Officer", "General Testing Official"], "ans": 0},
        {"q": "PVC stands for?", "options": ["Param Veer Chakra", "Param Vir Chakra", "Praveen Vir Chakra", "Parakram Vir Chakra"], "ans": 1},
        {"q": "SSB Conference is held on which day?", "options": ["Day 3", "Day 4", "Day 5", "Day 6"], "ans": 2},
    ],
    "Defence": [
        {"q": "Who is called the 'Missile Man of India'?", "options": ["Vikram Sarabhai", "APJ Abdul Kalam", "K Sivan", "R Chidambaram"], "ans": 1},
        {"q": "India's first aircraft carrier INS Vikrant was decommissioned in?", "options": ["1995", "1997", "2000", "2003"], "ans": 1},
        {"q": "Param Vir Chakra is equivalent to which award?", "options": ["George Cross", "Victoria Cross", "Medal of Honor", "Iron Cross"], "ans": 1},
        {"q": "BrahMos missile is a joint venture of India and?", "options": ["USA", "France", "Russia", "Israel"], "ans": 2},
        {"q": "Operation Vijay refers to?", "options": ["1965 War", "1971 War", "Kargil 1999", "Operation Blue Star"], "ans": 2},
        {"q": "INS Arihant is India's first?", "options": ["Aircraft carrier", "Nuclear submarine", "Destroyer", "Frigate"], "ans": 1},
        {"q": "DRDO was established in?", "options": ["1948", "1958", "1965", "1972"], "ans": 1},
        {"q": "Agniveer scheme was launched in?", "options": ["2020", "2021", "2022", "2023"], "ans": 2},
        {"q": "LCA Tejas is developed by?", "options": ["DRDO only", "HAL only", "HAL and DRDO", "BEL"], "ans": 2},
        {"q": "India's defence budget is approximately what % of GDP?", "options": ["1.2%", "1.8%", "2.1%", "3%"], "ans": 2},
    ],
    "CurrentAffairs": [
        {"q": "Operation Sindoor targeted terrorist infrastructure in?", "options": ["Bangladesh", "Pakistan and POK", "Afghanistan", "Myanmar"], "ans": 1},
        {"q": "INS Vikrant is India's?", "options": ["First nuclear submarine", "First indigenous aircraft carrier", "Largest destroyer", "Latest frigate"], "ans": 1},
        {"q": "AMCA is India's planned?", "options": ["4th gen fighter", "5th gen stealth fighter", "Helicopter", "Drone"], "ans": 1},
        {"q": "Malabar Exercise involves navies of India, USA and?", "options": ["Russia", "France", "Japan", "Australia"], "ans": 2},
        {"q": "Rafale Marine jets are being procured for?", "options": ["IAF", "Indian Navy", "Indian Army", "Coast Guard"], "ans": 1},
    ]
}

WAT_WORDS = [
    "Leadership", "Courage", "Team", "Challenge", "Victory", "Duty", "Nation", "Sacrifice",
    "Initiative", "Discipline", "Honour", "Responsibility", "Mission", "Strength", "Unity",
    "Service", "Determination", "Integrity", "Valor", "Perseverance", "Command", "Defence",
    "Spirit", "Excellence", "Commitment", "Resilience", "Loyalty", "Pride", "Action", "Goal"
]

SRT_SITUATIONS = [
    "You are on a trek with your team and one member twists their ankle 10 km from the base camp. What do you do?",
    "You are the team leader and notice two team members are having a conflict that affects group performance. How do you handle it?",
    "During a group task, you realize your plan is not working but your teammates disagree. What do you do?",
    "You see a junior making a mistake during an important exercise. How do you respond?",
    "Your team has to complete a task in 30 minutes but it normally takes 1 hour. What is your approach?",
    "You are in an unfamiliar city and your wallet and phone are stolen. What do you do?",
    "Your immediate supervisor gives you an order you believe is incorrect. How do you react?",
    "You witness a road accident while on your way to an important exam. What do you do?",
    "Your team is demoralized after repeated failures in training. As a leader, what steps do you take?",
    "You have to give a presentation in 30 minutes but your notes are missing. What do you do?",
    "You discover that a close friend has cheated in an important test. How do you handle it?",
    "You are camping and a forest fire breaks out nearby. What actions do you take?",
]

TAT_SITUATIONS = [
    "A young man stands at a crossroads looking at two different paths ahead of him.",
    "A soldier sits alone at night looking at the horizon while his camp is in the background.",
    "A group of people are trying to climb a steep mountain together.",
    "A person is working late into the night while others sleep.",
    "A doctor attends to an injured person on a roadside.",
    "A team of workers are building something together under a tight deadline.",
    "A person stands at the top of a hill watching the sunrise.",
    "An elder person is teaching something to a group of young people.",
]

SSB_QUESTIONS = {
    "personal": [
        "Tell me about yourself and your family background.",
        "What are your strengths and weaknesses?",
        "Why do you want to join the Indian Armed Forces?",
        "Describe a difficult situation you faced and how you overcame it.",
        "What are your hobbies and how do they help you?",
        "Where do you see yourself in 10 years?",
        "What are your academic achievements?",
        "Tell me about a time when you showed leadership.",
    ],
    "defence": [
        "Name the current Chief of Defence Staff of India.",
        "What is the role of Indian Army in peacetime?",
        "Tell me about a recent military exercise India participated in.",
        "What do you know about Operation Sindoor?",
        "Name any 3 missiles in India's arsenal.",
        "What is the significance of Kargil War?",
        "Tell me about India's nuclear doctrine.",
        "What are Officer Like Qualities?",
    ],
    "current_affairs": [
        "What are the major security challenges facing India today?",
        "Tell me about India-China border situation.",
        "What is QUAD and its significance?",
        "Tell me about India's defence exports.",
        "What is Make in India initiative in defence?",
        "Tell me about India's space military capabilities.",
    ],
    "situation": [
        "Your patrol team is ambushed in a jungle. You are the senior most person. What are your orders?",
        "You are in charge of a flood relief operation. Resources are limited and many areas need help. How do you prioritize?",
        "A civilian approaches your check post with information about a terrorist hideout. How do you proceed?",
        "During training exercise, two of your soldiers have a physical fight. You are the NCO. What do you do?",
    ]
}

OLQ_QUESTIONS = [
    {"q": "When given a complex problem, I:", "opts": ["Wait for someone else to solve it", "Try to understand it but hesitate to act", "Analyze and take calculated action", "Act immediately with full confidence"], "trait": "Initiative"},
    {"q": "In a group discussion, I usually:", "opts": ["Stay silent and listen", "Speak when asked", "Contribute ideas regularly", "Lead the discussion effectively"], "trait": "Leadership"},
    {"q": "When I make a mistake, I:", "opts": ["Try to hide it", "Acknowledge but blame others", "Accept responsibility and learn", "Accept and immediately find solutions"], "trait": "Responsibility"},
    {"q": "Under pressure, I:", "opts": ["Panic and freeze", "Get anxious but manage", "Stay calm and focused", "Perform better and inspire others"], "trait": "Self_Confidence"},
    {"q": "In a team task, I:", "opts": ["Work only on my part", "Help if asked", "Actively cooperate with all", "Enhance team performance significantly"], "trait": "Team_Spirit"},
    {"q": "When meeting new people, I:", "opts": ["Avoid interaction", "Am polite but distant", "Am friendly and open", "Quickly build rapport and connect deeply"], "trait": "Social_Adaptability"},
    {"q": "My communication style is:", "opts": ["Very unclear, avoid speaking", "Sometimes unclear", "Clear and confident usually", "Always clear, persuasive and impactful"], "trait": "Communication"},
    {"q": "When facing a difficult decision, I:", "opts": ["Avoid deciding", "Take too long", "Decide after analysis", "Decide quickly with good reasoning"], "trait": "Speed_of_Decision"},
]

def get_quiz(category, num=5):
    pool = QUIZ_DATA.get(category, QUIZ_DATA["Defence"])
    return random.sample(pool, min(num, len(pool)))

def get_wat_word():
    return random.choice(WAT_WORDS)

def get_srt_situation():
    return random.choice(SRT_SITUATIONS)

def get_tat_situation():
    return random.choice(TAT_SITUATIONS)

def get_ssb_question(stage="personal"):
    questions = SSB_QUESTIONS.get(stage, SSB_QUESTIONS["personal"])
    return random.choice(questions)

def get_olq_questions():
    return OLQ_QUESTIONS

def analyze_olq(answers):
    """answers: list of int (0-3) for each OLQ question"""
    traits = {}
    for i, ans in enumerate(answers):
        if i < len(OLQ_QUESTIONS):
            trait = OLQ_QUESTIONS[i]["trait"]
            score = (ans / 3) * 10
            traits[trait] = round(score, 1)

    avg = sum(traits.values()) / len(traits) if traits else 0

    strengths = [t for t, s in traits.items() if s >= 7]
    improvements = [t for t, s in traits.items() if s < 5]

    report = {
        "scores": traits,
        "average": round(avg, 1),
        "strengths": strengths,
        "improvements": improvements,
        "recommendation": "Recommended" if avg >= 6 else "Needs Improvement"
    }
    return report

def calculate_bmi(height_cm, weight_kg):
    h = height_cm / 100
    bmi = weight_kg / (h * h)
    if bmi < 18.5:
        category = "Underweight"
        tip = "You need to gain healthy weight. Focus on high-protein diet and strength training."
    elif bmi < 25:
        category = "Normal - Ideal"
        tip = "Excellent! Maintain this weight. Keep up with your fitness routine."
    elif bmi < 30:
        category = "Overweight"
        tip = "Focus on cardio exercise and reduce caloric intake. Aim to lose 5-10% of body weight."
    else:
        category = "Obese"
        tip = "Consult a doctor and fitness expert. Create a structured diet and exercise plan."

    fitness_ready = "Yes" if 18.5 <= bmi <= 26 else "Needs Improvement"

    return {
        "bmi": round(bmi, 1),
        "category": category,
        "fitness_ready": fitness_ready,
        "tip": tip
    }
