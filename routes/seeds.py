from config import conf


async def generate_points_and_routes():
    query = '''
        WITH alphabet AS (
            SELECT chr(generate_series(65, 90)) letter
        ), 
        points AS (
            INSERT INTO points (name, lat, lon)
                SELECT 
                    letter, 
                    random() * 100, 
                    random() * 100
                FROM alphabet
                RETURNING id
        ), 
        new_routes AS (
            INSERT INTO routes_meta (name)
                SELECT 
                    upper(md5(random()::text)) route_name
                FROM generate_series(0, 10)
                RETURNING id
        )
        INSERT INTO routes (meta, point)
            SELECT 
                ext.id, p.id 
            FROM (
                SELECT 
                    id, row_number() over (ORDER BY id) AS row_num
                FROM new_routes
                CROSS JOIN generate_series(0, 5)
            ) ext
            LEFT JOIN (
                SELECT 
                    id, 
                    row_number() over (ORDER BY random()) AS row_num
                FROM points
                CROSS JOIN generate_series(0, 5)
            ) p ON  ext.row_num = p.row_num
        '''

    conn = await conf.db_conn()
    await conn.execute(query)
