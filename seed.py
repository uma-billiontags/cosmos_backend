import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from rooms.models import Room, Space, SpaceMember

def seed():
    # 1. Create Admin User
    admin_user, created = User.objects.get_or_create(
        email='sarah.admin@billiontags.com',
        defaults={
            'name': 'Sarah Connor (Admin)',
            'role': 'Admin',
            'is_staff': True,
            'is_superuser': True,
            'status': 'online',
        }
    )
    admin_user.set_password('Password123!')
    admin_user.save()
    print(f"Admin User: {admin_user.email} (Password: Password123!)")

    # 2. Create Employee User
    emp_user, created = User.objects.get_or_create(
        email='alex.rivera@billiontags.com',
        defaults={
            'name': 'Alex Rivera (Engineer)',
            'role': 'Employee',
            'status': 'online',
        }
    )
    emp_user.set_password('Password123!')
    emp_user.save()
    print(f"Employee User: {emp_user.email} (Password: Password123!)")

    # 3. Create Sample Spaces & Memberships
    space_admin, _ = Space.objects.get_or_create(
        id='billiontags-team',
        defaults={
            'name': 'Billiontags_Team',
            'owner': admin_user,
            'admin_access': True,
            'is_free': True,
        }
    )
    SpaceMember.objects.get_or_create(
        space=space_admin,
        user=admin_user,
        defaults={'role': 'admin'}
    )
    SpaceMember.objects.get_or_create(
        space=space_admin,
        user=emp_user,
        defaults={'role': 'member'}
    )

    space_creation, _ = Space.objects.get_or_create(
        id='billiontags-creation',
        defaults={
            'name': 'Billiontags creation',
            'owner': emp_user,
            'admin_access': True,
            'is_free': True,
        }
    )
    SpaceMember.objects.get_or_create(
        space=space_creation,
        user=emp_user,
        defaults={'role': 'admin'}
    )
    SpaceMember.objects.get_or_create(
        space=space_creation,
        user=admin_user,
        defaults={'role': 'member'}
    )
    print("Spaces and memberships seeded: Billiontags_Team & Billiontags creation")

    # 4. Create Default Rooms
    rooms_data = [
        {
            'name': 'All-Hands Auditorium',
            'type': 'permanent',
            'capacity': 50,
            'description': 'Main company auditorium for office-wide announcements and town halls.',
            'created_by': admin_user,
            'space': space_admin,
        },
        {
            'name': 'Engineering Huddle',
            'type': 'permanent',
            'capacity': 10,
            'description': 'Sprint planning and technical sync for developers.',
            'created_by': admin_user,
            'space': space_admin,
        },
        {
            'name': 'Cowork Central Desk',
            'type': 'permanent',
            'capacity': 8,
            'description': 'Open co-working desk space for drop-in discussions.',
            'created_by': admin_user,
            'space': space_admin,
        },
        {
            'name': 'Design Critique (Temp)',
            'type': 'temporary',
            'capacity': 4,
            'description': 'Ad-hoc huddle space created by team.',
            'created_by': emp_user,
            'space': space_creation,
        },
    ]

    for r_data in rooms_data:
        room, _ = Room.objects.get_or_create(
            name=r_data['name'],
            defaults=r_data
        )
        print(f"Room ready: {room.name} ({room.type})")

    print("\n[SUCCESS] Seed data loaded successfully!")

if __name__ == '__main__':
    seed()
