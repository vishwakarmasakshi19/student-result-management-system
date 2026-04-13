from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *

# ================= INDEX =================
def index(request):
    return render(request, 'index.html')


# ================= LOGIN =================
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = "Invalid username or password"

    return render(request, 'admin_login.html', {'error': error})


# ================= DASHBOARD =================
@login_required
def admin_dashboard(request):
    context = {
        'student_count': Student.objects.count(),
        'subject_count': Subject.objects.count(),
        'class_count': Class.objects.count(),
        'result_count': Result.objects.count(),
    }

    return render(request, 'admin_dashboard.html', context)


# ================= LOGOUT =================
@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


# ================= CLASS =================
@login_required
def create_class(request):
    if request.method == 'POST':
        Class.objects.create(
            class_name=request.POST.get('classname'),
            class_numeric=request.POST.get('classnamenumeric'),
            section=request.POST.get('section')
        )
        messages.success(request, "Class Created Successfully")
        return redirect('create_class')

    return render(request, 'create_class.html')


@login_required
def manage_classes(request):
    classes = Class.objects.all()

    if request.GET.get('delete'):
        obj = get_object_or_404(Class, id=request.GET.get('delete'))
        obj.delete()
        messages.success(request, "Class deleted successfully")
        return redirect('manage_classes')

    return render(request, 'manage_classes.html', {'classes': classes})


@login_required
def edit_class(request, class_id):
    obj = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        obj.class_name = request.POST.get('classname')
        obj.class_numeric = request.POST.get('classnamenumeric')
        obj.section = request.POST.get('section')
        obj.save()

        messages.success(request, "Class Updated Successfully")
        return redirect('manage_classes')

    return render(request, 'edit_class.html', {'class_obj': obj})


# ================= SUBJECT =================
@login_required
def create_subject(request):
    if request.method == 'POST':
        Subject.objects.create(
            subject_name=request.POST.get('subjectname'),
            subject_code=request.POST.get('subjectcode')
        )
        messages.success(request, "Subject Created Successfully")
        return redirect('create_subject')

    return render(request, 'create_subject.html')


@login_required
def manage_subject(request):
    subjects = Subject.objects.all()

    if request.GET.get('delete'):
        obj = get_object_or_404(Subject, id=request.GET.get('delete'))
        obj.delete()
        messages.success(request, "Subject deleted successfully")
        return redirect('manage_subject')

    return render(request, 'manage_subject.html', {'subjects': subjects})


@login_required
def edit_subject(request, subject_id):
    obj = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        obj.subject_name = request.POST.get('subjectname')
        obj.subject_code = request.POST.get('subjectcode')
        obj.save()

        messages.success(request, "Subject Updated Successfully")
        return redirect('manage_subject')

    return render(request, 'edit_subject.html', {'subject_obj': obj})


