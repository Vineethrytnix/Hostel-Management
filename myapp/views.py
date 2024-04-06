from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from .models import *

# Create your views here.
#Uploading to GIT

def index(request):
    return render(request, "index.html")


def log(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        user = authenticate(username=email, password=passw)

        print("Authentication ", user)
        if user is not None:
            print(user)
            login(request, user)
            if user.userType == "Administrator":
                return HttpResponse(
                    "<script>alert('Login As Admin'); window.location='/admin_home'</script>"
                )

            elif user.userType == "User":
                id = user.id
                email = user.username
                userType = user.userType
                request.session["uid"] = id
                request.session["type"] = userType
                request.session["email"] = email
                return HttpResponse(
                    "<script>alert('Login As User'); window.location='/user_home'</script>"
                )

            elif user.userType == "Guest":
                id = user.id
                email = user.username
                userType = user.userType
                request.session["uid"] = id
                request.session["type"] = userType
                request.session["email"] = email
                return HttpResponse(
                    "<script>alert('Login as Hosteller'); window.location='/hostel_home'</script>"
                )

            else:
                return HttpResponse(
                    "<script>alert('Type Not Specified'); window.location='/log'</script>"
                )

        else:
            return HttpResponse(
                "<script>alert('Invalid Credentials'); window.location='/log'</script>"
            )
    return render(request, "login.html")


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")
        password = request.POST.get("password")
        address = request.POST.get("address")
        image = request.FILES["image"]

        # Check if the email already exists in the User model
        if Login.objects.filter(username=email).exists():
            return HttpResponse(
                "<script>alert('Email already exists'); window.location='/user_reg'</script>"
            )
        else:
            new_user = Login.objects.create_user(
                username=email,
                password=password,
                viewPass=password,
                email=email,
                first_name=username,
                is_active=1,
                userType="User",
            )
            new_user.save()

            # Create a DoctorReg object and associate it with the new User
            if image:
                user_info = UserReg.objects.create(
                    name=username,
                    email=email,
                    phone=mobile_number,
                    address=address,
                    image=image,
                    loginid=new_user,
                )
                user_info.save()
                return HttpResponse(
                    "<script>alert('Successfully Registered'); window.location='/log'</script>"
                )
            else:
                user_info = UserReg.objects.create(
                    name=username,
                    email=email,
                    phone=mobile_number,
                    address=address,
                    loginid=new_user,
                )
                user_info.save()
                return HttpResponse(
                    "<script>alert('Successfully Registered'); window.location='/log'</script>"
                )
    return render(request, "user_reg.html")


def guest_register(request):
    if request.method == "POST":
        hostelname = request.POST.get("name")
        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")
        password = request.POST.get("password")
        address = request.POST.get("address")
        image = request.FILES["image"]

        # Check if the email already exists in the User model
        if Login.objects.filter(username=email).exists():
            return HttpResponse(
                "<script>alert('Email already exists'); window.location='/hosteller_reg'</script>"
            )
        else:
            new_user = Login.objects.create_user(
                username=email,
                password=password,
                viewPass=password,
                email=email,
                first_name=hostelname,
                is_active=1,
                userType="Guest",
            )
            new_user.save()

            # Create a DoctorReg object and associate it with the new User
            if image:

                hostel_info = Hosteller_reg.objects.create(
                    name=hostelname,
                    email=email,
                    phone=mobile_number,
                    address=address,
                    image=image,
                    loginid=new_user,
                )
                hostel_info.save()
                return HttpResponse(
                    "<script>alert('Successfully Registered'); window.location='/log'</script>"
                )
            else:
                hostel_info = Hosteller_reg.objects.create(
                    name=hostelname,
                    email=email,
                    phone=mobile_number,
                    address=address,
                    loginid=new_user,
                )
                hostel_info.save()
                return HttpResponse(
                    "<script>alert('Successfully Registered'); window.location='/log'</script>"
                )
    return render(request, "hostel_reg.html")


def user_index(request):
    return render(request, "User/index.html")


def admin_index(request):
    return render(request, "Admin/index.html")


def hostel_index(request):
    return render(request, "Guest/index.html")


def add_rooms(request):
    block = request.GET.get("bid")
    Bid = Blocks.objects.get(id=block)
    # view =Blocks.objects.filter(id=block)
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        adults = request.POST.get("adults")
        size = request.POST.get("size")
        rent_type = request.POST.get("rent_type")
        room_no = request.POST.get("room_no")
        images = request.FILES.getlist(
            "images"
        )  # Adjusted to getlist to handle multiple files
        description = request.POST.get("description")

        print("No IMAGES ", images)

        # Create the room instance but don't commit to database yet
        if images:
            room = Rooms(
                name=name,
                price=price,
                room_no=room_no,
                image=images[0],
                image2=images[1],
                image3=images[2],
                description=description,
                no_of_adults=adults,
                size=size,
                type=rent_type,
                block=Bid,
            )
            room.save()
            return HttpResponse(
                f"<script>alert('Successfully Added'); window.location='/add_rooms?bid={block}'</script>"
            )

    return render(request, "Admin/add_rooms.html", {"block": Bid})


def add_blocks(request):
    blocks = Blocks.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        block_no = request.POST.get("block_no")
        no_of_rooms = request.POST.get("no_of_rooms")
        images = request.FILES["images"]  # Adjusted to getlist to handle multiple files
        description = request.POST.get("description")

        # Create the block instance but don't commit to database yet
        block = Blocks(
            name=name,
            block_no=block_no,
            no_of_rooms=no_of_rooms,
            image=images,
            description=description,
        )
        block.save()  # Save the block to get an ID
    return render(request, "Admin/add_block.html", {"blocks": blocks})


def udp(request):
    change = Login.objects.filter(id=5,is_active=1)
    return HttpResponse("Success")


def delete_block(request):
    return HttpResponse("<scripts>alert('Deleted');window.location='/add_blocks'")


def view_room(request):
    view_room = Rooms.objects.all()

    return render(request, "Admin/view_rooms.html", {"view_room": view_room})


def add_events(request):
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        start_time = request.POST.get("stime")
        end_time = request.POST.get("etime")
        description = request.POST.get("description")
        images = request.FILES["image"]

        # Create the event instance but don't commit to database yet
        event = Events(
            name=name,
            date=date,
            image=images,
            start_time=start_time,
            end_time=end_time,
            description=description,
        )
        event.save()
        return HttpResponse(
            f"<script>alert('Event successfully added'); window.location='/add_events'</script>"
        )

    return render(request, "Admin/add_events.html")


def add_fees_structure(request):
    view = Fees_structure.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("price")

        event = Fees_structure(
            desc=name,
            price=amount,
        )
        event.save()
        return HttpResponse(
            f"<script>alert('New Fees Added'); window.location='/add_fees_structure'</script>"
        )

    return render(request, "Admin/add_fees_structure.html", {"view": view})


def view_event(request):
    events = Events.objects.all()
    return render(request, "Admin/view_event.html", {"events": events})


def add_mezz_details(request):
    if request.method == "POST":
        day = request.POST.get("day")
        breakfast = request.POST.get("BreakFast")
        lunch = request.POST.get("Lunch")
        dinner = request.POST.get("Dinner")

        # Create the event instance but don't commit to database yet
        event = Mess_food(
            day=day,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
        )
        event.save()  # Save the event to get an ID
        return HttpResponse(
            f"<script>alert('Mess details added'); window.location='/add_mezz_details'</script>"
        )

    return render(request, "Admin/add_mezz_details.html")


def view_users(request):
    users = UserReg.objects.all()
    return render(request, "Admin/view_users.html", {"users": users})


def delete_user(request):
    uid = request.GET.get("uid")
    print("uid", uid)
    # delet=Login.objects.filter(id=uid).delete()

    return HttpResponse(
        "<scripts>alert('Deleted');window.location='/view_users'</scripts>"
    )


def user_view_blocks(request):
    blocks = Blocks.objects.all()
    return render(request, "User/view_blocks.html", {"blocks": blocks})


def user_view_room(request):
    view_room = Rooms.objects.filter(type="Monthly Rent")

    return render(request, "User/view_rooms.html", {"view_room": view_room})


from datetime import datetime


def view_more(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)

    rid = request.GET.get("rid")
    Rid = Rooms.objects.get(id=rid)
    view = Rooms.objects.filter(id=rid)

    food = Mess_food.objects.all()
    
    fees=Fees_structure.objects.all()

    if request.POST:
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        price = request.POST.get("price")
        print("Price   =       =      =", price)

        check_out_date = datetime.strptime(check_out, "%m/%d/%Y")
        formatted_check_out = check_out_date.strftime("%Y-%m-%d")

        check_in_date = datetime.strptime(check_in, "%m/%d/%Y")
        formatted_check_in = check_in_date.strftime("%Y-%m-%d")

        date_diff = check_out_date - check_in_date
        days_between = date_diff.days

        print(f"The difference between check-in and check-out is: {days_between} days")

        amount = int(days_between) * int(price)

        insert = Room_booking.objects.create(
            check_in=formatted_check_in,
            check_out=formatted_check_out,
            uid=Uid,
            rid=Rid,
            amount=price,
            type="Monthly",
        )
        insert.save()
        return HttpResponse(
            f"<script>alert('Booked Successfully');window.location='/view_more?rid={rid}'</script>"
        )

    return render(request, "User/view_more.html", {"view": view, "food": food,"fees":fees})


def make_payment(request):
    bid = request.GET.get("bid")
    if request.method == "POST":
        Bid = Room_booking.objects.filter(id=bid).update(pay_status="Paid")
        return HttpResponse(
            "<script>alert('Payment Success');window.location='/user_view_bookings'</script>"
        )

    return render(request, "User/payment.html")


def delete_room(request):
    rid = request.GET.get("rid")
    delete_roo = Rooms.objects.filter(id=rid).delete()
    return HttpResponse(
        f"<script>alert('Room Details Deleted');window.location='/view_room'</script>"
    )


def view_booking(request):
    bookings = Room_booking.objects.filter(type="Daily")
    bookings2 = Room_booking.objects.filter(type="Monthly")

    return render(
        request, "Admin/view_bookings.html", {"Daily": bookings, "Monthly": bookings2}
    )


def update_bookings(request):
    bid = request.GET.get("bid")
    status = request.GET.get("status")

    if status == "approve":
        bookings = Room_booking.objects.filter(id=bid).update(status="approved")
        return HttpResponse(
            f"<script>alert('Booking Details Updated');window.location='/view_booking'</script>"
        )

    elif status == "decline":
        bookings = Room_booking.objects.filter(id=bid).update(status="declined")
        return HttpResponse(
            f"<script>alert('Booking Details Updated');window.location='/view_booking'</script>"
        )


def add_hosteller(request):
    uid = request.GET.get("uid")
    Uid = UserReg.objects.get(loginid=uid)
    bid = request.GET.get("bid")
    Bid = Room_booking.objects.get(id=bid)

    insert = Hosteller.objects.create(uid=Uid, bid=Bid, status="Hosteller")
    insert.save()
    up = Room_booking.objects.filter(id=bid).update(status="Hosteller")

    return HttpResponse(
        f"<script>alert('Hosteller Added');window.location='/view_booking'</script>"
    )


def adm_view_hosteller(request):
    adm_view = Hosteller.objects.all()
    return render(request, "Admin/view_hosteller.html", {"view": adm_view})


def add_attendance(request):
    uid = request.GET.get("uid")
    Uid = UserReg.objects.get(loginid=uid)

    if request.POST:
        date = request.POST["date"]

        insert = Attendance.objects.create(uid=Uid, date=date, status="Present")
        insert.save()
        return HttpResponse(
            f"<script>alert('Attendance Marked Successfully');window.location = '/adm_view_hosteller'</script>"
        )
    return render(request, "Admin/add_attendance.html", {"uid": Uid})


def view_mess_details(request):
    mess = Mess_food.objects.all()
    return render(request, "Admin/view_mess_details.html", {"view": mess})


def user_view_events(request):
    events = Events.objects.all()
    return render(request, "User/view_event.html", {"events": events})


def user_profile(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)

    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")
        password = request.POST.get("password")
        address = request.POST.get("address")
        image = request.FILES.get("image")

        if image:
            user_info = UserReg.objects.filter(loginid_id=uid).update(
                name=username,
                email=email,
                phone=mobile_number,
                address=address,
            )
            up_image = UserReg.objects.get(loginid=uid)
            up_image.image = image
            up_image.save()

            set_pass = Login.objects.get(id=uid)
            print("Passwored : ", set_pass)
            set_pass.set_password(password)
            set_pass.viewPass = password
            set_pass.save()

            return HttpResponse(
                "<script>alert('Profile Updated'); window.location='/user_profile'</script>"
            )
        else:
            user_inf = UserReg.objects.filter(loginid_id=uid).update(
                name=username,
                email=email,
                phone=mobile_number,
                address=address,
            )
            set_pass = Login.objects.get(id=uid)
            print("Passwored : ", set_pass)
            set_pass.password = password
            set_pass.viewPass = password
            set_pass.save()

            return HttpResponse(
                "<script>alert('Profile Updated'); window.location='/user_profile'</script>"
            )

    return render(request, "User/profile.html", {"uid": Uid})


def my_attendance(request):
    uid = request.session["uid"]
    # print("Attendance",uid)
    Uid = UserReg.objects.get(loginid=uid)
    view = Attendance.objects.filter(uid=uid)
    return render(request, "User/view_attendance.html", {"att": view})


def guest_view_event(request):
    events = Events.objects.all()
    return render(request, "User/view_event.html", {"events": events})


def guest_view_room(request):
    view_room = Rooms.objects.filter(type="Daily Rent")

    return render(request, "Guest/view_rooms.html", {"view_room": view_room})


def guest_view_more(request):
    uid = request.session["uid"]
    Uid = Hosteller_reg.objects.get(loginid=uid)

    rid = request.GET.get("rid")
    Rid = Rooms.objects.get(id=rid)
    view = Rooms.objects.filter(id=rid)

    food = Mess_food.objects.all()
    
    fees=Fees_structure.objects.all()

    if request.POST:
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        price = request.POST.get("price")
        print("Price   =       =      =", price)

        check_out_date = datetime.strptime(check_out, "%m/%d/%Y")
        formatted_check_out = check_out_date.strftime("%Y-%m-%d")

        check_in_date = datetime.strptime(check_in, "%m/%d/%Y")
        formatted_check_in = check_in_date.strftime("%Y-%m-%d")

        date_diff = check_out_date - check_in_date
        days_between = date_diff.days

        print(f"The difference between check-in and check-out is: {days_between} days")

        amount = int(days_between) * int(price)

        insert = Room_booking.objects.create(
            check_in=formatted_check_in,
            check_out=formatted_check_out,
            gid=Uid,
            rid=Rid,
            amount=amount,
            type="Daily",
        )
        insert.save()
        return HttpResponse(
            f"<script>alert('Booked Successfully');window.location='/guest_payment?rid={rid}'</script>"
        )

    return render(request, "Guest/view_more.html", {"view": view, "food": food,"fees":fees})


def guest_view_bookings(request):
    uid = request.session["uid"]
    Uid = Hosteller_reg.objects.get(loginid=uid)

    bookings = Room_booking.objects.filter(type="Daily", gid=Uid)
    print(bookings, "Bookings")
    return render(request, "Guest/guest_bookings.html", {"bookings": bookings})


def guest_add_feed(request):
    uid = request.session["uid"]
    Uid = Hosteller_reg.objects.get(loginid=uid)
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("review")

        feed = Feedback.objects.create(
            type="Guest", gid=Uid, rating=rating, comment=comment
        )
        feed.save()
        return HttpResponse(
            "<script>alert('feedback Added');window.location='/guest_view_room'</script>"
        )
    return render(request, "Guest/add_feedback.html")


def user_add_feed(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("review")

        feed = Feedback.objects.create(
            type="User", uid=Uid, rating=rating, comment=comment
        )
        feed.save()
        return HttpResponse(
            "<script>alert('feedback Added');window.location='/guest_view_room'</script>"
        )

    return render(request, "User/add_feedback.html")


def add_admin(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        new_user = Login.objects.create_user(
            username=email,
            password=passw,
            viewPass=passw,
            email=email,
            is_active=1,
            userType="User",
        )
    return render(request, "Admin/add_admin.html")


def user_view_bookings(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)

    bookings = Room_booking.objects.filter(type="Monthly", uid=Uid)
    print(bookings, "Bookings")
    return render(request, "User/user_bookings.html", {"bookings": bookings})


def user_apply_leave(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)
    if request.method == "POST":

        fromdate = request.POST["fromdate"]
        todate = request.POST["todate"]
        no_of_days = request.POST["no_of_days"]
        reason = request.POST["reason"]

        leave = Leave.objects.create(
            uid=Uid,
            fromdate=fromdate,
            todate=todate,
            no_of_days=no_of_days,
            reason=reason,
        )
        leave.save()
        return HttpResponse(
            "<script>alert('Leave Requested');window.location='/user_view_bookings'</script>"
        )

    return render(request, "User/leave_page.html")


def adm_view_leave(request):
    view = Leave.objects.all()
    return render(request, "Admin/view_leave_requests.html", {"view": view})


def leave_status(request):
    lid = request.GET.get("lid")
    status = request.GET.get("status")

    if status == "approve":
        leave = Leave.objects.get(id=lid)
        leave.status = "Approved"
        leave.save()
        return HttpResponse(
            "<script>alert('Leave Request Approved');window.location='/adm_view_leave'</script>"
        )
    elif status == "reject":
        leave = Leave.objects.get(id=lid)
        leave.status = "Rejected"
        leave.save()
        return HttpResponse(
            "<script>alert('Leave Request Rejected');window.location='/adm_view_leave'</script>"
        )
    elif status == "delete":
        leave = Leave.objects.get(id=lid)
        leave.delete()
        return HttpResponse(
            "<script>alert('Leave Request Deleted');window.location='/adm_view_leave'</script>"
        )


def user_leave_request(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)
    view = Leave.objects.filter(uid=Uid)
    return render(request, "User/leave_page.html", {"view": view})


def update_mess_details(request):
    mid = request.GET.get("mid")
    view = Mess_food.objects.get(id=mid)
    if request.method == "POST":
        day = request.POST.get("day")
        breakfast = request.POST.get("BreakFast")
        lunch = request.POST.get("Lunch")
        dinner = request.POST.get("Dinner")

        # Create the event instance but don't commit to database yet
        event = Mess_food.objects.filter(id=mid).update(
            day=day,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
        )  # Save the event to get an ID
        return HttpResponse(
            f"<script>alert('Mess details updated'); window.location='/view_mess_details'</script>"
        )

    return render(request, "Admin/update_mess_details.html", {"view": view})


def delete_mess_food(request):
    mid = request.GET.get("mid")
    event = Mess_food.objects.filter(id=mid).delete()

    return HttpResponse(
        f"<script>alert('Mess details Deleted'); window.location='/view_mess_details'</script>"
    )


def deleteEvent(request):
    eid = request.GET.get("eid")
    event = Events.objects.filter(id=eid).delete()

    return HttpResponse(
        f"<script>alert('Event Deleted'); window.location='/view_event'</script>"
    )


def update_Event(request):
    eid = request.GET.get("eid")
    view = Events.objects.get(id=eid)
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        start_time = request.POST.get("stime")
        end_time = request.POST.get("etime")
        description = request.POST.get("description")
        images = request.FILES["image"]

        # Create the event instance but don't commit to database yet
        if images:
            event = Events.objects.filter(id=eid).update(
                name=name,
                date=date,
                start_time=start_time,
                end_time=end_time,
                description=description,
            )
            up_image = Events.objects.get(id=eid)
            up_image.image = images
            up_image.save()

            return HttpResponse(
                f"<script>alert('Event Updated'); window.location='/view_event'</script>"
            )
        else:
            event = Events.objects.filter(id=eid).update(
                name=name,
                date=date,
                start_time=start_time,
                end_time=end_time,
                description=description,
            )
            return HttpResponse(
                f"<script>alert('Event Updated'); window.location='/view_event'</script>"
            )
    return render(request, "Admin/update_event.html", {"i": view})


def adm_view_feedback(request):
    view = Feedback.objects.all()
    return render(request, "Admin/view_feedback.html", {"view": view})


def delete_feed(request):
    fid = request.GET.get("fid")
    dele = Feedback.objects.filter(id=fid).delete()
    return HttpResponse(
        f"<script>alert('Feedback Deleted'); window.location='/adm_view_feedback'</script>"
    )


def guest_payment(request):
    bid = request.GET.get("bid")
    if request.method == "POST":
        Bid = Room_booking.objects.filter(id=bid).update(pay_status="Paid")
        return HttpResponse(
            "<script>alert('Payment Success');window.location='/guest_view_room'</script>"
        )
    return render(request, "Guest/payment.html")


def modify_fees(request):
    fid = request.GET.get("fid")
    status = request.GET.get("status")
    
    view=Fees_structure.objects.get(id=fid)
    print("Modified",view)
    if status == "update":
        if request.POST:
            name = request.POST.get("name")
            amount = request.POST.get("price")

            event = Fees_structure.objects.filter(id=fid).update(
                desc=name,
                price=amount,
            )
            event.save()
            return HttpResponse(
                f"<script>alert('New Fees Updated'); window.location='/add_fees_structure'</script>"
            )
            
    else:
        dele=Fees_structure.objects.filter(id=fid).delete()
        return HttpResponse(
            f"<script>alert('Fees Deleted'); window.location='/add_fees_structure'</script>"
        )
        
    return render(request, "Admin/modify_fees.html",{"view": view})
