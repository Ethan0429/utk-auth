from canvasapi import Canvas
import bot_vars
import os


def catch_invalid_login_id(user):
    try:
        return str(user.login_id)
    except AttributeError:
        pass


def catch_invalid_login_name(user):
    try:
        username = str(user.name)
        first_last = username.split()
        username = first_last[0]+' ' + first_last[-1]
        return username
    except AttributeError:
        pass


def get_student_names():
    print('grabbing student names...')
    try:
        course = bot_vars.canvas.get_course(bot_vars.CANVAS_COURSE_URL_ID)
        full_names = [user.name for user in course.get_users()]
        # create student_names.txt file
        if not os.path.exists('student_names.txt'):
            with open('student_names.txt', 'w') as f:
                for name in full_names:
                    f.write(f"{name}\n")
                    print(f"{name}")

        nicknames = {catch_invalid_login_id(user): catch_invalid_login_name(
            user) for user in course.get_users()}
    except Exception as e:
        print(e)
        print('error grabbing student names')
        bot_vars.users = {}

    print('student names:')
    for key, value in bot_vars.users.items():
        print(key, value)

    return full_names, nicknames


class StudentDashboard:
    def __init__(self):
        self.canvas = bot_vars.canvas
        self.course_id = bot_vars.CANVAS_COURSE_URL_ID
        self.course = self.canvas.get_course(self.course_id)

    def get_user(self, username):
        return self.course.get_users(enrollment_type=['student'], include=[
            'enrollments'], search_term=username)

    def get_assignments(self, user):
        return user.get_assignments(course=self.course_id)

    def get_submissions(self, assignment):
        return assignment.get_submissions()

    def get_section(self, user_id):
        sections = self.course.get_sections(
            include=['students', 'enrollments'])
        for section in sections:
            for student in section.students:
                try:
                    if int(student['id']) == int(user_id):
                        return section
                except Exception as e:
                    print(e)
                    pass

    async def get_student_info(self, username):
        user = self.get_user(username)[0]
        assignments = self.get_assignments(user)
        submissions = [self.get_submissions(assignment)[0]
                       for assignment in assignments]
        section = self.get_section(user.id)

        data = {
            "student_id": user.id,
            "student_login_id": user.login_id,
            "student_name": user.name,
            "course_id": self.course_id,
            "course_name": self.course.name,
            "section_id": section.id,
            "section_name": section.name,
            "assignments": [],
        }

        for assignment, submission in zip(assignments, submissions):
            assignment_data = {
                "id": assignment.id,
                "name": assignment.name,
                "due_at": assignment.due_at,
                "submission": {
                    "attempt": submission.attempt,
                    "grade": submission.grade,
                    "score": submission.score,
                    "submitted_at": submission.submitted_at,
                    "late": submission.late,
                    "missing": submission.missing,
                    "points_deducted": submission.points_deducted,
                    "minutes_late": int(int(submission.seconds_late) / 60),
                },
            }
            assignment_data["submission"][
                "url"] = f"https://utk.instructure.com/courses/{bot_vars.CANVAS_COURSE_URL_ID}/assignments/{assignment_data['id']}"
            assignment_data["submission"][
                "submission_url"] = f"https://utk.instructure.com/courses/{bot_vars.CANVAS_COURSE_URL_ID}/assignments/{assignment_data['id']}/submissions/{data['student_id']}"
            data["assignments"].append(assignment_data)

        return data

    import os


# for debugging
def save_student_info_to_md(student_info, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_name = f"{student_info['student_name'].strip()}.md"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w") as md_file:
        md_file.write(f"# Student Information\n")
        md_file.write(f"\n")
        md_file.write(f"**Student ID**: {student_info['student_id']}\n")
        md_file.write(f"**Student Name**: {student_info['student_name']}\n")
        md_file.write(f"\n")
        md_file.write(
            f"**Student NetID**: {student_info['student_login_id']}\n")
        md_file.write(f"\n")
        md_file.write(f"## Course\n")
        md_file.write(f"\n")
        md_file.write(f"**Course ID**: {student_info['course_id']}\n")
        md_file.write(f"**Course Name**: {student_info['course_name']}\n")
        md_file.write(
            f"**Section ID**: {student_info['section_id']}\n**Section Name**: {student_info['section_name']}\n")
        md_file.write(f"\n")
        md_file.write(f"## Assignments\n")
        md_file.write(f"\n")

        for assignment in student_info["assignments"]:
            md_file.write(f"### {assignment['name']}\n")
            md_file.write(f"**URL**: {assignment['submission']['url']}\n")
            md_file.write(f"\n")
            md_file.write(
                f"**Submission URL**: {assignment['submission']['submission_url']}\n")
            md_file.write(f"\n")
            md_file.write(f"**ID**: {assignment['id']}\n")
            md_file.write(f"\n")
            md_file.write(f"**Description**: <snip>\n")
            md_file.write(f"\n")
            md_file.write(f"**Due At**: {assignment['due_at']}\n")
            md_file.write(f"\n")
            md_file.write(
                f"**Attempt**: {assignment['submission']['attempt']}\n")
            md_file.write(f"**Grade**: {assignment['submission']['grade']}\n")
            md_file.write(f"**Score**: {assignment['submission']['score']}\n")
            md_file.write(
                f"**Submitted At**: {assignment['submission']['submitted_at']}\n")
            md_file.write(f"**Late**: {assignment['submission']['late']}\n")
            md_file.write(
                f"**Missing**: {assignment['submission']['missing']}\n")
            md_file.write(
                f"**Points Deducted**: {assignment['submission']['points_deducted']}\n")
            md_file.write(
                f"**Minutes Late**: {assignment['submission']['minutes_late']}\n")
            md_file.write(f"\n")


def return_student_header(student_info):
    header_str = f"""
# Student Information

**Student ID**: {student_info['student_id']}

**Student Name**: {student_info['student_name']}

**Student NetID**: {student_info['student_login_id']}

## Course

**Course ID**: {student_info['course_id']}

**Course Name**: {student_info['course_name']}

**Section ID**: {student_info['section_id']}

**Section Name**: {student_info['section_name']}
"""

    return header_str


def return_assignment_info(data, assignment):
    assignment_str = f"""
# {data['student_name']}

## {assignment['name']}

**Assignment URL**: {assignment['submission']['url']}

**ID**: {assignment['id']}

**Description**: <snip>

**Due At**: {assignment['due_at']}

### Submission

**Submission URL**: {assignment['submission']['submission_url']}

**Attempt**: {assignment['submission']['attempt']}

**Grade**: {assignment['submission']['grade']}

**Score**: {assignment['submission']['score']}

**Submitted At**: {assignment['submission']['submitted_at']}

**Late**: {assignment['submission']['late']}

**Missing**: {assignment['submission']['missing']}

**Points Deducted**: {assignment['submission']['points_deducted']}

**Minutes Late**: {assignment['submission']['minutes_late']}

"""

    return assignment_str
