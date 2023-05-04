from database import query
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='views',
            static_folder='static', static_url_path='')


@app.route('/')
def state_map():
    ''' Serves state map on main route '''

    evNorm = {}
    ghgTotalNorm = {}
    ghgVehiclesNorm = {}
    # Fill arrays with county average stats
    evDataTuples = query('''SELECT 
        county, 
        (
            County_avg / 
            (1.0 * (
                SELECT MAX(County_avg) 
                FROM County_EV_Average
            ))
        ) AS normalized 
    FROM County_EV_Average 
    ORDER BY County_avg DESC;''')

    if evDataTuples is not None:
        for x in evDataTuples:
            evNorm[x[0]] = x[1]

    ghgTotalNormTuples = query('''SELECT 
        county, 
        (
            County_total_avg / 
            (1.0 * (
                SELECT MAX(County_total_avg) 
                FROM County_GHG_Average
            ))
        ) AS normalized 
    FROM County_GHG_Average 
    ORDER BY County_total_avg DESC;''')

    if ghgTotalNormTuples is not None:
        for x in ghgTotalNormTuples:
            ghgTotalNorm[x[0]] = x[1]

    ghgVehiclesNormTuples = query('''SELECT 
        county, 
        (
            County_vehicle_avg / 
            (1.0 * (
                SELECT MAX(County_vehicle_avg) 
                FROM County_GHG_Average
            ))
        ) AS normalized 
    FROM County_GHG_Average 
    ORDER BY County_vehicle_avg DESC;''')

    if ghgVehiclesNormTuples is not None:
        for x in ghgVehiclesNormTuples:
            ghgVehiclesNorm[x[0]] = x[1]

    return render_template('map.html', info=None, county='', evNorm=evNorm, ghgTotalNorm=ghgTotalNorm, ghgVehiclesNorm=ghgVehiclesNorm)


@app.route('/county/<county>')
def county_map(county):
    ''' Serves individual county maps and statistics, as well as showing average info for the county '''

    evNorm = {}
    ghgTotalNorm = {}
    ghgVehiclesNorm = {}
    # Fill arrays with mun stats

    evNormTuples = query(f'''SELECT 
        mun_name,
        (
            Avg_EV_change / 
            (1.0 * (
                SELECT MAX(Avg_EV_change) 
                FROM Mun_EV_Average 
                WHERE county = '{county}'
            ))
        ) AS normalized 
    FROM Mun_EV_Average 
    WHERE county = '{county}' 
    ORDER BY Avg_EV_change DESC;''')

    if evNormTuples is not None:
        for x in evNormTuples:
            evNorm[x[0]] = x[1]

    ghgTotalNormTuples = query(f'''SELECT 
        mun_name,
        (
            Avg_em_change / 
            (1.0 * (
                SELECT MAX(Avg_em_change) 
                FROM Mun_GHG_Average 
                WHERE county = '{county}'
            ))
        ) AS normalized 
    FROM Mun_GHG_Average 
    WHERE county = '{county}' 
    ORDER BY Avg_em_change DESC;''')

    if ghgTotalNormTuples is not None:
        for x in ghgTotalNormTuples:
            ghgTotalNorm[x[0]] = x[1]

    ghgVehiclesNormTuples = query(f'''SELECT 
        mun_name,
        (
            Avg_em_vehicle_change / 
            (1.0 * (
                SELECT MAX(Avg_em_vehicle_change) 
                FROM Mun_GHG_Average 
                WHERE county = '{county}'
            ))
        ) AS normalized 
    FROM Mun_GHG_Average 
    WHERE county = '{county}' 
    ORDER BY Avg_em_vehicle_change DESC;''')

    if ghgVehiclesNormTuples is not None:
        for x in ghgVehiclesNormTuples:
            ghgVehiclesNorm[x[0]] = x[1]

    # Query the County_GHG_Average table to get the average GHG change and GHG change per vehicle for the county
    countyAvgEV = query(
        f"SELECT County_avg FROM County_EV_Average WHERE county = '{county}';")
    countyAvgGHG = query(
        f"SELECT County_total_avg FROM County_GHG_Average WHERE county = '{county}';")
    countyVehicleGHG = query(
        f"SELECT County_vehicle_avg FROM County_GHG_Average WHERE county = '{county}';")

    infoString = ""
    # Format the info string to include the average EV change, average GHG change, and average GHG change per vehicle for the county
    infoString = '{} County\nAverage EV Change: {:.2f}% per year\nAverage GHG Change: {:.2f,} MTCO2e per year\nAverage GHG Change (Vehicles): {:.2f,} MTCO2e per year'.format(
        county, (countyAvgEV[0][0] * 100), (countyAvgGHG[0][0]), (countyVehicleGHG[0][0]))

    return render_template('map.html', info=infoString, mun='', county=county, evNorm=evNorm, ghgTotalNorm=ghgTotalNorm, ghgVehiclesNorm=ghgVehiclesNorm)


