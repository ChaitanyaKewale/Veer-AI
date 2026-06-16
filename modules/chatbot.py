"""
VeerAI Chatbot Engine
Uses ChatterBot as core conversational engine with fallback responses.
"""
import os
import re
import random

# ChatterBot integration with graceful fallback
try:
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
    CHATTERBOT_AVAILABLE = True
except ImportError:
    CHATTERBOT_AVAILABLE = False
    print("⚠️  ChatterBot not available. Using built-in response engine.")

DEFENCE_KB = {
    "nda": {
        "keywords": ["nda", "national defence academy", "khadakwasla"],
        "responses": [
            "NDA (National Defence Academy) is India's premier joint services training academy at Khadakwasla, Pune. It trains cadets for Army, Navy, and Air Force. Exam is conducted by UPSC twice yearly. Age: 16.5-19.5 years. Two papers: Maths (300 marks) and GAT (600 marks). SSB interview: 900 marks. Total: 1800 marks.",
            "To prepare for NDA: Study NCERT Maths (Class 11-12) thoroughly, read newspapers for current affairs, practice previous year papers. Physical fitness is equally important - run daily, practice pushups and situps. The GAT paper covers English, Physics, Chemistry, History, Geography and General Awareness."
        ]
    },
    "cds": {
        "keywords": ["cds", "combined defence services", "ima", "ota"],
        "responses": [
            "CDS (Combined Defence Services) is conducted by UPSC for graduates. Entries: IMA (Army), INA (Navy), AFA (Air Force), OTA (Officers Training Academy). Papers: English, GK, Elementary Maths (for IMA/INA/AFA). Negative marking: 1/3rd. After clearing, SSB interview follows.",
            "For CDS OTA, only English and GK papers are required. OTA trains Short Service Commission officers. IMA training is 18 months, producing Permanent Commission officers commissioned as Lieutenants in Indian Army."
        ]
    },
    "afcat": {
        "keywords": ["afcat", "air force", "flying branch", "ekt"],
        "responses": [
            "AFCAT (Air Force Common Admission Test) recruits officers for Indian Air Force in Flying, Technical, and Ground Duty branches. Conducted twice yearly. Syllabus: General Awareness, English, Numerical Ability, Reasoning. Technical candidates also take EKT (Engineering Knowledge Test).",
            "For AFCAT Flying Branch: Must be graduate with Physics and Maths at 10+2, age 20-24. After clearing AFCAT and AFSB (Air Force version of SSB), selected candidates undergo flying training at Air Force Academy, Dundigal."
        ]
    },
    "agniveer": {
        "keywords": ["agniveer", "agnipath", "4 year", "seva nidhi"],
        "responses": [
            "Agniveer is India's short-term military service scheme (2022). Duration: 4 years. Age: 17.5-21 years. After 4 years, 25% are retained as regular soldiers. Others receive Seva Nidhi of ~Rs 11.71 lakhs plus certificate, priority in CAPFs. Salary ranges from Rs 30,000 to Rs 40,000 per month.",
            "Agniveer recruitment process: Written exam based on education qualification, Physical Fitness Test (1.6km run, pullups, balance beam), Medical examination, and Document verification. Each service (Army/Navy/Air Force) has its own Agniveer recruitment process and trades."
        ]
    },
    "ssb": {
        "keywords": ["ssb", "services selection board", "interview", "io", "gto", "psychologist"],
        "responses": [
            "SSB Interview is a 5-day personality and psychology assessment at Services Selection Board centers. Day 1: OIR test + PPDT. Day 2: Psychology tests (TAT, WAT, SRT, SD). Day 3-4: GTO tasks (Group Discussion, Command Task, Obstacles). Day 5: Conference. About 20-25% are recommended.",
            "To succeed in SSB: Be genuine and consistent across all tests. Show initiative, leadership, and positive thinking. Prepare current affairs thoroughly. Practice WAT and SRT at home. Stay physically fit. Read biographies of military heroes. Have a clear understanding of why you want to join the forces."
        ]
    },
    "tat": {
        "keywords": ["tat", "thematic apperception", "story"],
        "responses": [
            "TAT (Thematic Apperception Test): 12 pictures shown (4 minutes each). Write a story with: background/situation, main character's thoughts/feelings, action taken, and outcome. Make stories positive, show initiative, leadership, problem-solving. Avoid tragedy, crime, or negative themes. The blank picture is your opportunity to show your ideal situation.",
            "TAT tips: Always have a hero who takes positive action. Show leadership and responsibility. Stories should have a beginning, middle, and positive end. Avoid repetitive themes. Include some diversity - social, professional, adventure situations. Time yourself: write 13-14 lines per story."
        ]
    },
    "wat": {
        "keywords": ["wat", "word association"],
        "responses": [
            "WAT (Word Association Test): 60 words shown (15 seconds each). Write one sentence that first comes to mind. Your sentences reveal your personality. Ensure your sentences are positive, show good values, initiative, and social awareness. Avoid negative sentences, crime, failure themes.",
            "WAT preparation: Practice with a friend showing you words randomly. Write positive, action-oriented sentences. Example - Word 'Courage': 'A brave soldier displayed courage by rescuing civilians.' Shows initiative and positive action. Avoid: 'Courage is needed to face fear' (too passive)."
        ]
    },
    "srt": {
        "keywords": ["srt", "situation reaction"],
        "responses": [
            "SRT (Situation Reaction Test): 60 situations in 30 minutes (30 seconds per situation). Write what YOU would do. Responses should show: initiative, responsibility, quick thinking, leadership, and care for others. Don't overthink - your first instinct often reflects your true personality.",
            "SRT tips: Always take action in your response (avoid 'I would think about it'). Show care for others alongside task completion. Accept responsibility as leader. Example: 'Accident on road → Stopped vehicle, called 112, administered first aid, managed traffic, stayed till help arrived.'"
        ]
    },
    "olq": {
        "keywords": ["olq", "officer like qualities", "leadership qualities"],
        "responses": [
            "Officer Like Qualities (OLQs) assessed in SSB: Effective Intelligence, Reasoning Ability, Organising Ability, Power of Expression, Social Adaptability, Cooperation, Sense of Responsibility, Initiative, Self Confidence, Speed of Decision, Ability to Influence Group, Liveliness, Determination, Courage, Stamina, Military Bearing. These 15 OLQs form the basis of SSB assessment.",
            "To develop OLQs: Read leadership books, participate in NCC/sports/debates, take initiative in daily life, join social service activities, practice public speaking, develop genuine interest in current affairs and defence. OLQs are personality traits that develop over years - start early!"
        ]
    },
    "fitness": {
        "keywords": ["fitness", "running", "pushup", "situp", "exercise", "bmi", "physical"],
        "responses": [
            "Defence Fitness Standards: 1.6 km run (under 7:30 mins for most entries), Pushups (40+), Situps (40+), Pullups (8+), Beam Balance. Start training 6 months before your exam. Progressive overload: increase reps/distance by 10% weekly. Focus on cardiovascular endurance and core strength.",
            "Fitness tips for aspirants: Morning: 5 km run (build gradually). Evening: Strength training (pushups, pullups, dips, planks). Weekly: One long run of 8-10 km. Diet: High protein, complex carbs, adequate hydration. Sleep 8 hours. Avoid alcohol and tobacco completely. Consistency beats intensity."
        ]
    },
    "brahmos": {
        "keywords": ["brahmos", "missile", "supersonic cruise"],
        "responses": [
            "BrahMos is a supersonic cruise missile jointly developed by India and Russia. Speed: Mach 2.8-3 (fastest cruise missile). Range: 290-500 km. Can be launched from land, sea, submarine, and air (Su-30MKI). It carries 200-300 kg warhead and uses sea-skimming trajectory. Named after Brahmaputra (India) and Moskva (Russia) rivers."
        ]
    },
    "ranks": {
        "keywords": ["rank", "colonel", "general", "admiral", "marshal", "lieutenant"],
        "responses": [
            "Indian Army Officer Ranks (lowest to highest): Second Lieutenant → Lieutenant → Captain → Major → Lieutenant Colonel → Colonel → Brigadier → Major General → Lieutenant General → General → Field Marshal (wartime honorary). JCO Ranks: Naib Subedar → Subedar → Subedar Major.",
            "Indian Navy Ranks: Sub Lieutenant → Lieutenant → Lieutenant Commander → Commander → Captain → Commodore → Rear Admiral → Vice Admiral → Admiral → Admiral of the Fleet. Air Force: Flying Officer → Flight Lieutenant → Squadron Leader → Wing Commander → Group Captain → Air Commodore → Air Vice Marshal → Air Marshal → Air Chief Marshal → Marshal of the Air Force."
        ]
    },
    "drdo": {
        "keywords": ["drdo", "defence research", "development"],
        "responses": [
            "DRDO (Defence Research and Development Organisation) is India's premier R&D agency under Ministry of Defence, established 1958. Major achievements: Agni/Prithvi/Akash/BrahMos missiles, LCA Tejas fighter, Arjun tank, INS Arihant submarine, Pinaka rocket system, INSAS rifle, Advanced Towed Artillery Gun System (ATAGS). It has 50+ labs across India."
        ]
    },
    "operation_sindoor": {
        "keywords": ["sindoor", "operation sindoor", "pahalgam", "pakistan strike", "2025 operation"],
        "responses": [
            "Operation Sindoor (May 2025): India's precision military operation targeting 9 terrorist camps in Pakistan and Pakistan-Occupied Kashmir (POK) in response to the Pahalgam terror attack which killed 26 civilians. The operation used precision-guided munitions and drones. It demonstrated India's resolve: zero tolerance for cross-border terrorism, measured but firm response."
        ]
    },
    "ins_vikrant": {
        "keywords": ["vikrant", "aircraft carrier", "ins vikrant"],
        "responses": [
            "INS Vikrant (IAC-1) is India's first indigenously designed and built aircraft carrier, commissioned in September 2022. Displacement: 45,000 tonnes. Operates MiG-29K fighters and helicopters. Built at Cochin Shipyard Limited at a cost of ~Rs 20,000 crore. It represents India's growing maritime power and Make in India success. It completes India's carrier fleet along with INS Vikramaditya."
        ]
    },
    "career": {
        "keywords": ["career", "entry", "join army", "join navy", "join air force", "how to join"],
        "responses": [
            "Major entries to join Indian Armed Forces as an Officer: NDA (10+2 pass, age 16.5-19.5), CDS (Graduate, age 19-25), AFCAT (Graduate, age 20-26), TES (10+2 with PCM 70%, age 16.5-19.5), NCC Special Entry (Graduate with NCC 'C' Certificate), Agniveer (10th/12th pass, age 17.5-21, 4-year contract).",
            "For best career in Indian Army: Join through NDA for permanent commission and senior rank. Study hard, clear UPSC NDA exam, pass SSB interview, complete 3-year NDA training and 1.5-year IMA training. You'll be commissioned as Lieutenant at ~21 years, with potential to become General by 55-58 years."
        ]
    }
}

GREETINGS = ["hello", "hi", "hey", "jai hind", "namaste", "good morning", "good evening", "greetings"]
GREETING_RESPONSES = [
    "Jai Hind! Welcome to VeerAI 🎖️ Your Personal Defence Mentor. I'm here to help you prepare for NDA, CDS, AFCAT, Agniveer, SSB, and more. What would you like to know?",
    "Jai Hind! I'm VeerAI, your AI-powered defence preparation assistant. Ask me anything about defence exams, SSB, career guidance, or current affairs!",
    "Hello Aspirant! 🫡 Ready to begin your defence preparation journey? I can help with NDA/CDS/AFCAT preparation, SSB guidance, fitness tips, and much more!"
]

FALLBACK_RESPONSES = [
    "I'm here to help with defence preparation! You can ask me about NDA, CDS, AFCAT, Agniveer, SSB interview, Indian Army/Navy/Air Force, defence technology, fitness guidance, or career paths. What would you like to know?",
    "That's an interesting question! For more specific information, try asking about: defence exams (NDA/CDS/AFCAT), SSB preparation, specific weapons/technology, ranks, military operations, or career guidance.",
    "I specialize in defence knowledge! Ask me about: exam patterns, SSB interview process, Officer Like Qualities, Indian Armed Forces history, defence technology, current affairs, or fitness tips for aspirants.",
]

