from flask import Flask, render_template

import data


app = Flask(__name__)


@app.errorhandler(KeyError)
@app.errorhandler(404)
def error(err):
    return render_template(
        'error.html',
        data=data,
        title='Stepik Travel - Oops...',
    )


@app.route('/')
def index():
    title = 'Stepik Travel'
    return render_template(
        'index.html',
        title=title,
        data=data,
        tours=data.tours
    )


@app.route('/departures/<departures>/')
def departures(departures):
    title = f'Stepik Travel - ' + data.departures[departures]
    tours = dict(filter(lambda tour: tour[1]['departure'] == departures, data.tours.items()))
    min_price = float('inf')
    max_price = float('-inf')
    min_night = float('inf')
    max_night = float('-inf')
    for value in tours.values():
        if value['price'] < min_price:
            min_price = value['price']
        if value['price'] > max_price:
            max_price = value['price']
        if value['nights'] < min_night:
            min_night = value['nights']
        if value['nights'] > max_night:
            max_night = value['nights']

    return render_template(
        'departure.html',
        title=title,
        data=data,
        dep=departures,
        tours=tours,
        min_night=min_night,
        min_price=min_price,
        max_night=max_night,
        max_price=max_price
    )


@app.route('/tour/<int:id>/')
def tour(id):
    tour_active = data.tours[id]
    title = tour_active['title']
    from_tour = tour_active['country']

    return render_template(
        'tour.html',
        title=title,
        tour_active=tour_active,
        data=data,
        from_tour=from_tour
    )


if __name__ == '__main__':
    app.run(debug=True)
