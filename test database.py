"""
seed_bioskop_final.py

Script final (tanpa membaca file Excel sama sekali).
Fungsi:
- membuat schema database (MySQL / SQLite via SQLAlchemy)
- generate studio dengan ukuran random (baris >=8, kolom >=6)
- generate seat map (studio_seats)
- generate 100 membership
- generate jadwal (jam tayang)
- generate orders (dengan order_code), order_seats (multiple seats per order)
- menjamin tidak terjadi double-booking saat seeding

Cara pakai:
1) Install dependencies:
   pip install sqlalchemy pymysql faker
2) Edit connection string di bagian CONFIG jika mau pakai MySQL
   contoh MySQL: mysql+pymysql://root:password@localhost:3306/bioskop
   default script menggunakan SQLite file bioskop.db jika tidak diubah
3) Jalankan:
   python seed_bioskop_final.py

Catatan harga berdasarkan durasi:
- durasi < 100 menit: 40_000
- durasi >= 150 menit: 45_000
- durasi >= 180 menit: 50_000
(aturan prioritas: cek >=180 dulu, lalu >=150, lalu <100)

"""

from sqlalchemy import (
    create_engine, Column, Integer, String, Date, Time, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from faker import Faker
import random
import datetime
import uuid
import os

# ===========
# CONFIG
# ===========
# Database connection string: ganti ke MySQL jika perlu
# Contoh MySQL:
# DB_URL = "mysql+pymysql://root:password@localhost:3306/bioskop"
# Default: SQLite file bioskop.db
DB_URL = "mysql+pymysql://root:%40Keju1234@localhost:3306/bioskop"

# Jumlah membership yang ingin di-generate
NUM_MEMBERS = 100
# Jumlah studio
NUM_STUDIOS = 5
# Minimal rows & cols for a studio
MIN_ROWS = 8
MIN_COLS = 6
# Jumlah jadwal per movie
SCHEDULES_PER_MOVIE = 3
# Jumlah random orders yang ingin dibuat saat seeding
NUM_RANDOM_ORDERS = 300

fake = Faker("id_ID")
Base = declarative_base()

# ===========
# MODELS
# ===========
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(100))
    durasi = Column(Integer)
    rating_usia = Column(String(20))
    sutradara = Column(String(255))
    price = Column(Integer)  # harga default per seat untuk movie

    jadwals = relationship("JamTayang", back_populates="movie")

class Studio(Base):
    __tablename__ = "studios"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    baris = Column(Integer, nullable=False)
    kolom = Column(Integer, nullable=False)

    seats = relationship("StudioSeat", back_populates="studio")

class StudioSeat(Base):
    __tablename__ = "studio_seats"
    id = Column(Integer, primary_key=True)
    studio_id = Column(Integer, ForeignKey("studios.id"), nullable=False)
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)

    studio = relationship("Studio", back_populates="seats")

    __table_args__ = (
        UniqueConstraint('studio_id', 'row', 'col', name='uix_studio_row_col'),
    )

class Membership(Base):
    __tablename__ = "memberships"
    id = Column(Integer, primary_key=True)
    nama = Column(String(255), nullable=False)

    orders = relationship("Order", back_populates="member")

class JamTayang(Base):
    __tablename__ = "jadwal"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    studio_id = Column(Integer, ForeignKey("studios.id"), nullable=False)
    tanggal = Column(Date, nullable=False)
    jam = Column(Time, nullable=False)

    movie = relationship("Movie", back_populates="jadwals")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_code = Column(String(64), unique=True, nullable=False)
    membership_id = Column(Integer, ForeignKey("memberships.id"), nullable=False)
    jadwal_id = Column(Integer, ForeignKey("jadwal.id"), nullable=False)
    payment_method = Column(String(50))
    total_price = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    member = relationship("Membership", back_populates="orders")
    seats = relationship("OrderSeat", back_populates="order")

