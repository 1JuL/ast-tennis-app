from views.payments_view import PaymentsView
from models.Payment import Payment
import flet as ft

class PaymentsController:
    
    def __init__(self, view:PaymentsView):
        self.view = view
        