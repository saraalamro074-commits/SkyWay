from flask import Flask, request, redirect, render_template_string
import mysql.connector
from datetime import datetime


app = Flask(__name__)


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="skyway_db"
    )


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    return render_template_string(
        open("templates/index.html", encoding="utf-8").read()
    )


# =========================
# FLIGHTS PAGE
# =========================

@app.route("/flights")
def flights():

    return render_template_string(
        open("templates/flights.html", encoding="utf-8").read()
    )


# =========================
# BOOKING PAGE
# =========================

@app.route("/booking")
def booking():

    return render_template_string(
        open("templates/booking.html", encoding="utf-8").read()
    )


# =========================
# BOOKING SUCCESS
# =========================

@app.route("/booking-success", methods=["POST"])
def booking_success():

    passenger_name = request.form["passenger_name"]
    phone = request.form["phone"]
    email = request.form["email"]
    passport = request.form["passport"]
    passengers = request.form["passengers"]
    flight = request.form["flight"]

    booking_date = datetime.now()


    # Connect to database

    conn = get_db_connection()

    cursor = conn.cursor()


    # Save booking

    cursor.execute("""
        INSERT INTO bookings
        (
            passenger_name,
            phone,
            email,
            passport,
            passengers,
            flight,
            booking_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        passenger_name,
        phone,
        email,
        passport,
        passengers,
        flight,
        booking_date
    ))


    conn.commit()


    # Get booking ID

    booking_id = cursor.lastrowid


    cursor.close()
    conn.close()


    # =========================
    # TICKET PAGE
    # =========================

    return f"""
<!DOCTYPE html>

<html lang="ar" dir="rtl">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>تم تأكيد الحجز - SkyWay</title>


    <style>

        * {{
            box-sizing: border-box;
        }}


        body {{

            margin: 0;

            font-family: Arial, sans-serif;

            background:
                linear-gradient(
                    135deg,
                    #e0f2fe,
                    #f8fafc
                );

            color: #164e63;

            min-height: 100vh;
        }}


        /* =========================
           MENU BUTTON
        ========================= */

        .menu-button {{

            position: fixed;

            top: 20px;
            right: 20px;

            width: 50px;
            height: 50px;

            border: none;

            border-radius: 12px;

            background: #164e63;

            color: white;

            font-size: 25px;

            cursor: pointer;

            z-index: 1001;

            box-shadow:
                0 5px 15px
                rgba(0,0,0,0.15);
        }}


        .menu-button:hover {{
            background: #0e7490;
        }}


        /* =========================
           SIDE MENU
        ========================= */

        .side-menu {{

            position: fixed;

            top: 0;

            right: -300px;

            width: 280px;

            height: 100vh;

            background: white;

            box-shadow:
                -5px 0 25px
                rgba(0,0,0,0.15);

            z-index: 1000;

            padding: 30px 20px;

            transition: right 0.3s ease;
        }}


        .side-menu.open {{
            right: 0;
        }}


        .side-logo {{

            text-align: center;

            font-size: 28px;

            font-weight: bold;

            color: #164e63;

            margin-bottom: 40px;
        }}


        .menu-item {{

            display: block;

            padding: 15px;

            margin-bottom: 10px;

            border-radius: 10px;

            color: #164e63;

            text-decoration: none;

            font-size: 16px;

            font-weight: bold;

            transition: 0.2s;
        }}


        .menu-item:hover {{

            background: #e0f2fe;

            color: #0e7490;
        }}


        .menu-admin {{

            margin-top: 20px;

            background: #164e63;

            color: white;
        }}


        .menu-admin:hover {{

            background: #0e7490;

            color: white;
        }}


        /* =========================
           OVERLAY
        ========================= */

        .overlay {{

            position: fixed;

            top: 0;

            left: 0;

            width: 100%;

            height: 100%;

            background:
                rgba(0,0,0,0.35);

            z-index: 999;

            display: none;
        }}


        .overlay.show {{
            display: block;
        }}


        /* =========================
           TICKET
        ========================= */

        .container {{

            width: 90%;

            max-width: 700px;

            margin: 80px auto 40px;
        }}


        .ticket {{

            background: white;

            border-radius: 20px;

            padding: 35px;

            box-shadow:
                0 10px 35px
                rgba(0,0,0,0.12);

            border-top:
                7px solid #164e63;
        }}


        .success {{

            text-align: center;

            font-size: 22px;

            font-weight: bold;

            color: #15803d;

            margin-bottom: 10px;
        }}


        .logo {{

            text-align: center;

            font-size: 32px;

            font-weight: bold;

            color: #164e63;

            margin-bottom: 5px;
        }}


        .subtitle {{

            text-align: center;

            color: #64748b;

            margin-bottom: 30px;
        }}


        .booking-number {{

            background: #e0f2fe;

            padding: 15px;

            border-radius: 10px;

            text-align: center;

            font-weight: bold;

            margin-bottom: 25px;
        }}


        .info {{

            display: grid;

            grid-template-columns: 1fr 1fr;

            gap: 15px;

            margin-top: 20px;
        }}


        .info-box {{

            background: #f8fafc;

            padding: 15px;

            border-radius: 10px;

            border:
                1px solid #e2e8f0;
        }}


        .label {{

            font-size: 13px;

            color: #64748b;

            margin-bottom: 5px;
        }}


        .value {{

            font-weight: bold;

            color: #164e63;

            word-break: break-word;
        }}


        .flight-box {{

            background: #164e63;

            color: white;

            padding: 20px;

            border-radius: 12px;

            text-align: center;

            font-size: 20px;

            font-weight: bold;

            margin: 25px 0;
        }}


        .buttons {{

            display: flex;

            gap: 12px;

            margin-top: 25px;
        }}


        .btn {{

            flex: 1;

            display: block;

            text-align: center;

            text-decoration: none;

            padding: 13px;

            border-radius: 9px;

            font-weight: bold;
        }}


        .btn-home {{

            background: #164e63;

            color: white;
        }}


        .btn-flights {{

            background: #e0f2fe;

            color: #164e63;
        }}


        @media (max-width: 600px) {{

            .container {{
                width: 94%;
            }}

            .ticket {{
                padding: 25px 18px;
            }}

            .info {{
                grid-template-columns: 1fr;
            }}

            .buttons {{
                flex-direction: column;
            }}

            .side-menu {{
                width: 260px;
            }}

        }}

    </style>

</head>


<body>


    <!-- MENU BUTTON -->

    <button
        class="menu-button"
        onclick="openMenu()"
    >
        ☰
    </button>


    <!-- SIDE MENU -->

    <div
        class="side-menu"
        id="sideMenu"
    >

        <div class="side-logo">
            ✈️ SkyWay
        </div>


        <a
            href="/"
            class="menu-item"
        >
            🏠 الرئيسية
        </a>


        <a
            href="/flights"
            class="menu-item"
        >
            ✈️ الرحلات
        </a>


        <a
            href="/booking"
            class="menu-item"
        >
            🎫 حجز جديد
        </a>


        <a
            href="/admin"
            class="menu-item menu-admin"
        >
            📊 لوحة الإدارة
        </a>

    </div>


    <!-- OVERLAY -->

    <div
        class="overlay"
        id="overlay"
        onclick="closeMenu()"
    ></div>


    <!-- TICKET -->

    <div class="container">

        <div class="ticket">


            <div class="success">
                ✅ تم تأكيد الحجز بنجاح!
            </div>


            <div class="logo">
                ✈️ SkyWay
            </div>


            <div class="subtitle">
                تذكرة السفر الإلكترونية
            </div>


            <div class="booking-number">
                🎫 رقم الحجز: #{booking_id}
            </div>


            <div class="flight-box">
                ✈️ {flight}
            </div>


            <div class="info">


                <div class="info-box">

                    <div class="label">
                        اسم المسافر
                    </div>

                    <div class="value">
                        {passenger_name}
                    </div>

                </div>


                <div class="info-box">

                    <div class="label">
                        رقم الهاتف
                    </div>

                    <div class="value">
                        {phone}
                    </div>

                </div>


                <div class="info-box">

                    <div class="label">
                        البريد الإلكتروني
                    </div>

                    <div class="value">
                        {email}
                    </div>

                </div>


                <div class="info-box">

                    <div class="label">
                        رقم جواز السفر
                    </div>

                    <div class="value">
                        {passport}
                    </div>

                </div>


                <div class="info-box">

                    <div class="label">
                        عدد المسافرين
                    </div>

                    <div class="value">
                        {passengers}
                    </div>

                </div>


                <div class="info-box">

                    <div class="label">
                        تاريخ الحجز
                    </div>

                    <div class="value">
                        {booking_date.strftime("%Y-%m-%d %H:%M")}
                    </div>

                </div>


            </div>


            <div class="buttons">

                <a
                    href="/"
                    class="btn btn-home"
                >
                    🏠 الرئيسية
                </a>


                <a
                    href="/flights"
                    class="btn btn-flights"
                >
                    ✈️ الرحلات
                </a>

            </div>


        </div>

    </div>


    <script>

        function openMenu() {{

            document
                .getElementById("sideMenu")
                .classList
                .add("open");

            document
                .getElementById("overlay")
                .classList
                .add("show");

        }}


        function closeMenu() {{

            document
                .getElementById("sideMenu")
                .classList
                .remove("open");

            document
                .getElementById("overlay")
                .classList
                .remove("show");

        }}

    </script>


</body>

</html>
"""


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
def admin():

    search = request.args.get("search", "").strip()


    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)


    if search:

        query = """
            SELECT *
            FROM bookings
            WHERE
                CAST(id AS CHAR) LIKE %s
                OR passenger_name LIKE %s
                OR phone LIKE %s
                OR email LIKE %s
                OR passport LIKE %s
                OR flight LIKE %s
            ORDER BY id DESC
        """

        value = f"%{search}%"

        cursor.execute(
            query,
            (
                value,
                value,
                value,
                value,
                value,
                value
            )
        )

    else:

        cursor.execute("""
            SELECT *
            FROM bookings
            ORDER BY id DESC
        """)


    bookings = cursor.fetchall()


    # Total bookings

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM bookings
    """)

    total_bookings = cursor.fetchone()["total"]


    # Total passengers

    cursor.execute("""
        SELECT COALESCE(SUM(passengers), 0) AS total
        FROM bookings
    """)

    total_passengers = cursor.fetchone()["total"]


    cursor.close()
    conn.close()


    return render_template_string(
        open("templates/admin.html", encoding="utf-8").read(),
        bookings=bookings,
        total_bookings=total_bookings,
        total_passengers=total_passengers,
        search=search
    )