class OrderSeat(Base):
    __tablename__ = "order_seats"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    studio_id = Column(Integer, ForeignKey("studios.id"), nullable=False)
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="seats")

    __table_args__ = (
        UniqueConstraint('order_id', 'studio_id', 'row', 'col', name='uix_order_studio_row_col'),
    )

# ===========
# UTIL: price rule
# ===========

def harga_dari_durasi(durasi):
    if durasi >= 180:
        return 50000
    if durasi >= 150:
        return 45000
    if durasi < 100:
        return 40000
    return 40000

# ===========
# SETUP DB
# ===========
engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

# ===========
# SEED FUNCTIONS
# ===========

def seed_movies_manual(session):
    """Buat list movie manual di sini (TIDAK membaca Excel)."""
    movie_list = [
        {"title": "Avengers: Endgame", "genre": "Action", "durasi": 181, "rating": "13+", "sutradara": "Anthony Russo"},
        {"title": "Interstellar", "genre": "Sci-Fi", "durasi": 169, "rating": "13+", "sutradara": "Christopher Nolan"},
        {"title": "Inception", "genre": "Sci-Fi", "durasi": 148, "rating": "13+", "sutradara": "Christopher Nolan"},
        {"title": "Toy Story 4", "genre": "Animation", "durasi": 100, "rating": "SU", "sutradara": "Josh Cooley"},
        {"title": "Spider-Man: No Way Home", "genre": "Action", "durasi": 148, "rating": "13+", "sutradara": "Jon Watts"},
        {"title": "Minions: The Rise of Gru", "genre": "Animation", "durasi": 87, "rating": "SU", "sutradara": "Kyle Balda"},
        {"title": "Fast X", "genre": "Action", "durasi": 142, "rating": "13+", "sutradara": "Louis Leterrier"},
        {"title": "Inside Out 2", "genre": "Animation", "durasi": 96, "rating": "SU", "sutradara": "Kelsey Mann"},
        {"title": "Dune Part Two", "genre": "Sci-Fi", "durasi": 166, "rating": "13+", "sutradara": "Denis Villeneuve"},
        {"title": "Avatar: The Way of Water", "genre": "Sci-Fi", "durasi": 192, "rating": "13+", "sutradara": "James Cameron"},
    ]

    created = []
    for m in movie_list:
        price = harga_dari_durasi(m["durasi"])
        mv = Movie(title=m["title"], genre=m["genre"], durasi=m["durasi"], rating_usia=m["rating"], sutradara=m["sutradara"], price=price)
        session.add(mv)
        created.append(mv)
    session.commit()
    return created


def seed_studios_and_seats(session, num_studios=NUM_STUDIOS):
    studios = []
    for i in range(1, num_studios+1):
        baris = random.randint(MIN_ROWS, 15)
        kolom = random.randint(MIN_COLS, 20)
        s = Studio(name=f"Studio {i}", baris=baris, kolom=kolom)
        session.add(s)
        session.flush()

        seats = []
        for r in range(1, baris+1):
            for c in range(1, kolom+1):
                seats.append(StudioSeat(studio_id=s.id, row=r, col=c))
        session.add_all(seats)
        studios.append(s)
    session.commit()
    return studios


def seed_members(session, n=NUM_MEMBERS):
    members = []
    for _ in range(n):
        m = Membership(nama=fake.name())
        session.add(m)
        members.append(m)
    session.commit()
    return members


def seed_jadwal(session, movies, studios):
    jadwals = []
    today = datetime.date.today()
    year = today.year
    month = today.month

    for mv in movies:
        for _ in range(SCHEDULES_PER_MOVIE):
            s = random.choice(studios)
            day = random.randint(1, 28)
            jam = datetime.time(random.randint(10, 22), random.choice([0, 15, 30, 45]))
            jt = JamTayang(movie_id=mv.id, studio_id=s.id, tanggal=datetime.date(year, month, day), jam=jam)
            session.add(jt)
            jadwals.append(jt)
    session.commit()
    return jadwals


