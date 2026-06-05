from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/', status_code=HTTPStatus.OK)
async def read_users():
    return {'message': 'some get logic'}


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_user():
    return {'message': 'some post logic'}


@router.get('/{user_id}', status_code=HTTPStatus.OK)
async def read_user(user_id: int):
    return {'message': f'some get logic for user {user_id}'}


@router.put('/{user_id}', status_code=HTTPStatus.ACCEPTED)
async def update_user(user_id: int):
    return {'message': f'some put logic for user {user_id}'}


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int):
    return None
