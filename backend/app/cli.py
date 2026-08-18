"""CLI utilities for admin tasks."""

import click
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.user import User, Role, Permission, RoleType
from app.core.constants import DEFAULT_ROLES, DEFAULT_PERMISSIONS
from app.services.auth import UserService
from app.schemas.auth import CreateUserRequest
import sys


def init_db():
    """Initialize database (create tables)."""
    click.echo("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    click.echo("Database tables created.")


def seed_roles_and_permissions(db: Session):
    """Seed default roles and permissions."""
    click.echo("Seeding roles and permissions...")

    # Create permissions
    for perm_data in DEFAULT_PERMISSIONS:
        existing = db.query(Permission).filter(
            Permission.resource == perm_data["resource"],
            Permission.action == perm_data["action"],
        ).first()
        if not existing:
            perm = Permission(
                name=f"{perm_data['resource']}:{perm_data['action']}",
                resource=perm_data["resource"],
                action=perm_data["action"],
            )
            db.add(perm)
            click.echo(f"  Created permission: {perm.name}")

    db.commit()

    # Create roles
    for role_name, role_data in DEFAULT_ROLES.items():
        existing = db.query(Role).filter(Role.name == role_name).first()
        if not existing:
            role = Role(
                name=role_name,
                description=role_data["description"],
                role_type=RoleType[role_name],
            )
            db.add(role)
            db.flush()

            # Assign permissions to role
            for perm_ref in role_data["permissions"]:
                if perm_ref == "*:*":
                    # Wildcard: assign all permissions
                    all_perms = db.query(Permission).all()
                    role.permissions.extend(all_perms)
                else:
                    resource, action = perm_ref.split(":")
                    perm = db.query(Permission).filter(
                        Permission.resource == resource,
                        Permission.action == action,
                    ).first()
                    if perm:
                        role.permissions.append(perm)

            db.add(role)
            click.echo(f"  Created role: {role.name}")

    db.commit()
    click.echo("Roles and permissions seeded.")


def create_admin_user(db: Session, username: str, email: str, password: str):
    """Create an admin user."""
    click.echo(f"Creating admin user: {username}...")

    # Check if user already exists
    existing = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing:
        click.echo(f"User {username} already exists.")
        return

    # Create user
    user_request = CreateUserRequest(
        username=username,
        email=email,
        password=password,
        is_superuser=True,
        full_name="Administrator",
    )
    user = UserService.create_user(db, user_request)

    # Assign ADMIN role
    admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
    if admin_role:
        UserService.assign_role(db, user, admin_role)

    click.echo(f"Admin user {username} created successfully.")


@click.command()
def setup_db():
    """Setup database (init, seed roles/permissions)."""
    db = SessionLocal()
    try:
        init_db()
        seed_roles_and_permissions(db)
        click.echo("Database setup complete.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    finally:
        db.close()


@click.command()
@click.option("--username", prompt="Username", help="Username for admin user")
@click.option("--email", prompt="Email", help="Email for admin user")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Password for admin user")
def create_admin(username: str, email: str, password: str):
    """Create an admin user interactively."""
    db = SessionLocal()
    try:
        create_admin_user(db, username, email, password)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