# =========================
# BOOKING DETAILS
# =========================

@app.route("/admin/booking/<int:booking_id>")
def booking_details(booking_id):

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)


    cursor.execute("""
        SELECT *
        FROM bookings
        WHERE id = %s
    """, (booking_id,))


    booking = cursor.fetchone()


    cursor.close()
    conn.close()


    if not booking:

        return """
        <h2 style="text-align:center;">
            الحجز غير موجود
        </h2>

        <p style="text-align:center;">
            <a href="/admin">
                العودة إلى لوحة الإدارة
            </a>
        </p>
        """


    return f"""
<!DOCTYPE html>

<html lang="ar" dir="rtl">

<head>

    <meta charset="UTF-8">

    <title>تفاصيل الحجز - SkyWay</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            background: #f2f6fa;
            color: #164e63;
            padding: 30px;
        }}

        .box {{
            max-width: 650px;
            margin: 30px auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        h1 {{
            text-align: center;
        }}

        .row {{
            padding: 15px;
            margin-bottom: 10px;
            background: #f8fafc;
            border-radius: 8px;
        }}

        .back {{
            display: block;
            text-align: center;
            margin-top: 20px;
            color: #164e63;
            text-decoration: none;
            font-weight: bold;
        }}

    </style>

</head>

<body>

    <div class="box">

        <h1>
            🎫 تفاصيل الحجز
        </h1>


        <div class="row">
            <strong>رقم الحجز:</strong>
            {booking["id"]}
        </div>


        <div class="row">
            <strong>اسم المسافر:</strong>
            {booking["passenger_name"]}
        </div>


        <div class="row">
            <strong>الهاتف:</strong>
            {booking["phone"]}
        </div>


        <div class="row">
            <strong>البريد الإلكتروني:</strong>
            {booking["email"]}
        </div>


        <div class="row">
            <strong>جواز السفر:</strong>
            {booking["passport"]}
        </div>


        <div class="row">
            <strong>عدد المسافرين:</strong>
            {booking["passengers"]}
        </div>


        <div class="row">
            <strong>الرحلة:</strong>
            {booking["flight"]}
        </div>


        <div class="row">
            <strong>تاريخ الحجز:</strong>
            {booking["booking_date"]}
        </div>


        <a
            href="/admin"
            class="back"
        >
            ← العودة إلى لوحة الإدارة
        </a>

    </div>

</body>

</html>
"""


# =========================
# DELETE BOOKING
# =========================

@app.route("/admin/delete/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id):

    conn = get_db_connection()

    cursor = conn.cursor()


    cursor.execute("""
        DELETE FROM bookings
        WHERE id = %s
    """, (booking_id,))


    conn.commit()


    cursor.close()
    conn.close()


    return redirect("/admin")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )

