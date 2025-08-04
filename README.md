# Property237 - NGS Holdings

**Cameroon’s No.1 Property Platform**

Property237.com is a robust web application enabling users to find, filter, and contact landlords and realtors for rentals, sales, and guesthouses across Cameroon and the CEMAC region. Realtors and landlords can list properties, complete KYC verification, pay posting fees, and manage ads. The platform features advanced property filtering, secure payments, and agent verification badges.

---

## Features

- **User Registration & Authentication:** Secure signup, role-based access (user/realtor), email verification.
- **Property Listings:** Realtors/landlords can list diverse property types with detailed attributes and images.
- **Advanced Filtering:** Filter by location, price, bedrooms, amenities, and more.
- **KYC Verification:** Realtors complete identity checks and document uploads for badge verification.
- **Payments:** Ad posting payments integrated via Flutterwave and Tranzak.net.
- **Admin Dashboard:** Manage ads, KYC, reviews, and agent status.
- **Responsive API:** Built with Django REST Framework for frontend, mobile, and third-party integrations.
- **Dockerized:** Easily deployable with Docker & Docker Compose.
- **Production-Ready:** Secure settings, logging, backup, and deployment scripts.

---

## Tech Stack

- **Backend:** Python 3.11+, Django 4.x, Django REST Framework
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **Payments:** Flutterwave, Tranzak.net
- **Testing:** Pytest, Django Test, DRF Test
- **Other:** Celery (async tasks), Gunicorn/Nginx (production), Swagger/OpenAPI (API docs)

---

## Getting Started

### Prerequisites

- Docker & Docker Compose installed
- Python 3.11+ (for local development without Docker)
- PostgreSQL (for local development without Docker)

### Environment Variables

Copy `.env.example` to `.env` and configure with your secrets:

```env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
POSTGRES_DB=property237
POSTGRES_USER=property237_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
FLUTTERWAVE_API_KEY=your_flutterwave_key
TRANZAK_API_KEY=your_tranzak_key
```

### Local Development (Docker)

```bash
docker-compose up --build
```

- Django API: `http://localhost:8000/`
- Swagger Docs: `http://localhost:8000/api/docs/`
- PostgreSQL: exposed as `db` service in Docker Compose

### Running Migrations

```bash
docker-compose exec web python manage.py migrate
```

### Creating Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## API Documentation

- Swagger/OpenAPI available at `/api/docs/`

---

## Running Tests

```bash
docker-compose exec web pytest
```

---

## Deployment

- Use production Docker Compose settings.
- Configure Gunicorn and Nginx for production.
- Set `DJANGO_DEBUG=False` and proper `ALLOWED_HOSTS`.
- Use HTTPS and configure backups for PostgreSQL and media files.

---

## Contributing

Pull requests are welcome! Please open issues for feature requests or bugs.

---

## License

MIT License

---

## Contact

For questions, partnerships, or support, contact [admin@property237.com](mailto:admin@property237.com).
