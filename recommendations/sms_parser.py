from .actions_list import ACTIONS_LIST

def exception_returns_false(func):
    def catch_errors(cls, message):
        try: 
            return func(cls, message)
        except Exception as e:
            return False
    
    return catch_errors

class SmsParser:

    @classmethod
    def parse(cls,message, phone):

        if cls.is_create_new_user(message):  
            username = message.split(' ')[-1]
            action = ACTIONS_LIST['create_user']
            response = { 'action': action, 'payload': {'username': username, 'phone': phone} }
        elif cls.is_recommendation_for_me(message):
            name = message[10:-6]
            response = {'action': ACTIONS_LIST['create_recommendation_for_me'], 'payload': {'name': name, 'phone': phone}}
        elif cls.is_recommendation_for_another_user(message):
            username = message.split(' ')[-1]
            name = ' '.join(message.split(' ')[1:-2])
            response = {'action' : ACTIONS_LIST['create_recommendation_for_another_user'], 'payload' : {'name': name, 'recommender_phone': phone, 'recommendee_username': username}}
        elif cls.is_recommendation_acception(message):
            response = {'action': ACTIONS_LIST['accept_recommendation_from_another_user'], 'payload': {'recommendation_id': message[1:], 'phone': phone}}
        else:
            raise ValueError('Message could not be parsed.')
        
        return response
    
    @classmethod
    @exception_returns_false
    def is_recommendation_for_another_user(cls,message):
        message_array = message.split(' ')
        last_word = message_array[-1]
        second_to_last_word = message_array[-2]
        first_word = message_array[0]
        return first_word.lower() == 'recommend' and second_to_last_word.lower() == 'to' and last_word.lower() != 'me'
       
    @classmethod
    @exception_returns_false
    def is_recommendation_for_me(cls,message):
        return message[:10].lower() == 'recommend ' and message[-6:].lower() == ' to me'
        
    
    @classmethod
    @exception_returns_false
    def is_create_new_user(cls,message):
        return message[:5].lower() == 'i am '
        
    
    @classmethod
    @exception_returns_false
    def is_recommendation_acception(cls, message):
        return message[0].lower() == 'r' and message[1:].isdigit()
        
