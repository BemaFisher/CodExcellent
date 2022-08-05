from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from jinja2 import TemplateNotFound
from applications.student_enrollments import model
from applications.students import students_model
from applications.courses import courses_model

""" 
  Citation for the following HTML:
  Date: 07/27/2022
  Flask Blueprints
  Source URL: https://hackersandslackers.com/flask-blueprints
"""
student_enrollments_bp = Blueprint(
                          'student_enrollments_bp', 
                          __name__, 
                          template_folder='templates',
                          static_folder='static',
                          static_url_path='/applications/student_enrollments/static'
                        )


@student_enrollments_bp.get('/student_enrollments')
def index():
  try:
    student_enrollments = model.get()
    students = students_model.get()
    courses = courses_model.find_one('status', 1)
    return render_template(
            'student_enrollments.j2', 
            student_enrollments=student_enrollments,
            students=students,
            courses=courses,
            modal_title='Student Enrollments')
  except TemplateNotFound:
    abort(404)


@student_enrollments_bp.post('/student_enrollments')
def new():
  s_id = request.form.get('student_id')
  c_id = request.form.get('course_id')
  if not (s_id.isnumeric() and c_id.isnumeric()):
    flash("Please provide valid Student ID and Course ID.")
  else:
    model.create(s_id, c_id)
  return redirect(url_for('student_enrollments_bp.index'))


@student_enrollments_bp.get('/student_enrollments/<int:student_enrollment_id>')
def edit(student_enrollment_id):
  students = students_model.get()
  courses = courses_model.find_one('status', 1)
  student_enrollment = model.find_one('student_enrollment_id', student_enrollment_id)

  return render_template(
          'update.j2', 
          student_enrollment=student_enrollment[0],
          students=students,
          courses=courses
        )
  

@student_enrollments_bp.post('/student_enrollments/<int:student_enrollment_id>')
def update(student_enrollment_id):
  s_id = request.form.get('student_id')
  c_id = request.form.get('course_id')
  is_enrolled = request.form.get('is_enrolled')

  if not (s_id.isnumeric() and
          c_id.isnumeric() and
          is_enrolled.isnumeric()):
          flash('Please provide a valid Student Id, Course Id, and Enrollment Status')
          return redirect(url_for('student_enrollments_bp.edit', student_enrollment_id=student_enrollment_id))
  else: 
    model.update(student_enrollment_id, s_id, c_id, is_enrolled)
    return redirect(url_for('student_enrollments_bp.index'))


@student_enrollments_bp.delete("/student_enrollments/<int:student_enrollment_id>")
def delete(student_enrollment_id):
  model.delete(student_enrollment_id)
  return {student_enrollment_id: student_enrollment_id}
