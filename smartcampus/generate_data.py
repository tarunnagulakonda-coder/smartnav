import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcampus.settings')
django.setup()

from navigator.models import Block, Faculty, Topic

def generate_data():
    print("Clearing old data...")
    Topic.objects.all().delete()
    Faculty.objects.all().delete()
    Block.objects.all().delete()

    # ========================================
    # REAL MVGR CAMPUS BLOCKS FROM OpenStreetMap
    # ========================================
    print("Generating MVGR Campus Blocks (Real GPS from OSM)...")

    blocks_data = [
        # (Name, Department, Latitude, Longitude) — ALL FROM OSM
        ("ECE Block", "Electronics & Communication", 18.0601, 83.4056),
        ("CSE Block", "Computer Science", 18.0598, 83.4059),
        ("EEE Block", "Electrical & Electronics", 18.0604, 83.4054),
        ("Admin Block", "Administration", 18.0597, 83.4049),
        ("Central Library", "General", 18.0613591, 83.406179),
        ("Sport's Complex", "General", 18.0612084, 83.4066295),
        ("Chemistry LAB", "Science & Humanities", 18.0610073, 83.4048394),
        ("Laboratory", "Research", 18.0611452, 83.4042826),
        ("Workshop", "Mechanical Engineering", 18.0612127, 83.4040291),
        ("Mechanical Workshop 1", "Mechanical Engineering", 18.060542, 83.404166),
        ("Mechanical Workshop 2", "Mechanical Engineering", 18.0606262, 83.4039161),
        ("Open Auditorium", "General", 18.060515, 83.4043829),
        ("Department of English & Humanities", "Science & Humanities", 18.059311, 83.4052414),
        ("MVGR Boys Hostel Admin Block", "Hostel", 18.0588469, 83.4037689),
        ("Boys Hostel - A Block", "Hostel", 18.0585207, 83.4036687),
        ("Boys Hostel - B Block", "Hostel", 18.0591528, 83.4038422),
        ("Boys Hostel - C Block", "Hostel", 18.0589258, 83.4035035),
        ("MVGR Girls Hostel", "Hostel", 18.063291, 83.4059615),
        ("Girls Hostel B Block (2,3,4 years)", "Hostel", 18.0636766, 83.4060156),
        ("Girls Hostel Mess", "Hostel", 18.062954, 83.4058731),
        ("Juice Shop", "Canteen", 18.0613717, 83.4050463),
        ("Baker's Corner", "Canteen", 18.0608725, 83.4062643),
        ("Security Room", "General", 18.0592885, 83.4041955),
        ("Anjani Food Court", "Canteen", 18.0627944, 83.4048193),
    ]

    blocks = {}
    for name, dept, lat, lng in blocks_data:
        blk = Block.objects.create(
            block_name=name,
            department=dept,
            latitude=lat,
            longitude=lng
        )
        blocks[name] = blk

    # ========================================
    # REAL MVGR ECE FACULTY
    # ========================================
    print("Adding Real MVGR ECE Faculty...")

    ece_block = blocks["ECE Block"]

    ece_faculty = [
        ("Dr. M. Sunil Prakash", "EEE", "Signal Processing", "Professor & Dean", "Room 201"),
        ("Dr. D. Rama Devi", "EEE", "VLSI Design", "Professor & HOD", "Room 202"),
        ("Dr. G. Anjaneyulu", "EEE", "Embedded Systems", "Professor", "Room 203"),
        ("Dr. I. Kranthi Kiran", "EEE", "RF & Microwave Engineering", "Professor", "Room 204"),
        ("Dr. Lavanya Vadda", "EEE", "Image Processing", "Professor", "Room 205"),
        ("Dr. P. Ujjvala Kanthi Prabha", "EEE", "Communication Systems", "Professor", "Room 206"),
        ("Dr. Satyanarayana Moturi", "EEE", "Digital Electronics", "Professor", "Room 207"),
        ("Dr. Shaik Mastan Vali", "EEE", "Signal Processing", "Professor", "Room 208"),
        ("Dr. T. A. N. Surya Narayana Varma", "EEE", "Antenna Design", "Professor", "Room 209"),
        ("Dr. V. N. Lakshmana Kumar", "EEE", "Wireless Communications", "Professor", "Room 210"),
        ("Dr. P. Surya Prasad", "EEE", "VLSI Design", "Professor", "Room 211"),
        ("Dr. B. Lavanya", "EEE", "Image Processing", "Associate Professor", "Room 212"),
        ("Dr. B. Srinivas", "EEE", "Embedded Systems", "Associate Professor", "Room 213"),
        ("Dr. D. Raja Ramesh", "EEE", "Digital Signal Processing", "Associate Professor", "Room 214"),
        ("Dr. G. Vimala Kumari", "EEE", "Communication Systems", "Associate Professor", "Room 215"),
        ("Dr. K. Satyanarayana Raju", "EEE", "VLSI Design", "Associate Professor", "Room 216"),
        ("Dr. M. Laxmi Prasanna Rani", "EEE", "Embedded Systems", "Associate Professor", "Room 217"),
        ("Dr. Yogananda Patnaik", "EEE", "Microelectronics", "Associate Professor", "Room 218"),
        ("Kalakurasa Rakesh", "EEE", "Signal Processing", "Associate Professor (TP)", "Room 219"),
        ("N. Shanmukha Rao", "EEE", "Communication Systems", "Associate Professor (TP)", "Room 220"),
        ("U. N. Subhadra Devi", "EEE", "VLSI Design", "Associate Professor (TP)", "Room 221"),
        ("Ashok Kumar Adepu", "EEE", "Embedded Systems", "Distinguished Asst. Professor", "Room 222"),
        ("P. Pavan Kumar", "EEE", "Digital Electronics", "Distinguished Asst. Professor", "Room 223"),
        ("Naguboina Gopi Chand", "EEE", "VLSI Design", "Sr. Assistant Professor", "Room 224"),
        ("P. Divakara Varma", "EEE", "VLSI Design", "Sr. Assistant Professor", "Room 225"),
        ("S. Kumar", "EEE", "Communication Systems", "Sr. Assistant Professor", "Room 226"),
        ("Sudhansu Sekhar Behera", "EEE", "Signal Processing", "Sr. Assistant Professor", "Room 227"),
        ("K. V. Koteswara Rao", "EEE", "Embedded Systems", "Assistant Professor", "Room 228"),
        ("V. Appala Raju", "EEE", "Digital Electronics", "Assistant Professor", "Room 229"),
    ]

    status_options = ['Available', 'In Class', 'In Meeting']

    for name, dept, spec, designation, room in ece_faculty:
        fac = Faculty.objects.create(
            name=name,
            department=dept,
            specialization=f"{spec} ({designation})",
            cabin_block=ece_block,
            cabin_room=room,
            latitude=ece_block.latitude + random.uniform(-0.0003, 0.0003),
            longitude=ece_block.longitude + random.uniform(-0.0003, 0.0003),
            availability=random.choice(status_options)
        )

        topic_map = {
            "Signal Processing": ["Digital Signal Processing", "Adaptive Signal Processing"],
            "VLSI Design": ["VLSI Design", "Digital IC Design"],
            "Embedded Systems": ["Embedded Systems", "Microprocessors & Microcontrollers"],
            "Image Processing": ["Image Processing", "Computer Vision"],
            "Communication Systems": ["Analog Communications", "Digital Communications"],
            "Digital Electronics": ["Digital Electronics", "Logic Design"],
            "RF & Microwave Engineering": ["Microwave Engineering", "RF Circuit Design"],
            "Antenna Design": ["Antenna Theory", "Electromagnetic Fields"],
            "Wireless Communications": ["Wireless Communications", "Mobile Computing"],
            "Microelectronics": ["Microelectronics", "Semiconductor Devices"],
            "Digital Signal Processing": ["DSP Algorithms", "Signal Analysis"],
        }

        topics = topic_map.get(spec, [spec])
        for t in topics:
            Topic.objects.create(topic_name=t, faculty=fac)

    print("\nMVGR Real Data Loaded Successfully!")
    print(f"Blocks: {Block.objects.count()}")
    print(f"Faculty: {Faculty.objects.count()}")
    print(f"Topics: {Topic.objects.count()}")

if __name__ == "__main__":
    generate_data()