def is_seat_available(session, jadwal_id, studio_id, row, col):
    q = session.query(OrderSeat).join(Order).filter(
        Order.jadwal_id == jadwal_id,
        OrderSeat.studio_id == studio_id,
        OrderSeat.row == row,
        OrderSeat.col == col
    ).first()
    return q is None


def create_order(session, membership_id, jadwal_id, studio_id, seat_list, payment_method):
    for (r, c) in seat_list:
        if not is_seat_available(session, jadwal_id, studio_id, r, c):
            raise ValueError(f"Seat not available: {r}-{c} for jadwal {jadwal_id}")

    order_code = str(uuid.uuid4())[:8].upper()
    order = Order(order_code=order_code, membership_id=membership_id, jadwal_id=jadwal_id,
                  payment_method=payment_method, timestamp=datetime.datetime.utcnow())
    session.add(order)
    session.flush()

    total = 0
    jadwal = session.query(JamTayang).filter(JamTayang.id == jadwal_id).first()
    movie = session.query(Movie).filter(Movie.id == jadwal.movie_id).first()
    harga_per_seat = movie.price

    for (r, c) in seat_list:
        os = OrderSeat(order_id=order.id, studio_id=studio_id, row=r, col=c, price=harga_per_seat)
        session.add(os)
        total += harga_per_seat

    order.total_price = total
    session.commit()
    return order


def generate_random_orders(session, members, jadwals, max_orders=NUM_RANDOM_ORDERS):
    payment_options = ["Cash", "Dana", "Gopay", "ShopeePay", "Debit", "Kredit"]
    created = 0
    attempts = 0
    max_attempts = max_orders * 10

    while created < max_orders and attempts < max_attempts:
        attempts += 1
        m = random.choice(members)
        j = random.choice(jadwals)
        studio = session.query(Studio).filter(Studio.id == j.studio_id).first()

        k = random.randint(1, 5)

        chosen = []
        tries = 0
        while len(chosen) < k and tries < 100:
            tries += 1
            r = random.randint(1, studio.baris)
            c = random.randint(1, studio.kolom)
            if (r, c) in chosen:
                continue
            if is_seat_available(session, j.id, studio.id, r, c):
                chosen.append((r, c))
        if len(chosen) == 0:
            continue

        try:
            create_order(session, membership_id=m.id, jadwal_id=j.id, studio_id=studio.id, seat_list=chosen,
                         payment_method=random.choice(payment_options))
            created += 1
        except Exception:
            session.rollback()
            continue

    print(f"Generated {created} random orders (attempts {attempts})")

# ===========
# MAIN
# ===========

def main():
    print("Init DB ->", DB_URL)
    init_db()
    session = SessionLocal()

    # 1) seed movies (manual, no Excel)
    movies = seed_movies_manual(session)
    print(f"Seeded {len(movies)} movies")

    # 2) seed studios + seats
    studios = seed_studios_and_seats(session, NUM_STUDIOS)
    print(f"Seeded {len(studios)} studios (dan seat map)")

    # 3) seed members
    members = seed_members(session, NUM_MEMBERS)
    print(f"Seeded {len(members)} memberships")

    # 4) seed jadwal
    jadwals = seed_jadwal(session, movies, studios)
    print(f"Seeded {len(jadwals)} jadwal (schedules)")

    # 5) generate random orders (safe booking)
    generate_random_orders(session, members, jadwals, NUM_RANDOM_ORDERS)

    # demo: contoh order manual
    try:
        demo_member = members[0]
        demo_jadwal = jadwals[0]
        demo_studio = session.query(Studio).filter(Studio.id == demo_jadwal.studio_id).first()
        demo_seats = [(1,1), (1,2)]
        order = create_order(session, membership_id=demo_member.id, jadwal_id=demo_jadwal.id,
                             studio_id=demo_studio.id, seat_list=demo_seats, payment_method="Gopay")
        print("Contoh order dibuat: order_code=", order.order_code)
    except Exception as e:
        print("Gagal buat demo order:", e)

    session.close()
    print("SELESAI: Database telah di-seed dan transaksi + kursi dibuat")

if __name__ == '__main__':
    main()