@app.route('/mun/<county>/<mun>')
def county_map_for_state(county, mun):
    ''' Serves specific info for a municipality '''

    evNorm = {}
    ghgTotalNorm = {}
    ghgVehiclesNorm = {}

    # determines stored municipality name using string operations on the name route
    nameParts = mun.split()
    selection = ' '.join(
        nameParts[2:]) + ' ' + nameParts[0].lower() if len(nameParts) > 1 else mun

    # Fill arrays with mun stats
    evNormTuples = query(f'''SELECT 
        mun_name,
        (
            Avg_EV_change / 
            (1.0 * (
                SELECT MAX(Avg_EV_change) 
                FROM Mun_EV_Average 
                WHERE county = '{county}'
            ))
        ) AS normalized 
    FROM Mun_EV_Average 
    WHERE county = '{county}' 
    ORDER BY Avg_EV_change DESC;''')

    if evNormTuples is not None:
        for x in evNormTuples:
            evNorm[x[0]] = x[1]

    ghgTotalNormTuples = query(f'''SELECT 
        mun_name,
        (
            Avg_em_change / 
            (1.0 * (
                SELECT MAX(Avg_em_change) 
                FROM Mun_GHG_Average 
                WHERE county = '{county}'
            ))
        ) AS normalized 
    FROM Mun_GHG_Average 
    WHERE county = '{county}' 
    ORDER BY Avg_em_change DESC;''')

    if ghgTotalNormTuples is not None:
        for x in ghgTotalNormTuples:
            ghgTotalNorm[x[0]] = x[1]

    ghgVehiclesNormTuples = query(f'''SELECT 
        mun_name,
        (
            Avg_em_vehicle_change / 
            (1.0 * (
                SELECT MAX(Avg_em_vehicle_change) 
                FROM Mun_GHG_Average 
                WHERE county = '{county}'
            ))
        ) AS normalized 
    FROM Mun_GHG_Average 
    WHERE county = '{county}' 
    ORDER BY Avg_em_vehicle_change DESC;''')

    if ghgVehiclesNormTuples is not None:
        for x in ghgVehiclesNormTuples:
            ghgVehiclesNorm[x[0]] = x[1]

    # set info var to info on town
    munAvgEV = query(
        f"SELECT Avg_EV_change FROM Mun_EV_Average WHERE county = '{county}' AND mun_name = '{selection}';")
    munAvgGHG = query(
        f"SELECT Avg_em_change FROM Mun_GHG_Average WHERE county = '{county}' AND mun_name = '{selection}';")
    munVehicleGHG = query(
        f"SELECT Avg_em_vehicle_change FROM Mun_GHG_Average WHERE county = '{county}' AND mun_name = '{selection}';")
    infoString = '{} \nAverage EV Change: {:.2f}% per year\nAverage GHG Change: {:.2f,} MTCO2e per year\nAverage GHG Change (Vehicles): {:.2f,} MTCO2e per year'.format(
        mun, (munAvgEV[0][0] * 100), (munAvgGHG[0][0]), (munVehicleGHG[0][0]))

    return render_template('map.html', info=infoString, mun=mun, county=county, evNorm=evNorm, ghgTotalNorm=ghgTotalNorm, ghgVehiclesNorm=ghgVehiclesNorm)


if __name__ == '__main__':
    app.run(debug=True)
