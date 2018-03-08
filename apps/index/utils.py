from grants.models import GrantCourse


def get_course_step_list(steps):
    courses = GrantCourse.objects.all().order_by('id')
    course_step_list = []
    for c in courses:
        course_steps = [
            s for s in steps
            if s.project.workflow.with_term_grant_course.grant_course == c]
        course_step_list.append((c, course_steps))
    return course_step_list