# ================= SUBJECT COMBINATION =================
@login_required
def add_subject_combination(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        SubjectCombination.objects.create(
            student_class_id=request.POST.get('class'),
            subject_id=request.POST.get('subject'),
            status=1
        )
        messages.success(request, "Combination Added Successfully")
        return redirect('add_subject_combination')

    return render(request, 'add_subject_combination.html', {
        'classes': classes,
        'subjects': subjects
    })


@login_required
def manage_subject_combination(request):
    combination = SubjectCombination.objects.all()

    if request.GET.get('aid'):
        SubjectCombination.objects.filter(id=request.GET.get('aid')).update(status=1)
        messages.success(request, "Activated successfully")
        return redirect('manage_subject_combination')

    if request.GET.get('did'):
        SubjectCombination.objects.filter(id=request.GET.get('did')).update(status=0)
        messages.success(request, "Deactivated successfully")
        return redirect('manage_subject_combination')

    return render(request, 'manage_subject_combination.html', {'combination': combination})


# ================= STUDENT =================
@login_required
def add_student(request):
    classes = Class.objects.all()

    if request.method == 'POST':
        student_class = Class.objects.get(id=request.POST.get('class'))

        Student.objects.create(
            name=request.POST.get('fullname'),
            roll_id=request.POST.get('rollid'),
            email=request.POST.get('email'),
            gender=request.POST.get('gender'),
            student_class=student_class
        )

        messages.success(request, "Student added successfully")
        return redirect('add_student')

    return render(request, 'add_student.html', {'classes': classes})


@login_required
def manage_student(request):
    students = Student.objects.select_related('student_class').all()

    if request.GET.get('delete'):
        student = get_object_or_404(Student, id=request.GET.get('delete'))
        student.delete()
        messages.success(request, "Student deleted successfully")
        return redirect('manage_student')

    return render(request, 'manage_student.html', {'students': students})


# ================= NOTICE =================
@login_required
def add_notice(request):
    if request.method == 'POST':
        Notice.objects.create(
            title=request.POST.get('title'),
            detail=request.POST.get('details')
        )
        messages.success(request, "Notice added successfully")
        return redirect('add_notice')

    return render(request, 'add_notice.html')


@login_required
def manage_notice(request):
    notice = Notice.objects.all()

    if request.GET.get('delete'):
        obj = get_object_or_404(Notice, id=request.GET.get('delete'))
        obj.delete()
        messages.success(request, "Notice deleted successfully")
        return redirect('manage_notice')

    return render(request, 'manage_notice.html', {'notice': notice})


# ================= RESULT =================
@login_required
def add_result(request):
    classes = Class.objects.all()

    if request.method == 'POST':
        try:
            student_id = request.POST.get('student')
            student = Student.objects.get(id=student_id)

            for key, value in request.POST.items():
                if key.startswith('marks_') and value:
                    subject_id = key.split('_')[1]
                    subject = Subject.objects.get(id=subject_id)

                    Result.objects.create(
                        student=student,
                        student_class=student.student_class,
                        subject=subject,
                        marks=value
                    )

            messages.success(request, "Result added successfully")
            return redirect('add_result')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('add_result')

    return render(request, 'add_result.html', {'classes': classes})


# ================= MANAGE RESULT =================

@login_required
def manage_result(request):

    # ✅ DELETE LOGIC
    if request.method == "POST":
        delete_id = request.POST.get('delete_id')

        if delete_id:
            Result.objects.filter(student_id=delete_id).delete()
            messages.success(request, "Deleted successfully")
            return redirect('manage_result')

    # ✅ DATA FETCH (ALWAYS RUN)
    students = Student.objects.all()
    final_data = []

    for student in students:
        results = Result.objects.filter(student=student)

        total = sum(int(r.marks) for r in results)
        count = results.count()
        percentage = (total / count) if count > 0 else 0

        result_status = "Pass"
        for r in results:
            if int(r.marks) < 33:
                result_status = "Fail"
                break

        final_data.append({
            "student": student,
            "results": results,
            "total": total,
            "percentage": round(percentage, 2),
            "result_status": result_status
        })

    return render(request, "manage_result.html", {"data": final_data})

def edit_result(request, stid):
   
    student = get_object_or_404(Student, id=stid)
    results = Result.objects.filter(student=student).select_related('subject')
    if request.method == 'POST':
        ids = request.POST.getlist('id[]')
        marks_list = request.POST.getlist('marks[]')

        for id_val, mark in zip(ids, marks_list):
            result_obj = get_object_or_404(Result, id=id_val)
            result_obj.marks = mark
            result_obj.save()

        messages.success(request, 'Result updated successfully')
        return redirect('edit_result', stid=student.id)

    return render(request, 'edit_result.html', {
        'student': student,
        'results': results
    })

from django.contrib.auth import update_session_auth_hash 

@login_required
def change_password(request):
    if request.method == 'POST':
        old = request.POST['old_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        # Step 1: Check new & confirm password
        if new != confirm:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('change_password')

        # Step 2: Authenticate old password
        user = authenticate(username=request.user.username, password=old)

        if user:
            user.set_password(new)
            user.save()

            # Keep user logged in
            update_session_auth_hash(request, user)

            messages.success(request, 'Password updated successfully')
            return redirect('change_password')
        else:
            messages.error(request, 'Old password is incorrect')
            return redirect('change_password')

    return render(request, 'change_password.html')

from django.shortcuts import render
from django.contrib import messages
from .models import *

def search_result(request):
    classes = Class.objects.all()

    student = None
    results = None
    total_marks = 0
    percentage = 0
    grade = ""
    status = ""

    if request.method == 'POST':
        rollid = request.POST.get('rollid')
        class_id = request.POST.get('class')

        try:
            # Get student
            student = Student.objects.get(
                roll_id=rollid,
                student_class_id=class_id
            )

            # Get results
            results = Result.objects.filter(student=student)

            # Calculate total
            total_marks = sum(int(r.marks) for r in results)

            subject_count = results.count()
            max_total = subject_count * 100

            # Percentage
            percentage = (total_marks / max_total) * 100 if max_total > 0 else 0
            percentage = round(percentage, 2)

            # Grade
            if percentage >= 90:
                grade = 'A+'
            elif percentage >= 75:
                grade = 'A'
            elif percentage >= 60:
                grade = 'B'
            elif percentage >= 50:
                grade = 'C'
            else:
                grade = 'F'

            # Pass/Fail
            status = "Pass" if percentage >= 40 else "Fail"

        except Student.DoesNotExist:
            messages.error(request, "Student not found")

    return render(request, 'search_result.html', {
        'classes': classes,
        'student': student,
        'results': results,
        'total_marks': total_marks,
        'percentage': percentage,
        'grade': grade,
        'status': status
    })

from django.contrib import messages
from django.shortcuts import render, redirect
def check_result(request):
    if request.method == 'POST':
        rollid = request.POST.get('rollid')
        class_id = request.POST.get('class')

        try:
            student = Student.objects.filter(
                roll_id=rollid,
                student_class_id=class_id
            ).first()   # ✅ FIX

            if not student:
                messages.error(request, "No result found")
                return redirect('search_result')

            results = Result.objects.filter(student=student)

            total_marks = sum(int(r.marks) for r in results)
            subject_count = results.count()
            max_total = subject_count * 100

            percentage = (total_marks / max_total) * 100 if max_total > 0 else 0
            percentage = round(percentage, 2)

            return render(request, 'result_page.html', {
                'student': student,
                'results': results,
                'total_marks': total_marks,
                'percentage': percentage,
                'max_total': max_total
            })

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('search_result')

    return redirect('search_result')

# ✅ NOW OUTSIDE (VERY IMPORTANT)
from django.http import JsonResponse
from .models import Student, SubjectCombination

def get_student_subjects(request):
    class_id = request.GET.get('class_id')

    # ❗ Step 1: Check if class_id exists
    if not class_id:
        return JsonResponse({'students': [], 'subjects': []})

    # ✅ Step 2: Get students
    students = list(
        Student.objects.filter(student_class_id=class_id)
        .values('id', 'name', 'roll_id')
    )

    # ✅ Step 3: Get subjects from combination
    subject_combinations = SubjectCombination.objects.filter(
        student_class_id=class_id,
        status=1
    ).select_related('subject')

    subjects = []
    for sc in subject_combinations:
        subjects.append({
            'id': sc.subject.id,
            'name': sc.subject.subject_name
        })

    # ✅ Step 4: Return JSON response
    return JsonResponse({
        'students': students,
        'subjects': subjects
    })

def result_page(request):
    return render(request, 'result_page.html')