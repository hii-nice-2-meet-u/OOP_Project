import BGC_person
import BGC_menu
import BGC_log
import BGC_operation
from fastapi import FastAPI
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from typing import List, Optional
class BoardGameCafeSystem:
    def __init__(self):
        self.__personlist = []
        self.__version = "1.0"
        self.__orders = []
        self.__branches = []
        self.__reservations = []
    def add_branch(self, branch):
        self.__branches.append(branch)
    def remove_branch(self, branch):
        self.__branches.remove(branch)
    def register_new_member(self, member):
        self.__personlist.append(member)
    def remove_member(self, member):
        self.__personlist.remove(member)
    def login_user(self, username, password):
        for person in self.__personlist:
            if person.get_username() == username and person.get_password() == password:
                return person
        return None
    def check_in_play_table(self, table_id):
        for branch in self.__branches:
            for table in branch.get_play_tables():
                if table.get_table_id() == table_id and table.get_status() == "Available":
                    table.set_status("Occupied")
                    return table
        return None 
    def check_out_play_table(self, table_id):
        for branch in self.__branches:
            for table in branch.get_play_tables():
                if table.get_table_id() == table_id and table.get_status() == "Occupied":
                    table.reset_table()
                    return table
        return None
    def create_reservation(self, customer, table_id, reservation_time):
        reservation = BGC_operation.Reservation(customer, table_id, reservation_time)
        self.__reservations.append(reservation)
        return reservation
    def check_availablity(self, table_id, reservation_time):
        for reservation in self.__reservations:
            if reservation.get_table_id() == table_id and reservation.get_reservation_time() == reservation_time:
                return False
        return True
    def confirm_reservation(self, reservation):
        reservation.set_status("Confirmed")
    def cancel_reservation(self, reservation):
        reservation.set_status("Cancelled")
        
    def view_menu(self, branch):
        return branch.get_menu()
    def place_order(self, branch, order):
        branch.add_order(order)
        self.__orders.append(order)
    def process_payment(self, order, payment_method):
        order.set_payment_status("Paid")
        order.set_payment_method(payment_method)
    def get_reservation_report(self):
        return self.__reservations
    def get_sales_report(self):
        return self.__orders
    def add_board_game_to_inventory(self, branch, board_game):
        branch.add_board_game(board_game)
    def remove_board_game_from_inventory(self, branch, board_game):
        branch.remove_board_game(board_game)
    def add_play_table_to_branch(self, branch, play_table):
        branch.add_play_table(play_table)
    def remove_play_table_from_branch(self, branch, play_table):
        branch.remove_play_table(play_table)
    
class BoardGameCafeBranch:
    def __init__(self):
        self.__cafe_id = None
        self.__name = None
        self.__location = None
        self.__board_games = []
        self.__play_tables = []
        self.__inventory = []


