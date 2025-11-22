# FINAL SEED SYSTEM BIOSKOP (Updated with weekday for Jadwal & Orders)
# - Row kursi: A1, A2, B3, ...
# - 6 Movies fixed
# - 3 tayang/hari (1-31 Desember 2024)
# - Promo_name + discount
# - Anti double booking
# - Orders default 1200
# - transaction_date + weekday on jadwal & orders

from sqlalchemy import (
    create_engine, Column, Integer, String, Date, Time, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker
from faker import Faker
import random, datetime, uuid, sys, time

DB_URL = "mysql+pymysql://root:%40Keju1234@localhost:3306/bioskop"

Base = declarative_base()
fake = Faker("id_ID")

NUM_STUDIOS = 5
NUM_MEMBERS = 100
ORDERS_TO_GENERATE = 1200
MIN_ROWS = 8
MIN_COLS = 6

WEEKDAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

def get_weekday(date_obj):
    return WEEKDAYS[date_obj.weekday()]

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    genre = Column(String(100))
    durasi = Column(Integer)
    price = Column(Integer)

class Studio(Base):
    __tablename__ = "studios"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    rows = Column(Integer)
    cols = Column(Integer)

class StudioSeat(Base):
    __tablename__ = "studio_seats"
    id = Column(Integer, primary_key=True)
    studio_id = Column(Integer, ForeignKey("studios.id"))
    row = Column(String(5))
    col = Column(Integer)
    __table_args__ = (UniqueConstraint("studio_id", "row", "col", name="uq_studio_row_col"),)

class Membership(Base):
    __tablename__ = "memberships"
    id = Column(Integer, primary_key=True)
    nama = Column(String(255))

class Jadwal(Base):
    __tablename__ = "jadwal"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer)
    studio_id = Column(Integer)
    tanggal = Column(Date)
    jam = Column(Time)
    weekday = Column(String(20))

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_code = Column(String(20))
    membership_id = Column(Integer)
    jadwal_id = Column(Integer)
    payment_method = Column(String(40))
    seat_count = Column(Integer)
    discount = Column(Integer)
    promo_name = Column(String(255))
    total_price = Column(Integer)
    final_price = Column(Integer)
    created_at = Column(DateTime)
    transaction_date = Column(Date)
    weekday = Column(String(20))

class OrderSeat(Base):
    __tablename__ = "order_seats"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    jadwal_id = Column(Integer)
    studio_id = Column(Integer)
    row = Column(String(5))
    col = Column(Integer)
    __table_args__ = (UniqueConstraint("jadwal_id", "studio_id", "row", "col", name="uq_jadwal_studio_row_col"),)


def seat_available(session, jid, studio, r, c):
    q = session.query(OrderSeat).filter_by(
        jadwal_id=jid, studio_id=studio, row=r, col=c
    ).first()
    return q is None

def ticket_price(dur):
    if dur >= 180: return 50000
    if dur >= 150: return 45000
    return 40000

def random_december_date():
    day = random.randint(1, 31)
    return datetime.date(2024, 12, day)

engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

def main():
    print("== START SEEDING ==")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = Session()

    films = [
        ("Avengers Endgame", "Action", 181),
        ("Interstellar", "SciFi", 169),
        ("Inception", "SciFi", 148),
        ("Toy Story 4", "Anim", 100),
        ("Spiderman NWH", "Action", 148),
        ("Minions 2", "Anim", 87)
    ]

    movie_objs = [Movie(title=t, genre=g, durasi=d, price=ticket_price(d)) for t, g, d in films]
    db.add_all(movie_objs)
    db.commit()
    print("Movies seeded: 6")

    studios = []
    for i in range(1, NUM_STUDIOS + 1):
        r = random.randint(MIN_ROWS, MIN_ROWS + 7)
        c = random.randint(MIN_COLS, MIN_COLS + 14)
        s = Studio(name=f"Studio {i}", rows=r, cols=c)
        db.add(s)
        db.flush()

        row_letters = [chr(ord('A') + idx) for idx in range(r)]
        seats = [StudioSeat(studio_id=s.id, row=rr, col=cc) for rr in row_letters for cc in range(1, c + 1)]
        db.add_all(seats)
        studios.append(s)
    db.commit()
    print(f"Studios seeded: {len(studios)}")

    members = []
    for _ in range(NUM_MEMBERS):
        m = Membership(nama=fake.name())
        db.add(m)
        members.append(m)
    db.commit()
    print(f"Memberships seeded: {len(members)}")

    jadwals = []
    showtimes = [datetime.time(11, 0), datetime.time(15, 0), datetime.time(19, 0)]
    for day in range(1, 32):
        tgl = datetime.date(2024, 12, day)
        wd = get_weekday(tgl)
        for mv in movie_objs:
            for jam in showtimes:
                st = random.choice(studios)
                jd = Jadwal(movie_id=mv.id, studio_id=st.id, tanggal=tgl, jam=jam, weekday=wd)
                db.add(jd)
                jadwals.append(jd)
    db.commit()
    print(f"Jadwal seeded: {len(jadwals)}")

    promo_list = [
        ("Tanpa Promo", 0),
        ("Promo Akhir Tahun", 10),
        ("Member Gold", 15),
        ("Promo Bank XYZ", 20),
        ("Promo Midnight", 5)
    ]
    pay_opts = ["Cash", "QRIS", "Debit", "Gopay", "ShopeePay"]

    done = 0
    attempts = 0
    max_attempts = ORDERS_TO_GENERATE * 20

    start = time.time()
    while done < ORDERS_TO_GENERATE and attempts < max_attempts:
        attempts += 1

        j = random.choice(jadwals)
        tgl = random_december_date()
        wd = get_weekday(tgl)

        st = db.query(Studio).filter_by(id=j.studio_id).first()
        mv = db.query(Movie).filter_by(id=j.movie_id).first()
        price = mv.price

        member = random.choice(members)
        seat_want = random.randint(1, 6)

        promo_name, disc = random.choice(promo_list)
        row_letters = [chr(ord('A') + idx) for idx in range(st.rows)]

        chosen = []
        tries = 0
        while len(chosen) < seat_want and tries < 60:
            tries += 1
            r = random.choice(row_letters)
            c = random.randint(1, st.cols)
            if (r, c) in chosen:
                continue
            if seat_available(db, j.id, st.id, r, c):
                chosen.append((r, c))

        if not chosen:
            continue

        tot = len(chosen) * price
        fin = tot - int(tot * disc / 100)

        ordx = Order(
            order_code=str(uuid.uuid4())[:12],
            membership_id=member.id,
            jadwal_id=j.id,
            payment_method=random.choice(pay_opts),
            seat_count=len(chosen),
            discount=disc,
            promo_name=promo_name,
            total_price=tot,
            final_price=fin,
            created_at=datetime.datetime.now(),
            transaction_date=tgl,
            weekday=wd
        )

        db.add(ordx)
        db.flush()

        for a, b in chosen:
            db.add(OrderSeat(order_id=ordx.id, jadwal_id=j.id, studio_id=st.id, row=a, col=b))

        try:
            db.commit()
            done += 1
        except:
            db.rollback()
            continue

    print(f"Orders generated: {done}")

    print("== DONE SEEDING ==")

if __name__ == "__main__":
    main()
