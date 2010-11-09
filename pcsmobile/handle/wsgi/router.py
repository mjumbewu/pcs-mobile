from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcsmobile.handle.wsgi.cancel_reservation import CancelReservationHandler
from pcsmobile.handle.wsgi.choose_datetime import ChooseDateTimeHandler
from pcsmobile.handle.wsgi.choose_location import ChooseLocationHandler
from pcsmobile.handle.wsgi.choose_vehicle import ChooseVehicleHandler
from pcsmobile.handle.wsgi.confirm_cancel import ConfirmCancellationHandler
from pcsmobile.handle.wsgi.confirm_create import ConfirmReservationHandler
from pcsmobile.handle.wsgi.create_reservation import CreateReservationHandler
from pcsmobile.handle.wsgi.index import IndexHandler
from pcsmobile.handle.wsgi.my_reservations import MyReservationsHandler
from pcsmobile.handle.wsgi.my_session import MySessionHandler
from pcsmobile.handle.wsgi.reservation_info import ReservationInfoHandler

application = webapp.WSGIApplication(
        [('/', IndexHandler),
         ('/cancel_reservation', CancelReservationHandler),
         ('/choose_datetime', ChooseDateTimeHandler),
         ('/choose_location', ChooseLocationHandler),
         ('/choose_vehicle', ChooseVehicleHandler),
         ('/confirm_reservation', ConfirmReservationHandler),
         ('/confirm_cancellation', ConfirmCancellationHandler),
         ('/create_reservation', CreateReservationHandler),
         ('/index.html', IndexHandler),
         ('/login', IndexHandler),
         ('/my_reservations', MyReservationsHandler),
         ('/my_session', MySessionHandler),
         ('/reservation_info', ReservationInfoHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
