if __name__ == '__main__':
    print('PASSING VALUE TO A FUNCTION, PROVIDED THE ARGUMENT NAME IS STORED IN A VARIABLE')
    
    def one(**kwargs):
        print(kwargs)


    a = 'name_of_argument_in_a_variable'

    one(a='felix')  # that's not what i want
    one(**{a:'felix'})  # got u
    one(**{a+'_with_modification':'felix'})