class VeerAIBot:
    def __init__(self):
        self.chatbot = None
        self.initialized = False
        self._try_init_chatterbot()

    def _try_init_chatterbot(self):
        if not CHATTERBOT_AVAILABLE:
            print("Using built-in defence knowledge base.")
            self.initialized = True
            return

        try:
            db_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, 'chatterbot.sqlite3')

            self.chatbot = ChatBot(
                'VeerAI',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri=f'sqlite:///{db_path}',
                logic_adapters=[
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'default_response': 'I need more information to answer that.',
                        'maximum_similarity_threshold': 0.65
                    }
                ],
                read_only=False
            )
            self._train_chatterbot()
            self.initialized = True
            print("✅ ChatterBot initialized and trained!")
        except Exception as e:
            print(f"⚠️  ChatterBot init failed: {e}. Using built-in knowledge base.")
            self.chatbot = None
            self.initialized = True

    def _train_chatterbot(self):
        try:
            trainer = ListTrainer(self.chatbot)
            training_data = []
            for topic, data in DEFENCE_KB.items():
                for resp in data["responses"]:
                    for kw in data["keywords"]:
                        training_data.extend([f"Tell me about {kw}", resp])
            if training_data:
                trainer.train(training_data)
        except Exception as e:
            print(f"Training warning: {e}")

    def get_response(self, user_input):
        user_input_lower = user_input.lower().strip()

        # Check greetings
        if any(greet in user_input_lower for greet in GREETINGS):
            return random.choice(GREETING_RESPONSES)

        # Check defence knowledge base
        for topic, data in DEFENCE_KB.items():
            if any(kw in user_input_lower for kw in data["keywords"]):
                return random.choice(data["responses"])

        # Try ChatterBot if available
        if self.chatbot:
            try:
                response = str(self.chatbot.get_response(user_input))
                if len(response) > 20 and response != 'I need more information to answer that.':
                    return response
            except Exception:
                pass

        return random.choice(FALLBACK_RESPONSES)

# Singleton instance
_bot_instance = None

def get_bot():
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = VeerAIBot()
    return _bot_instance
