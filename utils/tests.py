import asyncio
from db import init, create, delete, get_all_by


# create db
asyncio.run(init())


""" CREATE TESTS """
# data_pool = {
#     'name': 'Some name',
#     'file_id': 'Some file id',
#     'file_type': 'Some file type',
#     'text': 'Lorem ipsum dolor sit amet',
#     'button': 'Some button text',
#     'check_user': True,
#     'message_id': 125789678
# }
# pool = asyncio.run(create('pool', data_pool))
# print("Pool:\n", pool, "\n\n")


""" DELETE TESTS """
# delete_pool_byid = asyncio.run(delete('pool', 'id', 1))
# print("Pool delete by id:\n", delete_pool_byid, "\n")
# delete_pool_by_name = asyncio.run(delete('pool', 'name', 'Some name'))
# print("Pool delete by name:\n", delete_pool_by_name, "\n\n")


""" GET ALL BY TEST """
# all_pool_by_name = asyncio.run(get_all_by('pool', ['name', 'id', 'check_user'], 'name', 'Some nam'))
# print(all_pool_by_name)
# all_pool_byid = asyncio.run(get_all_by('pool', ['name', 'id', 'check_user'], 'id', 1))
# print(all_pool_byid)
