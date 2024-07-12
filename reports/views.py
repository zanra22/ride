from django.db import connection
from django.http import JsonResponse

def get_distinct_months():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT strftime('%Y-%m', pickup_time) AS month
            FROM rides_ride
            ORDER BY month
        """)
        months = [row[0] for row in cursor.fetchall()]
    return months

def get_trip_report(request):
    try:
        # Step 1: Retrieve distinct months
        months = get_distinct_months()

        # Step 2: Prepare dynamic columns for months
        month_columns = ', '.join(
            [f"SUM(CASE WHEN month = '{month}' THEN count_of_trips ELSE 0 END) AS \"{month}\"" for month in months]
        )
        month_totals = ', '.join(
            [f"SUM(CASE WHEN month = '{month}' THEN count_of_trips ELSE 0 END) AS \"{month}_Total\"" for month in months]
        )

        query = f"""
            WITH RideDurations AS (
                SELECT
                    r.id_driver_id AS driver_id,
                    u.first_name || ' ' || u.last_name AS driver_name,
                    strftime('%Y-%m', r.pickup_time) AS month,
                    r.id_ride,
                    MIN(CASE WHEN re.description = 'Status changed to pickup' THEN re.created_at END) AS pickup_time,
                    MIN(CASE WHEN re.description = 'Status changed to dropoff' THEN re.created_at END) AS dropoff_time
                FROM rides_ride AS r
                INNER JOIN rides_rideevent AS re ON r.id_ride = re.id_ride_id
                INNER JOIN accounts_user AS u ON r.id_driver_id = u.id_user
                WHERE re.description IN ('Status changed to pickup', 'Status changed to dropoff')
                GROUP BY r.id_driver_id, u.first_name, u.last_name, strftime('%Y-%m', r.pickup_time), r.id_ride
            ),
            FilteredRides AS (
                SELECT
                    driver_id,
                    driver_name,
                    month,
                    id_ride,
                    pickup_time,
                    dropoff_time,
                    (julianday(dropoff_time) - julianday(pickup_time)) * 24 AS duration_hours
                FROM RideDurations
                WHERE pickup_time IS NOT NULL AND dropoff_time IS NOT NULL
            ),
            DriverMonthCounts AS (
                SELECT
                    driver_id,
                    driver_name,
                    month,
                    COUNT(id_ride) AS count_of_trips
                FROM FilteredRides
                WHERE duration_hours > 1
                GROUP BY driver_id, driver_name, month
            ),
            MonthlyTotals AS (
                SELECT
                    driver_id,
                    driver_name,
                    {month_columns},
                    SUM(count_of_trips) AS Grand_Total
                FROM DriverMonthCounts
                GROUP BY driver_id, driver_name
            ),
            MonthTotals AS (
                SELECT
                    {month_totals},
                    SUM(count_of_trips) AS Total
                FROM DriverMonthCounts
            )
            SELECT
                driver_name AS Driver,
                {', '.join([f'dmc.\"{month}\"' for month in months])},
                dmc.Grand_Total
            FROM MonthlyTotals dmc
            UNION ALL
            SELECT
                'Grand Total' AS Driver,
                {', '.join([f'mt.\"{month}_Total\"' for month in months])},
                mt.Total
            FROM MonthTotals mt;
        """

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        # Step 3: Format the results
        report = []
        for row in results:
            # Handling null values for driver
            driver_name = row[0] if row[0] is not None else "Unknown Driver"
            report.append({
                'driver': driver_name,
                **{months[i]: row[i + 1] for i in range(len(months))},
                'grand_total': row[-1]
            })
        print(report)

        return JsonResponse(report, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
