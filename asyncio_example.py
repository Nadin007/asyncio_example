import asyncio


async def request_hotels(street: str):
    await asyncio.sleep(1)
    return [
        {"name": "Hotel 1", "stars": 5, "id": "1"},
        {"name": "Hotel 2", "stars": 3, "id": "2"},
        {"name": "Hotel 3", "stars": 1, "id": "3"},
    ]


async def request_suites(hotel_id: str):
    suites = [
        {"name": "Suite 1", "price": 100, "hotel_id": "1", "id": "1"},
        {"name": "Suite 2", "price": 200, "hotel_id": "1", "id": "2"},
        {"name": "Suite 3", "price": 120, "hotel_id": "2", "id": "3"},
        {"name": "Suite 4", "price": 150, "hotel_id": "2", "id": "4"},
        {"name": "Suite poor", "price": 10, "hotel_id": "3", "id": "5"},
    ]
    await asyncio.sleep(5)
    return [s for s in suites if s["hotel_id"] == hotel_id]


async def request_apartments(street: str):
    await asyncio.sleep(20)
    return [
        {"name": "Apartment 1", "price": 500, "id": "1"},
        {"name": "Apartment 2", "price": 300, "id": "2"},
        {"name": "Apartment 3", "price": 100, "id": "3"},
    ]


async def request_amenities(apartment_id: str):
    await asyncio.sleep(2)
    return ["wifi", "parking", "pool"]


async def get_hotels(street: str):
    hotels = await request_hotels(street)
    suites = await asyncio.gather(*[request_suites(hotel.get('id')) for hotel in hotels])
    return suites


async def get_appartments(street: str):
    appartments = await request_apartments(street)
    amenities = await asyncio.gather(*[request_amenities(flat.get('id')) for flat in appartments])
    return amenities


async def load_data(street: str, cancel: str = None):
    # Load hotels for the street and load suites for each hotel
    # load_hotels(street) -> load_suites(hotel_id)
    # coros_hotels = [(hotel, await request_suites(hotel.get('id'))) for hotel in await request_hotels(street)]

    tasks = [asyncio.create_task(get_hotels(street)), asyncio.create_task(get_appartments(street))]
    while tasks:
        try:
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for t in done:
                print(t.result())
        except asyncio.CancelledError:
            pass

    # result_hotels, result_appart = await asyncio.gather(asyncio.gather(*coros_hotels), asyncio.gather(*coros_appartmants))
    # Load apartments for the street and load amenities for each apartment
    # load_apartments(street) -> load_amenities(apartment_id)
    # coros_apprt = [(appatr, await request_amenities(appatr.get('id'))) for appatr in await request_apartments(street)]
    # result_appart = await asyncio.gather(*coros_apprt)


loop = asyncio.get_event_loop()
loop.run_until_complete(load_data("Some street"))
