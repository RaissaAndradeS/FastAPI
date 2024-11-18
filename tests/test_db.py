from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='raissinha',
        email='raissa@ra.com',
        password='mysenha',
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'raissa@ra.com')
    )

    assert result.username == 'raissinha'
